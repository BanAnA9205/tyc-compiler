"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from ast import UnaryOp
from functools import reduce
from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *


class ASTGeneration(TyCVisitor):
    """AST Generation visitor for TyC language."""
    
    # Visit a parse tree produced by TyCParser#program.
    def visitProgram(self, ctx: TyCParser.ProgramContext):
        """Visit the program node and generate the AST."""
        
        # note: there is an <EOF> token at the end of the children list
        decls = [self.visit(decl_ctx) for decl_ctx in ctx.getChildren() if decl_ctx.getText() != "<EOF>"]

        return Program(decls)


    # Visit a parse tree produced by TyCParser#expr.
    def visitExpr(self, ctx:TyCParser.ExprContext):
        if ctx.LB(): # LB expr_list? RB
            if ctx.expr_list():
                elements = self.visit(ctx.expr_list())
                return StructLiteral(elements)
            else:
                return StructLiteral([])

        elif ctx.LP():                      # LP expr RP
            return self.visit(ctx.expr(0))
        
        elif ctx.INT_LIT():                 # INT_LIT | FLOAT_LIT | STRING_LIT 
            return IntLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())  

        elif ctx.MEM_ACC():                 # expr MEM_ACC ID
            return MemberAccess(self.visit(ctx.expr(0)), ctx.ID().getText())

        elif ctx.ID():                      # ID (note: since both ID and MEM_ACC, 
                                            # ID can be present, we check MEM_ACC first)
            return Identifier(ctx.ID().getText())
        
        elif ctx.func_call():               # func_call
            return self.visit(ctx.func_call())

        # from here on, it's either 3 or 2 children, 
        # at least 1 expr and 0 BS
        child_cnt = ctx.getChildCount() 

        if child_cnt == 2:
            # expr (INC_OP | DEC_OP)
            # | <assoc=right> (INC_OP | DEC_OP) expr
            # | <assoc=right> (LO_NOT | SUB_OP | ADD_OP) expr
            is_postfix = isinstance(ctx.getChild(0), TyCParser.ExprContext)

            if is_postfix:
                operand = self.visit(ctx.expr(0))
                op = ctx.getChild(1).getText()
                return PostfixOp(op, operand)
            else:
                op = ctx.getChild(0).getText()
                operand = self.visit(ctx.expr(0))
                return PrefixOp(op, operand)
            
        elif child_cnt == 3:
            if ctx.ASSIGN():
                # <assoc=right> expr ASSIGN expr
                lhs = self.visit(ctx.expr(0))
                rhs = self.visit(ctx.expr(1))

                return AssignExpr(lhs, rhs)

            # expr (MUL_OP | DIV_OP | MOD_OP) expr
            # | expr (ADD_OP | SUB_OP) expr
            # | expr (LESS_OP | LEQ_OP | GREAT_OP | GEQ_OP) expr
            # | expr (EQ_OP | NOTEQ_OP) expr
            # | expr LO_AND expr
            # | expr LO_OR expr
            left = self.visit(ctx.expr(0))
            op = ctx.getChild(1).getText()
            right = self.visit(ctx.expr(1))
            
            return BinaryOp(left, op, right)

    # Visit a parse tree produced by TyCParser#expr_list.
    def visitExpr_list(self, ctx:TyCParser.Expr_listContext):
        return [self.visit(expr_ctx) for expr_ctx in ctx.expr()]
        

    # Visit a parse tree produced by TyCParser#param.
    def visitParam(self, ctx:TyCParser.ParamContext):
        # (INT_KW | FLOAT_KW | STRING_KW | ID) ID
        name = ctx.getChild(1).getText()
        type = None

        if ctx.INT_KW():
            type = IntType()
        elif ctx.FLOAT_KW():
            type = FloatType()
        elif ctx.STRING_KW():
            type = StringType()
        else:
            type = StructType(ctx.getChild(0).getText())

        return Param(type, name)


    # Visit a parse tree produced by TyCParser#struct_decl.
    def visitStruct_decl(self, ctx:TyCParser.Struct_declContext):
        # struct_decl: STRUCT ID LB (param SEMICOLON)* RB SEMICOLON ;
        name = ctx.ID().getText()
        params = [self.visit(param_ctx) for param_ctx in ctx.param()]
        members = [MemberDecl(param.param_type, param.name) for param in params]
        return StructDecl(name, members)


    # Visit a parse tree produced by TyCParser#func_decl.
    def visitFunc_decl(self, ctx:TyCParser.Func_declContext):
        # func_decl: (INT_KW | FLOAT_KW | STRING_KW | ID | VOID)? 
        #            ID LP (param (COMMA param)*)? RP block_stmt ;
        return_type = None
        func_name = None

        if ctx.INT_KW():
            return_type = IntType()
        elif ctx.FLOAT_KW():
            return_type = FloatType()
        elif ctx.STRING_KW():
            return_type = StringType()
        elif ctx.VOID():
            return_type = VoidType()
        elif len(ctx.ID()) == 2: # return type is struct
            return_type = StructType(ctx.ID(0).getText())
            func_name = ctx.ID(1).getText() 

        if func_name is None:
            func_name = ctx.ID(0).getText()
        params = [self.visit(param_ctx) for param_ctx in ctx.param()]
        body = self.visit(ctx.block_stmt())

        return FuncDecl(return_type, func_name, params, body)

    # Visit a parse tree produced by TyCParser#func_call.
    def visitFunc_call(self, ctx:TyCParser.Func_callContext):
        # func_call: ID LP expr_list? RP ;
        func_name = ctx.ID().getText()
        args = [] if not ctx.expr_list() else self.visit(ctx.expr_list())

        return FuncCall(func_name, args)


    # Visit a parse tree produced by TyCParser#stmt.
    def visitStmt(self, ctx:TyCParser.StmtContext):
        if ctx.decl_stmt():
            return self.visit(ctx.decl_stmt())
        elif ctx.block_stmt():
            return self.visit(ctx.block_stmt())
        elif ctx.if_stmt():
            return self.visit(ctx.if_stmt())
        elif ctx.while_stmt():
            return self.visit(ctx.while_stmt())
        elif ctx.for_stmt():
            return self.visit(ctx.for_stmt())
        elif ctx.switch_stmt():
            return self.visit(ctx.switch_stmt())
        elif ctx.BREAK():
            return BreakStmt()
        elif ctx.CONTINUE():
            return ContinueStmt()
        elif ctx.RETURN():
            if ctx.expr():
                return ReturnStmt(self.visit(ctx.expr()))
            else:
                return ReturnStmt(None)
        else:
            return ExprStmt(self.visit(ctx.expr()))
        
    # Visit a parse tree produced by TyCParser#decl_stmt.
    def visitDecl_stmt(self, ctx:TyCParser.Decl_stmtContext):
        # decl_stmt: (INT_KW | FLOAT_KW | STRING_KW | ID | AUTO) 
        #            ID (ASSIGN expr)? SEMICOLON ;

        type = None # for auto
        var_name = None

        if ctx.INT_KW():
            type = IntType()
        elif ctx.FLOAT_KW():
            type = FloatType()
        elif ctx.STRING_KW():
            type = StringType()
        elif len(ctx.ID()) == 2:
            type = StructType(ctx.ID(0).getText())
            var_name = ctx.ID(1).getText()
        
        if var_name is None:
            var_name = ctx.ID(0).getText()

        init_value = self.visit(ctx.expr()) if ctx.expr() else None

        return VarDecl(type, var_name, init_value)

    # Visit a parse tree produced by TyCParser#block_stmt.
    def visitBlock_stmt(self, ctx:TyCParser.Block_stmtContext):
        # block_stmt: LB stmt* RB ;
        stmts = [self.visit(stmt_ctx) for stmt_ctx in ctx.stmt()]
        return BlockStmt(stmts)


    # Visit a parse tree produced by TyCParser#if_stmt.
    def visitIf_stmt(self, ctx:TyCParser.If_stmtContext):
        # if_stmt: IF LP expr RP stmt (ELSE stmt)? ;
        condition = self.visit(ctx.expr())
        then_branch, else_branch = None, None
        if ctx.ELSE():
            then_branch, else_branch = self.visit(ctx.stmt(0)), self.visit(ctx.stmt(1))
        else:
            then_branch = self.visit(ctx.stmt(0))

        return IfStmt(condition, then_branch, else_branch)

    # Visit a parse tree produced by TyCParser#while_stmt.
    def visitWhile_stmt(self, ctx:TyCParser.While_stmtContext):
        # while_stmt: WHILE LP expr RP stmt ;
        condition = self.visit(ctx.expr())
        body = self.visit(ctx.stmt())
        return WhileStmt(condition, body)


    # Visit a parse tree produced by TyCParser#for_init.
    def visitFor_init(self, ctx:TyCParser.For_initContext):
        # for_init: decl_stmt | expr SEMICOLON ;
        if ctx.decl_stmt():
            return self.visit(ctx.decl_stmt())
        return ExprStmt(self.visit(ctx.expr()))

    # Visit a parse tree produced by TyCParser#for_updt.
    def visitFor_updt(self, ctx:TyCParser.For_updtContext):
        # for_updt: expr ;
        return self.visit(ctx.expr())


    # Visit a parse tree produced by TyCParser#for_stmt.
    def visitFor_stmt(self, ctx:TyCParser.For_stmtContext):
        # for_stmt: FOR LP 
        #         (for_init | SEMICOLON)
        #         expr? SEMICOLON
        #         for_updt?
        #       RP 
        #   stmt ; 
        init, condition, update = None, None, None
        body = self.visit(ctx.stmt())

        if ctx.for_init():
            init = self.visit(ctx.for_init())
        if ctx.expr():
            condition = self.visit(ctx.expr())
        if ctx.for_updt():
            update = self.visit(ctx.for_updt())

        return ForStmt(init, condition, update, body)


    # Visit a parse tree produced by TyCParser#sw_case.
    def visitSw_case(self, ctx:TyCParser.Sw_caseContext):
        # sw_case: CASE expr COLON stmt* ;
        cond = self.visit(ctx.expr())
        stmts = [self.visit(stmt_ctx) for stmt_ctx in ctx.stmt()]
        return CaseStmt(cond, stmts)


    # Visit a parse tree produced by TyCParser#sw_def.
    def visitSw_def(self, ctx:TyCParser.Sw_defContext):
        # sw_def: DEFAULT COLON stmt* ;
        stmts = [self.visit(stmt_ctx) for stmt_ctx in ctx.stmt()]
        return DefaultStmt(stmts)


    # Visit a parse tree produced by TyCParser#switch_stmt.
    def visitSwitch_stmt(self, ctx:TyCParser.Switch_stmtContext):
        # switch_stmt: SWITCH LP expr RP LB sw_case* (sw_def sw_case*)? RB ;
        expr = self.visit(ctx.expr())
        cases = [self.visit(case_ctx) for case_ctx in ctx.sw_case()]
        default_case = self.visit(ctx.sw_def()) if ctx.sw_def() else None
        return SwitchStmt(expr, cases, default_case)