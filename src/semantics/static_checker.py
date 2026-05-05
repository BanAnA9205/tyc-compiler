"""
Static Semantic Checker for TyC Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the TyC procedural programming language. It performs type checking,
scope management, type inference, and detects all semantic errors as
specified in the TyC language specification.
"""

from functools import reduce
from typing import (
    Dict,
    List,
    Set,
    Optional,
    Any,
    Tuple,
    NamedTuple,
    Union,
    TYPE_CHECKING,
)
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode,
    Program,
    StructDecl,
    MemberDecl,
    FuncDecl,
    Param,
    VarDecl,
    IfStmt,
    WhileStmt,
    ForStmt,
    BreakStmt,
    ContinueStmt,
    ReturnStmt,
    BlockStmt,
    SwitchStmt,
    CaseStmt,
    DefaultStmt,
    Type,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    BinaryOp,
    PrefixOp,
    PostfixOp,
    AssignExpr,
    MemberAccess,
    FuncCall,
    Identifier,
    StructLiteral,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    ExprStmt,
    Expr,
    Stmt,
    Decl,
)

# Type aliases for better type hints
TyCType = Union[IntType, FloatType, StringType, VoidType, StructType]
from .static_error import (
    StaticError,
    Redeclared,
    UndeclaredIdentifier,
    UndeclaredFunction,
    UndeclaredStruct,
    TypeCannotBeInferred,
    TypeMismatchInStatement,
    TypeMismatchInExpression,
    MustInLoop,
)


# ---------------------------------------------------------------------------
# Type helpers
# ---------------------------------------------------------------------------

# Operators that only accept int operands
INT_ONLY_OPS = {"%", "&&", "||", "!", "++", "--"}
# Operators that accept int or float operands (result depends on operand types)
NUMERIC_OPS = {"+", "-", "*", "/"}
# Relational operators: accept int or float, always produce int
RELATIONAL_OPS = {"<", "<=", ">", ">=", "==", "!="}


def type_of(t):
    """Return a canonical category string for a type/literal, or None if unknown."""
    if t is None:
        return None  # auto / unresolved
    if isinstance(t, (IntType, IntLiteral)):
        return "int"
    if isinstance(t, (FloatType, FloatLiteral)):
        return "float"
    if isinstance(t, (StringType, StringLiteral)):
        return "string"
    if isinstance(t, VoidType):
        return "void"
    if isinstance(t, (StructType, StructLiteral)):
        return "struct"
    return None


def types_match(a, b):
    """Check whether two resolved types are the same TyC type."""
    ca, cb = type_of(a), type_of(b)
    if ca is None or cb is None or ca != cb:
        return False
    if isinstance(a, StructType) and isinstance(b, StructType):
        return a.struct_name == b.struct_name
    return True


def is_numeric(cat):
    return cat in ("int", "float")


def to_formal(t):
    """Given a type or literal, return the corresponding formal Type node."""
    cat = type_of(t)
    if cat == "int":
        return IntType()
    if cat == "float":
        return FloatType()
    if cat == "string":
        return StringType()
    if cat == "void":
        return VoidType()
    if isinstance(t, StructType):
        return t
    return t  # fallback


# ---------------------------------------------------------------------------
# Scope & Symbol Table
# ---------------------------------------------------------------------------

class Scope:
    """A single scope level: the AST node that opened it + its symbols."""
    __slots__ = ("node", "symbols")

    def __init__(self, node=None):
        self.node = node
        self.symbols: Dict[str, Any] = {}


class SymbolTable:
    """Stack of scopes for variable/parameter resolution."""

    def __init__(self):
        self.scopes: List[Scope] = [Scope()]  # global scope

    def enter(self, node=None):
        self.scopes.append(Scope(node))

    def exit(self):
        return self.scopes.pop()

    # --- queries ---

    def current_scope(self) -> Scope:
        return self.scopes[-1]

    def lookup(self, name: str):
        """Search from innermost scope outward; return stored type or sentinel."""
        for scope in reversed(self.scopes):
            if name in scope.symbols:
                return scope.symbols[name]
        return ...  # not found (distinct from None = auto/unresolved)

    def declared_in_current(self, name: str) -> bool:
        return name in self.scopes[-1].symbols

    def find_enclosing(self, *node_types):
        """Walk scope stack looking for a scope opened by one of node_types."""
        for scope in reversed(self.scopes):
            if isinstance(scope.node, tuple(node_types)):
                return scope.node
        return None

    def find_func(self) -> Optional[FuncDecl]:
        return self.find_enclosing(FuncDecl)

    # --- mutations ---

    def declare(self, name: str, typ):
        self.scopes[-1].symbols[name] = typ

    def update_auto(self, name: str, new_type):
        """Set the type of an as-yet-unresolved auto variable. Returns True if updated."""
        for scope in reversed(self.scopes):
            if name in scope.symbols:
                if scope.symbols[name] is not None:
                    return False  # already resolved
                scope.symbols[name] = new_type
                return True
        return False


# ---------------------------------------------------------------------------
# Environment – bundles all checker state
# ---------------------------------------------------------------------------

_BUILTINS = {
    "printInt":    FuncDecl(VoidType(),   "printInt",    [Param(IntType(), "x")],    None),
    "printFloat":  FuncDecl(VoidType(),   "printFloat",  [Param(FloatType(), "x")],  None),
    "printString": FuncDecl(VoidType(),   "printString", [Param(StringType(), "x")], None),
    "readInt":     FuncDecl(IntType(),    "readInt",     [],                         None),
    "readFloat":   FuncDecl(FloatType(),  "readFloat",   [],                         None),
    "readString":  FuncDecl(StringType(), "readString",  [],                         None),
}


class Environment:
    def __init__(self):
        self.sym = SymbolTable()
        self.structs: Dict[str, List[MemberDecl]] = {}
        self.funcs: Dict[str, FuncDecl] = dict(_BUILTINS)


# ---------------------------------------------------------------------------
# Static Checker
# ---------------------------------------------------------------------------

class StaticChecker(ASTVisitor):
    def __init__(self):
        super().__init__()
        self.env = Environment()

    def check_program(self, ast):
        return self.visit(ast, self.env)

    # -----------------------------------------------------------------------
    # Internal helpers
    # -----------------------------------------------------------------------

    def _ensure_declared_struct_type(self, declared_type, o):
        if isinstance(declared_type, StructType) and declared_type.struct_name not in o.structs:
            raise UndeclaredStruct(declared_type.struct_name)

    def _validate_typed_declaration(self, declared_type, error_node, o):
        if declared_type is None:
            raise TypeCannotBeInferred(error_node)
        if isinstance(declared_type, VoidType):
            raise TypeMismatchInStatement(error_node)
        self._ensure_declared_struct_type(declared_type, o)

    def _anchor_auto(self, expr_node, resolved_type, o):
        """If expr_node is an Identifier whose type is still None (auto), fix it."""
        if (resolved_type is not None
                and isinstance(expr_node, Identifier)
                and o.sym.lookup(expr_node.name) is None):
            o.sym.update_auto(expr_node.name, resolved_type)

    def _anchor_struct_literal(self, target_type: StructType, lit: StructLiteral, o):
        """Recursively resolve auto variables hidden inside a struct literal."""
        members = o.structs.get(target_type.struct_name)
        if not members or len(members) != len(lit.values):
            return
        for mem, val in zip(members, lit.values):
            if isinstance(val, Identifier) and o.sym.lookup(val.name) is None:
                o.sym.update_auto(val.name, mem.member_type)
            elif isinstance(val, StructLiteral) and isinstance(mem.member_type, StructType):
                self._anchor_struct_literal(mem.member_type, val, o)

    def _check_condition(self, cond_node, stmt_node, o):
        """Validate an expression used as a condition (must be int)."""
        cond_type = self.visit(cond_node, o)
        if cond_type is None:
            # auto variable in condition context: infer as int
            if isinstance(cond_node, Identifier):
                o.sym.update_auto(cond_node.name, IntType())
                return
            raise TypeCannotBeInferred(stmt_node)
        if isinstance(cond_type, StructLiteral):
            raise TypeMismatchInExpression(cond_node)
        if type_of(cond_type) != "int":
            raise TypeMismatchInStatement(stmt_node)


    def _is_self_call(self, init_value, o):
        """Check if init_value is a direct FuncCall to the current function with unresolved return type."""
        if not isinstance(init_value, FuncCall):
            return False
        func = o.sym.find_func()
        return func is not None and init_value.name == func.name and func.return_type is None

    def _struct_literal_compatible(self, target: StructType, rhs, o, rhs_expr=None):
        """Check if a StructLiteral (already visited -> list of types) matches a struct type.

        When rhs_expr is provided (original AST StructLiteral), mismatch errors are raised
        at the most specific struct literal node.
        """
        if not isinstance(rhs, StructLiteral):
            return False
        members = o.structs.get(target.struct_name)
        if members is None or len(members) != len(rhs.values):
            if rhs_expr is not None:
                raise TypeMismatchInExpression(rhs_expr)
            return False
        for idx, (mem, val_type) in enumerate(zip(members, rhs.values)):
            val_expr = None
            if isinstance(rhs_expr, StructLiteral) and idx < len(rhs_expr.values):
                val_expr = rhs_expr.values[idx]

            if val_type is None:
                # Unresolved auto — inferred from struct member type (compatible)
                continue
            if isinstance(val_type, StructLiteral) and isinstance(mem.member_type, StructType):
                nested_expr = val_expr if isinstance(val_expr, StructLiteral) else None
                if not self._struct_literal_compatible(mem.member_type, val_type, o, nested_expr):
                    return False
            elif not types_match(mem.member_type, val_type):
                if rhs_expr is not None:
                    raise TypeMismatchInExpression(rhs_expr)
                return False
        return True

    def _assignment_compatible(self, lhs_type, rhs_type, o, rhs_expr=None):
        """Check if rhs_type can be assigned to lhs_type.
        Both must be resolved. Returns True if compatible."""
        if lhs_type is None or rhs_type is None:
            return False
        # lhs must be a proper value type
        if not isinstance(lhs_type, (IntType, FloatType, StringType, StructType)):
            return False
        # struct literal on rhs
        if isinstance(rhs_type, StructLiteral):
            if not isinstance(lhs_type, StructType):
                return False
            return self._struct_literal_compatible(lhs_type, rhs_type, o, rhs_expr)
        return types_match(lhs_type, rhs_type)

    def _check_unresolved_autos(self, scope: Scope, error_node):
        """After finishing a scope, check for any auto variables still unresolved."""
        deferred_names = {n.name for n, _ in getattr(self, '_deferred_self_calls', [])}
        for name, typ in scope.symbols.items():
            if typ is None and name not in deferred_names:
                raise TypeCannotBeInferred(error_node)

    def _check_op(self, node, lhs_type, op, rhs_type):
        """Unified operator type checking. Returns the result type.
        lhs_type is None for prefix ops; rhs_type is None for postfix ops."""
        lcat = type_of(lhs_type)  # None for prefix unary
        rcat = type_of(rhs_type)  # None for postfix unary
        # --- int-only operators: %, &&, ||, !, ++, -- ---
        if op in INT_ONLY_OPS:
            # For unary: one side is None (unused)
            operand_type = rhs_type if lcat is None else lhs_type  # the actual operand
            if isinstance(node, (PrefixOp, PostfixOp)):
                if operand_type is None:
                    # auto: infer as int (e.g. ++auto_var)
                    return IntType()
                if type_of(operand_type) != "int":
                    raise TypeMismatchInExpression(node)
                if op != "!" and self._is_int_constant_expr(operand_type):
                    raise TypeMismatchInExpression(node)
                return IntType()
            # Binary: both sides exist
            if lcat is not None and lcat != "int":
                if rcat is None:
                    raise TypeCannotBeInferred(node)
                raise TypeMismatchInExpression(node)
            if rcat is not None and rcat != "int":
                if lcat is None:
                    raise TypeCannotBeInferred(node)
                raise TypeMismatchInExpression(node)
            return IntType()

        # --- numeric arithmetic ops: +, -, *, / ---
        if op in NUMERIC_OPS:
            if isinstance(node, PrefixOp):
                # Unary +, -
                ocat = rcat if lcat is None else lcat
                if ocat is None:
                    raise TypeCannotBeInferred(node)
                if not is_numeric(ocat):
                    raise TypeMismatchInExpression(node)
                return to_formal(rhs_type) if lcat is None else to_formal(lhs_type)
            # Binary
            if lcat is None:
                if not isinstance(rhs_type, IntLiteral):
                    raise TypeCannotBeInferred(node)
                return to_formal(rhs_type)
            if rcat is None:
                if not isinstance(lhs_type, IntLiteral):
                    raise TypeCannotBeInferred(node)
                return to_formal(lhs_type)
            if not is_numeric(lcat) or not is_numeric(rcat):
                raise TypeMismatchInExpression(node)
            return FloatType() if lcat == "float" or rcat == "float" else IntType()

        # --- relational ops ---
        if op in RELATIONAL_OPS:
            if lcat is None or rcat is None:
                raise TypeCannotBeInferred(node)
            if not is_numeric(lcat) or not is_numeric(rcat):
                raise TypeMismatchInExpression(node)
            return IntType()

        raise TypeMismatchInExpression(node)


    def _is_constant_expr(self, node):
        """Check if an AST expression is a compile-time constant (literals and const operators)."""
        if isinstance(node, (IntLiteral, FloatLiteral, StringLiteral)):
            return node
        if isinstance(node, BinaryOp):
            return self._check_op(node, self._is_constant_expr(node.left), 
                                  node.operator, self._is_constant_expr(node.right)) 
        if isinstance(node, PrefixOp) and node.operator not in ('++', '--'):
            return self._is_constant_expr(node.operand)
        return None


    def _is_int_constant_expr(self, node):
        """Check if an AST expression is a compile-time constant (only literals and non-mutating operators)."""
        const_expr = self._is_constant_expr(node)
        return True if const_expr and isinstance(const_expr, (IntLiteral, IntType)) else False
    

    # -----------------------------------------------------------------------
    # Program & declarations
    # -----------------------------------------------------------------------

    def visit_program(self, node: "Program", o: Any = None):
        # First pass: register all top-level names (detect redeclaration early)
        for decl in node.decls:
            if isinstance(decl, StructDecl):
                if decl.name in self.env.structs:
                    raise Redeclared("Struct", decl.name)
            elif isinstance(decl, FuncDecl):
                if decl.name in self.env.funcs:
                    raise Redeclared("Function", decl.name)
                self.env.funcs[decl.name] = decl
            # Visit the declaration
            self.visit(decl, self.env)
            # Register struct members after visiting (so self-referencing structs fail)
            if isinstance(decl, StructDecl):
                self.env.structs[decl.name] = decl.members

        # Ensure a main function of void type exists
        main_func = self.env.funcs.get("main")
        if not main_func or not isinstance(main_func.return_type, VoidType) or len(main_func.params) != 0:
            raise UndeclaredFunction("main")

    def visit_struct_decl(self, node: "StructDecl", o: Any = None):
        o.sym.enter(node)
        for member in node.members:
            self.visit(member, o)
        o.sym.exit()

    def visit_member_decl(self, node: "MemberDecl", o: Any = None):
        if o.sym.declared_in_current(node.name):
            raise Redeclared("Member", node.name)
        self._validate_typed_declaration(node.member_type, node, o)
        o.sym.declare(node.name, node.member_type)

    def visit_func_decl(self, node: "FuncDecl", o: Any = None):
        self._ensure_declared_struct_type(node.return_type, o)
        o.sym.enter(node)
        for param in node.params:
            self.visit(param, o)
        # Track deferred self-recursive call assignments
        prev_deferred = getattr(self, '_deferred_self_calls', [])
        self._deferred_self_calls = []
        self.visit(node.body, o)
        # If return type was never set by a return statement, default to void
        if node.return_type is None:
            node.return_type = VoidType()
        # Process deferred self-recursive call assignments now that return type is known
        for var_node, declared_type in self._deferred_self_calls:
            if declared_type is None:
                # auto x = foo() -> resolve x's type from inferred return type
                if isinstance(node.return_type, VoidType):
                    raise TypeMismatchInStatement(var_node)
                o.sym.update_auto(var_node.name, node.return_type)
            else:
                # int x = foo() -> validate compatibility
                if not self._assignment_compatible(declared_type, node.return_type, o):
                    raise TypeMismatchInStatement(var_node)
        self._deferred_self_calls = prev_deferred
        o.sym.exit()

    def visit_param(self, node: "Param", o: Any = None):
        if o.sym.declared_in_current(node.name):
            raise Redeclared("Parameter", node.name)
        self._validate_typed_declaration(node.param_type, node, o)
        o.sym.declare(node.name, node.param_type)

    # -----------------------------------------------------------------------
    # Type nodes (pass-through)
    # -----------------------------------------------------------------------

    def visit_int_type(self, node: "IntType", o: Any = None):
        return node

    def visit_float_type(self, node: "FloatType", o: Any = None):
        return node

    def visit_string_type(self, node: "StringType", o: Any = None):
        return node

    def visit_void_type(self, node: "VoidType", o: Any = None):
        return node

    def visit_struct_type(self, node: "StructType", o: Any = None):
        return node

    # -----------------------------------------------------------------------
    # Statements
    # -----------------------------------------------------------------------

    def visit_block_stmt(self, node: "BlockStmt", o: Any = None):
        o.sym.enter(node)
        for stmt in node.statements:
            self.visit(stmt, o)

        self._check_unresolved_autos(o.sym.current_scope(), node)
        o.sym.exit()

    def visit_var_decl(self, node: "VarDecl", o: Any = None):
        # --- Redeclaration checks ---
        if o.sym.declared_in_current(node.name):
            raise Redeclared("Variable", node.name)
        func = o.sym.find_func()
        if func and any(p.name == node.name for p in func.params):
            raise Redeclared("Variable", node.name)

        # --- Type validity checks ---
        if isinstance(node.var_type, VoidType):
            raise TypeMismatchInStatement(node)
        self._ensure_declared_struct_type(node.var_type, o)

        declared_type = node.var_type  # None means auto

        if node.init_value is not None:
            init_type = self.visit(node.init_value, o)

            if declared_type is None:
                # auto with init
                if init_type is None:
                    # Self-recursive call: defer until return type is known
                    if self._is_self_call(node.init_value, o):
                        o.sym.declare(node.name, None)
                        self._deferred_self_calls.append((node, None))
                        return
                    raise TypeCannotBeInferred(node)
                if isinstance(init_type, StructLiteral):
                    raise TypeCannotBeInferred(node)
                if isinstance(init_type, VoidType):
                    raise TypeMismatchInStatement(node)
                declared_type = init_type
            else:
                # explicit type with init — check compatibility
                # Anchor autos inside struct literals before compatibility check
                if isinstance(node.init_value, StructLiteral) and isinstance(declared_type, StructType):
                    self._anchor_struct_literal(declared_type, node.init_value, o)
                # Self-recursive call with unresolved return: defer
                if init_type is None: 
                    # lhs = auto variable -> ok
                    if isinstance(node.init_value, Identifier):
                        init_type = declared_type
                        o.sym.update_auto(node.init_value.name, declared_type)
                    elif self._is_self_call(node.init_value, o):
                        o.sym.declare(node.name, declared_type)
                        self._deferred_self_calls.append((node, declared_type))
                        return
                if not self._assignment_compatible(declared_type, init_type, o, node.init_value):
                    if isinstance(node.init_value, StructLiteral) and isinstance(declared_type, StructType):
                        raise TypeMismatchInExpression(node.init_value)
                    raise TypeMismatchInStatement(node)

        o.sym.declare(node.name, declared_type)

    def visit_if_stmt(self, node: "IfStmt", o: Any = None):
        self._check_condition(node.condition, node, o)
        o.sym.enter(node)
        self.visit(node.then_stmt, o)
        o.sym.exit()
        if node.else_stmt:
            o.sym.enter(node)
            self.visit(node.else_stmt, o)
            o.sym.exit()

    def visit_while_stmt(self, node: "WhileStmt", o: Any = None):
        self._check_condition(node.condition, node, o)
        o.sym.enter(node)
        self.visit(node.body, o)
        o.sym.exit()

    def visit_for_stmt(self, node: "ForStmt", o: Any = None):
        if node.init:
            self.visit(node.init, o)
        if node.condition:
            self._check_condition(node.condition, node, o)
        if node.update:
            self.visit(node.update, o)
        # Body always gets its own scope so it can shadow for-init variables.
        o.sym.enter(node) 
        if isinstance(node.body, BlockStmt):
            self.visit(node.body, o)  # visit_block_stmt enters its own scope
        else:
            o.sym.enter(node.body)
            self.visit(node.body, o)
            o.sym.exit()
        self._check_unresolved_autos(o.sym.current_scope(), node)
        o.sym.exit()

    def visit_switch_stmt(self, node: "SwitchStmt", o: Any = None):
        self._check_condition(node.expr, node, o)
        o.sym.enter(node)
        for case in node.cases:
            self.visit(case, o)
        if node.default_case:
            self.visit(node.default_case, o)
        o.sym.exit()

    def visit_case_stmt(self, node: "CaseStmt", o: Any = None):
        expr_type = self.visit(node.expr, o)
        # Case expressions must be compile-time int constants
        if not self._is_int_constant_expr(node.expr):
            raise TypeMismatchInStatement(node)
        self._check_condition(expr_type, node, o)
        # Cases share the switch scope (no separate scope)
        for stmt in node.statements:
            self.visit(stmt, o)

    def visit_default_stmt(self, node: "DefaultStmt", o: Any = None):
        # Default shares the switch scope (no separate scope)
        for stmt in node.statements:
            self.visit(stmt, o)

    def visit_break_stmt(self, node: "BreakStmt", o: Any = None):
        if not o.sym.find_enclosing(WhileStmt, ForStmt, SwitchStmt):
            raise MustInLoop(node)

    def visit_continue_stmt(self, node: "ContinueStmt", o: Any = None):
        if not o.sym.find_enclosing(WhileStmt, ForStmt):
            raise MustInLoop(node)

    def visit_return_stmt(self, node: "ReturnStmt", o: Any = None):
        func = o.sym.find_func()
        o.sym.enter(node)  # for resolving autos in return expression
        ret_type = self.visit(node.expr, o) if node.expr else VoidType()
        ret_type = to_formal(ret_type) if ret_type is not None else None
        o.sym.exit()

        # Handle auto return expression
        if ret_type is None:
            if func.return_type is not None and isinstance(node.expr, Identifier):
                o.sym.update_auto(node.expr.name, func.return_type)
                ret_type = func.return_type
            else:
                raise TypeCannotBeInferred(node)

        # "return <void_expr>" is never valid — void functions must use bare "return;"
        if node.expr is not None and isinstance(ret_type, VoidType):
            if func.return_type is None:
                raise TypeCannotBeInferred(node)
            raise TypeMismatchInStatement(node)

        # Set inferred return type on first return
        if func.return_type is None:
            if isinstance(ret_type, StructLiteral):
                raise TypeCannotBeInferred(node)
            func.return_type = ret_type

        # Anchor autos in struct literal returns
        if isinstance(node.expr, StructLiteral) and isinstance(func.return_type, StructType):
            self._anchor_struct_literal(func.return_type, node.expr, o)

        # Check compatibility
        if isinstance(func.return_type, VoidType) and isinstance(ret_type, VoidType):
            pass  # void returning void is fine
        elif not self._assignment_compatible(func.return_type, ret_type, o):
            raise TypeMismatchInStatement(node)

    def visit_expr_stmt(self, node: "ExprStmt", o: Any = None):
        try:
            ret_type = self.visit(node.expr, o)
            if isinstance(node.expr, Identifier) and ret_type is None:
                # Unused auto variable in expression context: cannot infer
                raise TypeCannotBeInferred(node)
            if isinstance(node.expr, StructLiteral):
                for v in node.expr.values:
                    if isinstance(v, Identifier) and o.sym.lookup(v.name) is None:
                        # Unused auto variable in struct literal: cannot infer
                        raise TypeCannotBeInferred(node)
        except TypeMismatchInExpression as e:
            # Top-level assignment expression errors become statement errors
            if isinstance(node.expr, AssignExpr) and e.expr == node.expr:
                raise TypeMismatchInStatement(node)
            raise e

    # -----------------------------------------------------------------------
    # Expressions
    # -----------------------------------------------------------------------

    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        lhs = self.visit(node.left, o)
        rhs = self.visit(node.right, o)
        if isinstance(lhs, StructLiteral):
            raise TypeMismatchInExpression(node)
        if isinstance(rhs, StructLiteral):
            raise TypeMismatchInExpression(node)
        result = self._check_op(node, lhs, node.operator, rhs)
        self._anchor_auto(node.left, result, o)
        self._anchor_auto(node.right, result, o)
        return result

    def visit_prefix_op(self, node: "PrefixOp", o: Any = None):
        operand_type = self.visit(node.operand, o)
        if node.operator in ("++", "--"):
            if not isinstance(node.operand, (Identifier, MemberAccess)):
                raise TypeMismatchInExpression(node)
        result = self._check_op(node, None, node.operator, operand_type)
        self._anchor_auto(node.operand, result, o)
        return result

    def visit_postfix_op(self, node: "PostfixOp", o: Any = None):
        operand_type = self.visit(node.operand, o)
        if not isinstance(node.operand, (Identifier, MemberAccess)):
            raise TypeMismatchInExpression(node)
        result = self._check_op(node, operand_type, node.operator, None)
        self._anchor_auto(node.operand, result, o)
        return result

    def visit_assign_expr(self, node: "AssignExpr", o: Any = None):
        if not isinstance(node.lhs, (Identifier, MemberAccess)):
            raise TypeMismatchInExpression(node)

        rhs = self.visit(node.rhs, o)
        lhs = self.visit(node.lhs, o)

        lcat, rcat = type_of(lhs), type_of(rhs)

        # Both auto: cannot infer
        if lcat is None and rcat is None:
            raise TypeCannotBeInferred(node)

        if lcat is None:
            # auto = struct literal: cannot infer (no target type)
            if isinstance(rhs, StructLiteral):
                raise TypeCannotBeInferred(node)
            # auto = void: cannot infer
            elif rcat == "void":
                raise TypeCannotBeInferred(node)
            else:
                # auto = non-void literal/expression: infer from RHS
                result = to_formal(rhs)
        elif rcat is None:
            result = lhs
        else:
            # Both resolved: check compatibility
            if isinstance(node.rhs, StructLiteral) and isinstance(lhs, StructType):
                self._anchor_struct_literal(lhs, node.rhs, o)
            if not self._assignment_compatible(lhs, rhs, o, node.rhs):
                if isinstance(node.rhs, StructLiteral) and isinstance(lhs, StructType):
                    raise TypeMismatchInExpression(node.rhs)
                raise TypeMismatchInExpression(node)
            result = lhs

        self._anchor_auto(node.lhs, result, o)
        self._anchor_auto(node.rhs, result, o)
        return result

    def visit_member_access(self, node: "MemberAccess", o: Any = None):
        obj_type = self.visit(node.obj, o)
        if obj_type is None:
            if isinstance(node.obj, FuncCall) and self._is_self_call(node.obj, o):
                return None
            raise TypeCannotBeInferred(node)
        if isinstance(obj_type, StructLiteral):
            raise TypeMismatchInExpression(node)

        if isinstance(obj_type, StructType):
            members = o.structs.get(obj_type.struct_name)
            if members is None:
                raise UndeclaredStruct(obj_type.struct_name)

            for mem in members:
                if mem.name == node.member:
                    return mem.member_type

        raise TypeMismatchInExpression(node)

    def visit_func_call(self, node: "FuncCall", o: Any = None):
        func = o.funcs.get(node.name)
        if not func:
            raise UndeclaredFunction(node.name)
        if len(node.args) != len(func.params):
            raise TypeMismatchInExpression(node)
        # a function return itself but not have type yet -> cannot infer
        ret_node = o.sym.find_enclosing(ReturnStmt)
        if ret_node is not None and func.return_type is None: 
            raise TypeCannotBeInferred(ret_node)

        for arg, param in zip(node.args, func.params):
            arg_type = self.visit(arg, o)
            # Anchor autos inside struct literal arguments
            if isinstance(arg, StructLiteral) and isinstance(param.param_type, StructType):
                self._anchor_struct_literal(param.param_type, arg, o)

            # auto arg: infer from param type
            if type_of(arg_type) is None:
                # arg_type is None: arg not used yet
                # -> no value -> assign param_type to arg_type is valid
                self._anchor_auto(arg, param.param_type, o)
            elif isinstance(arg_type, StructLiteral):
                if not isinstance(param.param_type, StructType):
                    raise TypeMismatchInExpression(node)
                if not self._struct_literal_compatible(param.param_type, arg_type, o):
                    raise TypeMismatchInExpression(node)
            elif not types_match(param.param_type, arg_type):
                raise TypeMismatchInExpression(node)

        return func.return_type

    def visit_identifier(self, node: "Identifier", o: Any = None):
        result = o.sym.lookup(node.name)
        if result is ...:
            raise UndeclaredIdentifier(node.name)
        return result  # may be None (auto, unresolved)

    def visit_struct_literal(self, node: "StructLiteral", o: Any = None):
        visited = [self.visit(v, o) for v in node.values]
        visited = [self.visit(v, o) for v in node.values]
        return StructLiteral(visited)

    # -----------------------------------------------------------------------
    # Literals
    # -----------------------------------------------------------------------

    def visit_int_literal(self, node: "IntLiteral", o: Any = None):
        return node

    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        return node

    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        return node
