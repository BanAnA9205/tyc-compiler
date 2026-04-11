# Generated from /home/banana9205/Desktop/Main/Uni/PPL/tyc-compiler/src/grammar/TyC.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .TyCParser import TyCParser
else:
    from TyCParser import TyCParser

# This class defines a complete listener for a parse tree produced by TyCParser.
class TyCListener(ParseTreeListener):

    # Enter a parse tree produced by TyCParser#program.
    def enterProgram(self, ctx:TyCParser.ProgramContext):
        pass

    # Exit a parse tree produced by TyCParser#program.
    def exitProgram(self, ctx:TyCParser.ProgramContext):
        pass


    # Enter a parse tree produced by TyCParser#expr.
    def enterExpr(self, ctx:TyCParser.ExprContext):
        pass

    # Exit a parse tree produced by TyCParser#expr.
    def exitExpr(self, ctx:TyCParser.ExprContext):
        pass


    # Enter a parse tree produced by TyCParser#assign_expr.
    def enterAssign_expr(self, ctx:TyCParser.Assign_exprContext):
        pass

    # Exit a parse tree produced by TyCParser#assign_expr.
    def exitAssign_expr(self, ctx:TyCParser.Assign_exprContext):
        pass


    # Enter a parse tree produced by TyCParser#expr_list.
    def enterExpr_list(self, ctx:TyCParser.Expr_listContext):
        pass

    # Exit a parse tree produced by TyCParser#expr_list.
    def exitExpr_list(self, ctx:TyCParser.Expr_listContext):
        pass


    # Enter a parse tree produced by TyCParser#param.
    def enterParam(self, ctx:TyCParser.ParamContext):
        pass

    # Exit a parse tree produced by TyCParser#param.
    def exitParam(self, ctx:TyCParser.ParamContext):
        pass


    # Enter a parse tree produced by TyCParser#struct_decl.
    def enterStruct_decl(self, ctx:TyCParser.Struct_declContext):
        pass

    # Exit a parse tree produced by TyCParser#struct_decl.
    def exitStruct_decl(self, ctx:TyCParser.Struct_declContext):
        pass


    # Enter a parse tree produced by TyCParser#func_decl.
    def enterFunc_decl(self, ctx:TyCParser.Func_declContext):
        pass

    # Exit a parse tree produced by TyCParser#func_decl.
    def exitFunc_decl(self, ctx:TyCParser.Func_declContext):
        pass


    # Enter a parse tree produced by TyCParser#func_call.
    def enterFunc_call(self, ctx:TyCParser.Func_callContext):
        pass

    # Exit a parse tree produced by TyCParser#func_call.
    def exitFunc_call(self, ctx:TyCParser.Func_callContext):
        pass


    # Enter a parse tree produced by TyCParser#stmt.
    def enterStmt(self, ctx:TyCParser.StmtContext):
        pass

    # Exit a parse tree produced by TyCParser#stmt.
    def exitStmt(self, ctx:TyCParser.StmtContext):
        pass


    # Enter a parse tree produced by TyCParser#decl_stmt.
    def enterDecl_stmt(self, ctx:TyCParser.Decl_stmtContext):
        pass

    # Exit a parse tree produced by TyCParser#decl_stmt.
    def exitDecl_stmt(self, ctx:TyCParser.Decl_stmtContext):
        pass


    # Enter a parse tree produced by TyCParser#block_stmt.
    def enterBlock_stmt(self, ctx:TyCParser.Block_stmtContext):
        pass

    # Exit a parse tree produced by TyCParser#block_stmt.
    def exitBlock_stmt(self, ctx:TyCParser.Block_stmtContext):
        pass


    # Enter a parse tree produced by TyCParser#if_stmt.
    def enterIf_stmt(self, ctx:TyCParser.If_stmtContext):
        pass

    # Exit a parse tree produced by TyCParser#if_stmt.
    def exitIf_stmt(self, ctx:TyCParser.If_stmtContext):
        pass


    # Enter a parse tree produced by TyCParser#while_stmt.
    def enterWhile_stmt(self, ctx:TyCParser.While_stmtContext):
        pass

    # Exit a parse tree produced by TyCParser#while_stmt.
    def exitWhile_stmt(self, ctx:TyCParser.While_stmtContext):
        pass


    # Enter a parse tree produced by TyCParser#for_init.
    def enterFor_init(self, ctx:TyCParser.For_initContext):
        pass

    # Exit a parse tree produced by TyCParser#for_init.
    def exitFor_init(self, ctx:TyCParser.For_initContext):
        pass


    # Enter a parse tree produced by TyCParser#for_updt.
    def enterFor_updt(self, ctx:TyCParser.For_updtContext):
        pass

    # Exit a parse tree produced by TyCParser#for_updt.
    def exitFor_updt(self, ctx:TyCParser.For_updtContext):
        pass


    # Enter a parse tree produced by TyCParser#for_stmt.
    def enterFor_stmt(self, ctx:TyCParser.For_stmtContext):
        pass

    # Exit a parse tree produced by TyCParser#for_stmt.
    def exitFor_stmt(self, ctx:TyCParser.For_stmtContext):
        pass


    # Enter a parse tree produced by TyCParser#sw_case.
    def enterSw_case(self, ctx:TyCParser.Sw_caseContext):
        pass

    # Exit a parse tree produced by TyCParser#sw_case.
    def exitSw_case(self, ctx:TyCParser.Sw_caseContext):
        pass


    # Enter a parse tree produced by TyCParser#sw_def.
    def enterSw_def(self, ctx:TyCParser.Sw_defContext):
        pass

    # Exit a parse tree produced by TyCParser#sw_def.
    def exitSw_def(self, ctx:TyCParser.Sw_defContext):
        pass


    # Enter a parse tree produced by TyCParser#switch_stmt.
    def enterSwitch_stmt(self, ctx:TyCParser.Switch_stmtContext):
        pass

    # Exit a parse tree produced by TyCParser#switch_stmt.
    def exitSwitch_stmt(self, ctx:TyCParser.Switch_stmtContext):
        pass



del TyCParser