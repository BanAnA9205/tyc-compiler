"""
Code generator for TyC.
"""

from typing import Any

from ..utils.nodes import *
from ..utils.visitor import BaseVisitor
from .emitter import *
from .frame import *
from .io import IO_SYMBOL_LIST
from .utils import *


class StringArrayType:
    """Marker type for JVM main(String[] args)."""
    pass



class MockFrame:
    def push(self): pass
    def pop(self): pass

class CodeGenerator(BaseVisitor):

    def _infer_function_return_type(self, node: FuncDecl):
        if node.return_type:
            return node.return_type
        def find_return_type(stmt):
            from src.utils.nodes import ReturnStmt, BlockStmt, IfStmt
            if isinstance(stmt, ReturnStmt):
                if stmt.expr:
                    syms = []
                    for p in node.params:
                        syms.append(Symbol(p.name, p.param_type, Index(0)))
                    return self._infer_type(stmt.expr, Access(None, syms))
                return VoidType()
            if isinstance(stmt, BlockStmt):
                for s in stmt.statements:
                    rt = find_return_type(s)
                    if rt: return rt
            if isinstance(stmt, IfStmt):
                rt = find_return_type(stmt.then_stmt)
                if rt: return rt
                if stmt.else_stmt:
                    rt = find_return_type(stmt.else_stmt)
                    if rt: return rt
            if hasattr(stmt, 'body'):
                rt = find_return_type(stmt.body)
                if rt: return rt
            return None
        inferred = find_return_type(node.body)
        return inferred if inferred else VoidType()


    """Minimal AST -> Jasmin code generator."""

    def __init__(self):
        self.emit = None
        self.functions = {}
        self.structs = {}   # name -> StructDecl node
        self.current_return_type = VoidType()
        self.class_name = "TyC"

    def _lookup_symbol(self, name: str, sym_list: list[Symbol]) -> Symbol:
        for sym in reversed(sym_list):
            if sym.name == name:
                return sym
        raise RuntimeError(f"Undeclared symbol: {name}")

    def _infer_type(self, node: Expr, o: Access):
        if isinstance(node, IntLiteral):
            return IntType()
        if isinstance(node, FloatLiteral):
            return FloatType()
        if isinstance(node, StringLiteral):
            return StringType()
        if isinstance(node, StructLiteral):
            if o is None or not hasattr(o, 'expected_type') or o.expected_type is None:
                raise RuntimeError("Struct literal needs expected type in codegen")
            return o.expected_type
        if isinstance(node, Identifier):
            return self._lookup_symbol(node.name, o.sym).type
        if isinstance(node, AssignExpr):
            return self._infer_type(node.rhs, o)
        if isinstance(node, FuncCall):
            return self.functions[node.name].type.return_type
        if isinstance(node, BinaryOp):
            if node.operator in ["+", "-", "*", "/", "%"]:
                left_type = self._infer_type(node.left, o)
                right_type = self._infer_type(node.right, o)
                if is_float_type(left_type) or is_float_type(right_type):
                    return FloatType()
                return IntType()
            if node.operator in ["<", "<=", ">", ">=", "==", "!="]:
                return IntType()
        return IntType()

    def visit_program(self, node: Program, o: Any = None):
        self.emit = Emitter(f"{self.class_name}.j")
        self.emit.print_out(self.emit.emit_prolog(self.class_name))

        for io_sym in IO_SYMBOL_LIST:
            self.functions[io_sym.name] = io_sym

        # First pass: register all struct declarations and emit their class files
        for decl in node.decls:
            if isinstance(decl, StructDecl):
                self.visit(decl, None)

        # Second pass: register all function signatures
        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                return_type = self._infer_function_return_type(decl)
                param_types = [p.param_type for p in decl.params]
                self.functions[decl.name] = Symbol(
                    decl.name, FunctionType(param_types, return_type), CName(self.class_name)
                )

        # Third pass: generate code for all functions
        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                self.visit(decl, None)

        self.emit.emit_epilog()

    def visit_func_decl(self, node: FuncDecl, o: Any = None):
        self.current_return_type = self._infer_function_return_type(node)
        frame = Frame(node.name, self.current_return_type)
        frame.enter_scope(True)

        if node.name == "main":
            mtype = FunctionType([StringArrayType()], VoidType())
        else:
            mtype = FunctionType([p.param_type for p in node.params], self.current_return_type)

        self.emit.print_out(self.emit.emit_method(node.name, mtype, True))

        start_label = frame.get_start_label()
        end_label = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))

        local_syms: list[Symbol] = []
        if node.name == "main":
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", StringArrayType(), start_label, end_label
                )
            )

        for param in node.params:
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(idx, param.name, param.param_type, start_label, end_label)
            )
            local_syms.append(Symbol(param.name, param.param_type, Index(idx)))

        sub_body = SubBody(frame, local_syms)
        self.visit(node.body, sub_body)

        if is_void_type(self.current_return_type):
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))
        elif is_int_type(self.current_return_type):
            self.emit.print_out(self.emit.emit_push_iconst(0, frame))
            self.emit.print_out(self.emit.emit_return(IntType(), frame))
        elif is_float_type(self.current_return_type):
            self.emit.print_out(self.emit.emit_push_fconst("0.0", frame))
            self.emit.print_out(self.emit.emit_return(FloatType(), frame))
        else:
            self.emit.print_out(self.emit.emit_push_iconst(0, frame))
            self.emit.print_out(self.emit.emit_return(self.current_return_type, frame))

        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_scope()
        self.emit.print_out(self.emit.emit_end_method(frame))

    def visit_block_stmt(self, node: BlockStmt, o: SubBody = None):
        o.frame.enter_scope(False)
        start_label = o.frame.get_start_label()
        end_label = o.frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_label, o.frame))
        
        new_sym = list(o.sym)
        new_o = SubBody(o.frame, new_sym)
        for stmt in node.statements:
            self.visit(stmt, new_o)
            
        self.emit.print_out(self.emit.emit_label(end_label, o.frame))
        o.frame.exit_scope()
        return o

    def visit_var_decl(self, node: VarDecl, o: SubBody = None):
        frame = o.frame
        idx = frame.get_new_index()
        var_type = node.var_type if node.var_type else self._infer_type(node.init_value, Access(frame, o.sym))
        self.emit.print_out(
            self.emit.emit_var(
                idx, node.name, var_type, frame.get_start_label(), frame.get_end_label()
            )
        )
        if node.init_value is not None:
            acc = Access(frame, o.sym); acc.expected_type = var_type; rhs_code, _ = self.visit(node.init_value, acc)
            self.emit.print_out(rhs_code)
            self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
        else:
            if is_struct_type(var_type):
                init_code = self.emit.emit_new_instance(var_type.struct_name, frame)
                self.emit.print_out(init_code)
                self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
        o.sym.append(Symbol(node.name, var_type, Index(idx)))
        return o

    def visit_expr_stmt(self, node: ExprStmt, o: SubBody = None):
        code, expr_type = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        if not is_void_type(expr_type):
            self.emit.print_out(self.emit.emit_pop(o.frame))
        return o

    def visit_if_stmt(self, node: IfStmt, o: SubBody = None):
        frame = o.frame
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        else_label = frame.get_new_label()
        end_label = frame.get_new_label()
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(else_label, frame))
        self.visit(node.then_stmt, SubBody(frame, list(o.sym)))
        self.emit.print_out(self.emit.emit_goto(end_label, frame))
        self.emit.print_out(self.emit.emit_label(else_label, frame))
        if node.else_stmt:
            self.visit(node.else_stmt, SubBody(frame, list(o.sym)))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_while_stmt(self, node: WhileStmt, o: SubBody = None):
        frame = o.frame
        frame.enter_loop()
        start_label = frame.get_continue_label()
        end_label = frame.get_break_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(end_label, frame))
        self.visit(node.body, SubBody(frame, list(o.sym)))
        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_loop()
        return o

    def visit_return_stmt(self, node: ReturnStmt, o: SubBody = None):
        if node.expr is None:
            self.emit.print_out(self.emit.emit_return(VoidType(), o.frame))
            return o
        acc = Access(o.frame, o.sym); acc.expected_type = getattr(self, "current_return_type", None); code, ret_type = self.visit(node.expr, acc)
        self.emit.print_out(code)
        self.emit.print_out(self.emit.emit_return(ret_type, o.frame))
        return o

    def visit_binary_op(self, node: BinaryOp, o: Access = None):
        left_code, left_type = self.visit(node.left, o)
        right_code, right_type = self.visit(node.right, o)
        frame = o.frame

        if node.operator in ["+", "-", "*", "/", "<", "<=", ">", ">=", "==", "!="]:
            if is_float_type(left_type) or is_float_type(right_type):
                if is_int_type(left_type):
                    left_code += self.emit.emit_i2f(frame)
                if is_int_type(right_type):
                    right_code += self.emit.emit_i2f(frame)
                op_type = FloatType()
            else:
                op_type = IntType()
                
            if node.operator in ["+", "-"]:
                return left_code + right_code + self.emit.emit_add_op(node.operator, op_type, frame), op_type
            if node.operator in ["*", "/"]:
                return left_code + right_code + self.emit.emit_mul_op(node.operator, op_type, frame), op_type
            if node.operator in ["<", "<=", ">", ">=", "==", "!="]:
                return left_code + right_code + self.emit.emit_re_op(node.operator, op_type, frame), IntType()
        
        if node.operator == "&&":
            false_label = frame.get_new_label()
            end_label = frame.get_new_label()
            
            code = left_code
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_re_op("==", IntType(), frame)
            code += self.emit.emit_if_true(false_label, frame)
            
            code += right_code
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_re_op("==", IntType(), frame)
            code += self.emit.emit_if_true(false_label, frame)
            
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_goto(end_label, frame)
            code += self.emit.emit_label(false_label, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_label(end_label, frame)
            return code, IntType()

        if node.operator == "||":
            true_label = frame.get_new_label()
            end_label = frame.get_new_label()
            
            code = left_code
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_re_op("!=", IntType(), frame)
            code += self.emit.emit_if_true(true_label, frame)
            
            code += right_code
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_re_op("!=", IntType(), frame)
            code += self.emit.emit_if_true(true_label, frame)
            
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_goto(end_label, frame)
            code += self.emit.emit_label(true_label, frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_label(end_label, frame)
            return code, IntType()
        if node.operator == "%":
            return left_code + right_code + self.emit.emit_mod(frame), IntType()
        raise RuntimeError(f"Unsupported operator: {node.operator}")

    def visit_assign_expr(self, node: AssignExpr, o: Access = None):
        if isinstance(node.lhs, Identifier):
            lhs_sym = self._lookup_symbol(node.lhs.name, o.sym)
            acc = Access(o.frame, o.sym); acc.expected_type = lhs_sym.type; rhs_code, rhs_type = self.visit(node.rhs, acc)
            idx = lhs_sym.value.value
            code = rhs_code + self.emit.emit_dup(o.frame) + self.emit.emit_write_var(
                node.lhs.name, lhs_sym.type, idx, o.frame
            )
            return code, rhs_type
        if isinstance(node.lhs, MemberAccess):
            obj_code, obj_type = self.visit(node.lhs.obj, o)
            struct_decl = self.structs[obj_type.struct_name]
            member_name = node.lhs.member
            member_decl = next(m for m in struct_decl.members if m.name == member_name)
            member_type = member_decl.member_type
            field_lexeme = f"{obj_type.struct_name}/{member_name}"

            acc = Access(o.frame, o.sym); acc.expected_type = member_type; rhs_code, rhs_type = self.visit(node.rhs, acc)
            code = obj_code
            code += rhs_code
            code += self.emit.emit_dup_x1(o.frame)
            code += self.emit.emit_put_field(field_lexeme, member_type, o.frame)
            return code, rhs_type
        raise RuntimeError("Assignment only supports identifier or member access")

    def visit_func_call(self, node: FuncCall, o: Access = None):
        frame = o.frame
        fn_sym = self.functions[node.name]
        fn_type = fn_sym.type
        code = ""
        for arg in node.args:
            arg_code, _ = self.visit(arg, o)
            code += arg_code
        code += self.emit.emit_invoke_static(f"{fn_sym.value.value}/{node.name}", fn_type, frame)
        return code, fn_type.return_type

    def visit_identifier(self, node: Identifier, o: Access = None):
        sym = self._lookup_symbol(node.name, o.sym)
        return self.emit.emit_read_var(node.name, sym.type, sym.value.value, o.frame), sym.type

    def visit_int_literal(self, node: IntLiteral, o: Access = None):
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: FloatLiteral, o: Access = None):
        return self.emit.emit_push_fconst(str(node.value), o.frame), FloatType()

    def visit_string_literal(self, node: StringLiteral, o: Access = None):
        return self.emit.emit_push_const(node.value, StringType(), o.frame), StringType()

    def visit_struct_decl(self, node: StructDecl, o: Any = None):
        # Register the struct so MemberAccess / StructLiteral can look it up
        self.structs[node.name] = node

        # Each struct becomes its own Jasmin class file
        struct_emit = Emitter(f"{node.name}.j")
        struct_emit.print_out(struct_emit.emit_prolog(node.name))

        # Emit one public field per member
        for member in node.members:
            struct_emit.print_out(struct_emit.emit_field(member.name, member.member_type))

        # Emit a custom constructor that initializes struct fields
        c_code = ""
        c_code += struct_emit.jvm.emitMETHOD("<init>", "()V", False)
        c_code += struct_emit.jvm.emitLIMITSTACK(3)
        c_code += struct_emit.jvm.emitLIMITLOCAL(1)
        c_code += struct_emit.jvm.emitALOAD(0)
        c_code += struct_emit.jvm.emitINVOKESPECIAL()
        
        for m in node.members:
            if is_struct_type(m.member_type):
                c_code += struct_emit.jvm.emitALOAD(0)
                c_code += struct_emit.emit_new_instance(m.member_type.struct_name, MockFrame())
                c_code += struct_emit.emit_put_field(f"{node.name}/{m.name}", m.member_type, MockFrame())
                
        c_code += struct_emit.jvm.emitRETURN()
        c_code += struct_emit.jvm.emitENDMETHOD()
        struct_emit.print_out(c_code)

        struct_emit.emit_epilog()

    def visit_member_decl(self, node: MemberDecl, o: Any = None):
        # Member declarations are fully handled inside visit_struct_decl;
        # this visitor is kept as a no-op for completeness.
        return None

    def visit_param(self, node: Param, o: Any = None):
        # Parameters are handled inline in visit_func_decl.
        return None

    def visit_int_type(self, node: IntType, o: Any = None):
        return node

    def visit_float_type(self, node: FloatType, o: Any = None):
        return node

    def visit_string_type(self, node: StringType, o: Any = None):
        return node

    def visit_void_type(self, node: VoidType, o: Any = None):
        return node

    def visit_struct_type(self, node: StructType, o: Any = None):
        return node

    def visit_for_stmt(self, node: ForStmt, o: Any = None):
        frame = o.frame

        # init, condition, and update use the outer scope `o` directly
        if node.init:
            if isinstance(node.init, (VarDecl, ExprStmt)):
                self.visit(node.init, o)
            else:
                init_code, init_type = self.visit(node.init, Access(frame, o.sym))
                self.emit.print_out(init_code)
                if not is_void_type(init_type):
                    self.emit.print_out(self.emit.emit_pop(frame))

        frame.enter_loop()
        cond_label = frame.get_new_label()
        continue_label = frame.get_continue_label()
        break_label = frame.get_break_label()

        self.emit.print_out(self.emit.emit_label(cond_label, frame))
        if node.condition:
            cond_code, _ = self.visit(node.condition, Access(frame, o.sym))
            self.emit.print_out(cond_code)
            self.emit.print_out(self.emit.emit_if_false(break_label, frame))

        # The body gets its own isolated scope
        self.visit(node.body, SubBody(frame, list(o.sym)))

        self.emit.print_out(self.emit.emit_label(continue_label, frame))
        if node.update:
            update_code, update_type = self.visit(node.update, Access(frame, o.sym))
            self.emit.print_out(update_code)
            if not is_void_type(update_type):
                self.emit.print_out(self.emit.emit_pop(frame))

        self.emit.print_out(self.emit.emit_goto(cond_label, frame))
        self.emit.print_out(self.emit.emit_label(break_label, frame))
        frame.exit_loop()
        return o

    def visit_switch_stmt(self, node: SwitchStmt, o: Any = None):
        frame = o.frame
        break_label = frame.get_new_label()
        frame.brk_label.append(break_label)

        switch_code, _ = self.visit(node.expr, Access(frame, o.sym))
        switch_idx = frame.get_new_index()
        self.emit.print_out(switch_code)
        self.emit.print_out(self.emit.emit_write_var("$switch", IntType(), switch_idx, frame))

        case_labels = [frame.get_new_label() for _ in node.cases]
        default_label = frame.get_new_label() if node.default_case else break_label

        # Create switch scope and pre-allocate variables with default values
        new_sym = list(o.sym)
        new_o = SubBody(frame, new_sym)
        
        # Pre-pass: allocate local variables for all cases
        all_stmts = []
        for case in node.cases:
            all_stmts.extend(case.statements)
        if node.default_case:
            all_stmts.extend(node.default_case.statements)
            
        for stmt in all_stmts:
            if isinstance(stmt, VarDecl):
                idx = frame.get_new_index()
                var_type = stmt.var_type if stmt.var_type else self._infer_type(stmt.init_value, Access(frame, new_sym))
                new_sym.append(Symbol(stmt.name, var_type, Index(idx)))
                
                # Emit default value
                if is_int_type(var_type):
                    self.emit.print_out(self.emit.emit_push_iconst(0, frame))
                elif is_float_type(var_type):
                    self.emit.print_out(self.emit.emit_push_fconst("0.0", frame))
                elif is_string_type(var_type):
                    self.emit.print_out(self.emit.emit_push_const('""', StringType(), frame))
                elif is_struct_type(var_type):
                    self.emit.print_out(self.emit.emit_new_instance(var_type.struct_name, frame))
                
                self.emit.print_out(self.emit.emit_write_var(stmt.name, var_type, idx, frame))

        for case, case_label in zip(node.cases, case_labels):
            self.emit.print_out(self.emit.emit_read_var("$switch", IntType(), switch_idx, frame))
            case_code, _ = self.visit(case.expr, Access(frame, o.sym))
            self.emit.print_out(case_code)
            self.emit.print_out(self.emit.emit_re_op("==", IntType(), frame))
            self.emit.print_out(self.emit.emit_if_true(case_label, frame))

        self.emit.print_out(self.emit.emit_goto(default_label, frame))

        for case, case_label in zip(node.cases, case_labels):
            self.emit.print_out(self.emit.emit_label(case_label, frame))
            for stmt in case.statements:
                if isinstance(stmt, VarDecl):
                    if stmt.init_value:
                        idx = next(s.value.value for s in reversed(new_sym) if s.name == stmt.name)
                        var_type = next(s.type for s in reversed(new_sym) if s.name == stmt.name)
                        acc = Access(frame, new_sym); acc.expected_type = var_type
                        rhs_code, _ = self.visit(stmt.init_value, acc)
                        self.emit.print_out(rhs_code)
                        self.emit.print_out(self.emit.emit_write_var(stmt.name, var_type, idx, frame))
                else:
                    self.visit(stmt, new_o)

        if node.default_case:
            self.emit.print_out(self.emit.emit_label(default_label, frame))
            for stmt in node.default_case.statements:
                if isinstance(stmt, VarDecl):
                    if stmt.init_value:
                        idx = next(s.value.value for s in reversed(new_sym) if s.name == stmt.name)
                        var_type = next(s.type for s in reversed(new_sym) if s.name == stmt.name)
                        acc = Access(frame, new_sym); acc.expected_type = var_type
                        rhs_code, _ = self.visit(stmt.init_value, acc)
                        self.emit.print_out(rhs_code)
                        self.emit.print_out(self.emit.emit_write_var(stmt.name, var_type, idx, frame))
                else:
                    self.visit(stmt, new_o)

        self.emit.print_out(self.emit.emit_label(break_label, frame))
        frame.brk_label.pop()
        return o

    def visit_case_stmt(self, node: CaseStmt, o: Any = None):
        for stmt in node.statements:
            self.visit(stmt, o)
        return o

    def visit_default_stmt(self, node: DefaultStmt, o: Any = None):
        for stmt in node.statements:
            self.visit(stmt, o)
        return o

    def visit_break_stmt(self, node: BreakStmt, o: Any = None):
        self.emit.print_out(self.emit.emit_goto(o.frame.get_break_label(), o.frame))
        return o

    def visit_continue_stmt(self, node: ContinueStmt, o: Any = None):
        self.emit.print_out(self.emit.emit_goto(o.frame.get_continue_label(), o.frame))
        return o

    def visit_prefix_op(self, node: PrefixOp, o: Any = None):
        frame = o.frame
        if node.operator in ["+", "-"]:
            code, expr_type = self.visit(node.operand, o)
            if node.operator == "+":
                return code, expr_type
            return code + self.emit.emit_neg_op(expr_type, frame), expr_type
        if node.operator == "!":
            code, _ = self.visit(node.operand, o)
            return code + self.emit.emit_push_iconst(0, frame) + self.emit.emit_re_op("==", IntType(), frame), IntType()
        if node.operator in ["++", "--"]:
            if isinstance(node.operand, Identifier):
                sym = self._lookup_symbol(node.operand.name, o.sym)
                idx = sym.value.value
                load_code = self.emit.emit_read_var(node.operand.name, sym.type, idx, frame)
                one_code = self.emit.emit_push_iconst(1, frame)
                op_code = self.emit.emit_add_op(
                    "+" if node.operator == "++" else "-", sym.type, frame
                )
                write_code = self.emit.emit_write_var(node.operand.name, sym.type, idx, frame)
                dup_code = self.emit.emit_dup(frame)
                return load_code + one_code + op_code + dup_code + write_code, sym.type
            if isinstance(node.operand, MemberAccess):
                obj_code, obj_type = self.visit(node.operand.obj, o)
                struct_decl = self.structs[obj_type.struct_name]
                member_name = node.operand.member
                member_decl = next(m for m in struct_decl.members if m.name == member_name)
                member_type = member_decl.member_type
                field_lexeme = f"{obj_type.struct_name}/{member_name}"

                code = obj_code
                code += self.emit.emit_dup(frame)
                code += self.emit.emit_get_field(field_lexeme, member_type, frame)
                code += self.emit.emit_push_iconst(1, frame)
                code += self.emit.emit_add_op(
                    "+" if node.operator == "++" else "-", member_type, frame
                )
                code += self.emit.emit_dup_x1(frame)
                code += self.emit.emit_put_field(field_lexeme, member_type, frame)
                return code, member_type
        raise RuntimeError(f"Unsupported prefix operator: {node.operator}")

    def visit_postfix_op(self, node: PostfixOp, o: Any = None):
        frame = o.frame
        if isinstance(node.operand, Identifier):
            sym = self._lookup_symbol(node.operand.name, o.sym)
            idx = sym.value.value
            load_code = self.emit.emit_read_var(node.operand.name, sym.type, idx, frame)
            dup_code = self.emit.emit_dup(frame)
            one_code = self.emit.emit_push_iconst(1, frame)
            op_code = self.emit.emit_add_op(
                "+" if node.operator == "++" else "-", sym.type, frame
            )
            write_code = self.emit.emit_write_var(node.operand.name, sym.type, idx, frame)
            return load_code + dup_code + one_code + op_code + write_code, sym.type
        if isinstance(node.operand, MemberAccess):
            obj_code, obj_type = self.visit(node.operand.obj, o)
            struct_decl = self.structs[obj_type.struct_name]
            member_name = node.operand.member
            member_decl = next(m for m in struct_decl.members if m.name == member_name)
            member_type = member_decl.member_type
            field_lexeme = f"{obj_type.struct_name}/{member_name}"

            code = obj_code
            code += self.emit.emit_dup(frame)
            code += self.emit.emit_get_field(field_lexeme, member_type, frame)
            code += self.emit.emit_dup_x1(frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_add_op(
                "+" if node.operator == "++" else "-", member_type, frame
            )
            code += self.emit.emit_put_field(field_lexeme, member_type, frame)
            return code, member_type
        raise RuntimeError("PostfixOp only supports identifier or member access")

    def visit_member_access(self, node: MemberAccess, o: Any = None):
        obj_code, obj_type = self.visit(node.obj, o)
        struct_decl = self.structs[obj_type.struct_name]
        member_decl = next(m for m in struct_decl.members if m.name == node.member)
        member_type = member_decl.member_type
        field_lexeme = f"{obj_type.struct_name}/{node.member}"
        code = obj_code + self.emit.emit_get_field(field_lexeme, member_type, o.frame)
        return code, member_type

    def visit_struct_literal(self, node: StructLiteral, o: Any = None):
        frame = o.frame
        struct_type = self._infer_type(node, o)
        struct_decl = self.structs[struct_type.struct_name]

        code = self.emit.emit_new_instance(struct_type.struct_name, frame)
        for member, value in zip(struct_decl.members, node.values):
            code += self.emit.emit_dup(frame)
            acc = Access(frame, o.sym); acc.expected_type = member.member_type; value_code, _ = self.visit(value, acc)
            code += value_code
            field_lexeme = f"{struct_type.struct_name}/{member.name}"
            code += self.emit.emit_put_field(field_lexeme, member.member_type, frame)
        return code, struct_type
