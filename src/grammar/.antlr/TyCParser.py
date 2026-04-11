# Generated from /home/banana9205/Desktop/Main/Uni/PPL/tyc-compiler/src/grammar/TyC.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,51,272,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,1,0,1,0,5,0,41,
        8,0,10,0,12,0,44,9,0,1,0,1,0,1,1,1,1,1,1,3,1,51,8,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,68,8,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,5,1,93,8,1,10,1,12,1,96,9,1,1,2,1,2,1,2,5,
        2,101,8,2,10,2,12,2,104,9,2,1,2,1,2,1,2,1,3,1,3,1,3,5,3,112,8,3,
        10,3,12,3,115,9,3,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,5,5,126,8,
        5,10,5,12,5,129,9,5,1,5,1,5,1,5,1,6,3,6,135,8,6,1,6,1,6,1,6,1,6,
        1,6,5,6,142,8,6,10,6,12,6,145,9,6,3,6,147,8,6,1,6,1,6,1,6,1,7,1,
        7,1,7,3,7,155,8,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,
        8,3,8,169,8,8,1,8,1,8,1,8,1,8,3,8,175,8,8,1,9,1,9,1,9,1,9,3,9,181,
        8,9,1,9,1,9,1,10,1,10,5,10,187,8,10,10,10,12,10,190,9,10,1,10,1,
        10,1,11,1,11,1,11,1,11,1,11,1,11,1,11,3,11,201,8,11,1,12,1,12,1,
        12,1,12,1,12,1,12,1,13,1,13,1,13,1,13,3,13,213,8,13,1,14,1,14,1,
        14,1,14,1,14,1,14,3,14,221,8,14,1,15,1,15,1,15,1,15,3,15,227,8,15,
        1,15,3,15,230,8,15,1,15,1,15,3,15,234,8,15,1,15,1,15,1,15,1,16,1,
        16,1,16,1,16,5,16,243,8,16,10,16,12,16,246,9,16,1,17,1,17,1,17,5,
        17,251,8,17,10,17,12,17,254,9,17,1,18,1,18,1,18,1,18,1,18,1,18,5,
        18,262,8,18,10,18,12,18,265,9,18,1,18,3,18,268,8,18,1,18,1,18,1,
        18,0,1,2,19,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,
        0,10,1,0,19,20,2,0,21,22,34,34,1,0,23,25,1,0,21,22,1,0,28,31,1,0,
        26,27,2,0,5,7,49,49,2,0,5,8,49,49,1,0,12,13,3,0,3,3,5,7,49,49,301,
        0,42,1,0,0,0,2,67,1,0,0,0,4,97,1,0,0,0,6,108,1,0,0,0,8,116,1,0,0,
        0,10,119,1,0,0,0,12,134,1,0,0,0,14,151,1,0,0,0,16,174,1,0,0,0,18,
        176,1,0,0,0,20,184,1,0,0,0,22,193,1,0,0,0,24,202,1,0,0,0,26,212,
        1,0,0,0,28,220,1,0,0,0,30,222,1,0,0,0,32,238,1,0,0,0,34,247,1,0,
        0,0,36,255,1,0,0,0,38,41,3,10,5,0,39,41,3,12,6,0,40,38,1,0,0,0,40,
        39,1,0,0,0,41,44,1,0,0,0,42,40,1,0,0,0,42,43,1,0,0,0,43,45,1,0,0,
        0,44,42,1,0,0,0,45,46,5,0,0,1,46,1,1,0,0,0,47,48,6,1,-1,0,48,50,
        5,37,0,0,49,51,3,6,3,0,50,49,1,0,0,0,50,51,1,0,0,0,51,52,1,0,0,0,
        52,68,5,38,0,0,53,54,5,39,0,0,54,55,3,2,1,0,55,56,5,40,0,0,56,68,
        1,0,0,0,57,68,5,44,0,0,58,68,5,45,0,0,59,68,5,48,0,0,60,68,5,49,
        0,0,61,68,3,14,7,0,62,63,7,0,0,0,63,68,3,2,1,9,64,65,7,1,0,0,65,
        68,3,2,1,8,66,68,3,4,2,0,67,47,1,0,0,0,67,53,1,0,0,0,67,57,1,0,0,
        0,67,58,1,0,0,0,67,59,1,0,0,0,67,60,1,0,0,0,67,61,1,0,0,0,67,62,
        1,0,0,0,67,64,1,0,0,0,67,66,1,0,0,0,68,94,1,0,0,0,69,70,10,7,0,0,
        70,71,7,2,0,0,71,93,3,2,1,8,72,73,10,6,0,0,73,74,7,3,0,0,74,93,3,
        2,1,7,75,76,10,5,0,0,76,77,7,4,0,0,77,93,3,2,1,6,78,79,10,4,0,0,
        79,80,7,5,0,0,80,93,3,2,1,5,81,82,10,3,0,0,82,83,5,33,0,0,83,93,
        3,2,1,4,84,85,10,2,0,0,85,86,5,32,0,0,86,93,3,2,1,3,87,88,10,12,
        0,0,88,89,5,36,0,0,89,93,5,49,0,0,90,91,10,10,0,0,91,93,7,0,0,0,
        92,69,1,0,0,0,92,72,1,0,0,0,92,75,1,0,0,0,92,78,1,0,0,0,92,81,1,
        0,0,0,92,84,1,0,0,0,92,87,1,0,0,0,92,90,1,0,0,0,93,96,1,0,0,0,94,
        92,1,0,0,0,94,95,1,0,0,0,95,3,1,0,0,0,96,94,1,0,0,0,97,102,5,49,
        0,0,98,99,5,36,0,0,99,101,5,49,0,0,100,98,1,0,0,0,101,104,1,0,0,
        0,102,100,1,0,0,0,102,103,1,0,0,0,103,105,1,0,0,0,104,102,1,0,0,
        0,105,106,5,35,0,0,106,107,3,2,1,0,107,5,1,0,0,0,108,113,3,2,1,0,
        109,110,5,42,0,0,110,112,3,2,1,0,111,109,1,0,0,0,112,115,1,0,0,0,
        113,111,1,0,0,0,113,114,1,0,0,0,114,7,1,0,0,0,115,113,1,0,0,0,116,
        117,7,6,0,0,117,118,5,49,0,0,118,9,1,0,0,0,119,120,5,9,0,0,120,121,
        5,49,0,0,121,127,5,37,0,0,122,123,3,8,4,0,123,124,5,41,0,0,124,126,
        1,0,0,0,125,122,1,0,0,0,126,129,1,0,0,0,127,125,1,0,0,0,127,128,
        1,0,0,0,128,130,1,0,0,0,129,127,1,0,0,0,130,131,5,38,0,0,131,132,
        5,41,0,0,132,11,1,0,0,0,133,135,7,7,0,0,134,133,1,0,0,0,134,135,
        1,0,0,0,135,136,1,0,0,0,136,137,5,49,0,0,137,146,5,39,0,0,138,143,
        3,8,4,0,139,140,5,42,0,0,140,142,3,8,4,0,141,139,1,0,0,0,142,145,
        1,0,0,0,143,141,1,0,0,0,143,144,1,0,0,0,144,147,1,0,0,0,145,143,
        1,0,0,0,146,138,1,0,0,0,146,147,1,0,0,0,147,148,1,0,0,0,148,149,
        5,40,0,0,149,150,3,20,10,0,150,13,1,0,0,0,151,152,5,49,0,0,152,154,
        5,39,0,0,153,155,3,6,3,0,154,153,1,0,0,0,154,155,1,0,0,0,155,156,
        1,0,0,0,156,157,5,40,0,0,157,15,1,0,0,0,158,175,3,18,9,0,159,175,
        3,20,10,0,160,175,3,22,11,0,161,175,3,24,12,0,162,175,3,30,15,0,
        163,175,3,36,18,0,164,165,7,8,0,0,165,175,5,41,0,0,166,168,5,4,0,
        0,167,169,3,2,1,0,168,167,1,0,0,0,168,169,1,0,0,0,169,170,1,0,0,
        0,170,175,5,41,0,0,171,172,3,2,1,0,172,173,5,41,0,0,173,175,1,0,
        0,0,174,158,1,0,0,0,174,159,1,0,0,0,174,160,1,0,0,0,174,161,1,0,
        0,0,174,162,1,0,0,0,174,163,1,0,0,0,174,164,1,0,0,0,174,166,1,0,
        0,0,174,171,1,0,0,0,175,17,1,0,0,0,176,177,7,9,0,0,177,180,5,49,
        0,0,178,179,5,35,0,0,179,181,3,2,1,0,180,178,1,0,0,0,180,181,1,0,
        0,0,181,182,1,0,0,0,182,183,5,41,0,0,183,19,1,0,0,0,184,188,5,37,
        0,0,185,187,3,16,8,0,186,185,1,0,0,0,187,190,1,0,0,0,188,186,1,0,
        0,0,188,189,1,0,0,0,189,191,1,0,0,0,190,188,1,0,0,0,191,192,5,38,
        0,0,192,21,1,0,0,0,193,194,5,15,0,0,194,195,5,39,0,0,195,196,3,2,
        1,0,196,197,5,40,0,0,197,200,3,16,8,0,198,199,5,16,0,0,199,201,3,
        16,8,0,200,198,1,0,0,0,200,201,1,0,0,0,201,23,1,0,0,0,202,203,5,
        11,0,0,203,204,5,39,0,0,204,205,3,2,1,0,205,206,5,40,0,0,206,207,
        3,16,8,0,207,25,1,0,0,0,208,213,3,18,9,0,209,210,3,4,2,0,210,211,
        5,41,0,0,211,213,1,0,0,0,212,208,1,0,0,0,212,209,1,0,0,0,213,27,
        1,0,0,0,214,221,3,4,2,0,215,216,3,2,1,0,216,217,7,0,0,0,217,221,
        1,0,0,0,218,219,7,0,0,0,219,221,3,2,1,0,220,214,1,0,0,0,220,215,
        1,0,0,0,220,218,1,0,0,0,221,29,1,0,0,0,222,223,5,10,0,0,223,226,
        5,39,0,0,224,227,3,26,13,0,225,227,5,41,0,0,226,224,1,0,0,0,226,
        225,1,0,0,0,227,229,1,0,0,0,228,230,3,2,1,0,229,228,1,0,0,0,229,
        230,1,0,0,0,230,231,1,0,0,0,231,233,5,41,0,0,232,234,3,28,14,0,233,
        232,1,0,0,0,233,234,1,0,0,0,234,235,1,0,0,0,235,236,5,40,0,0,236,
        237,3,16,8,0,237,31,1,0,0,0,238,239,5,18,0,0,239,240,3,2,1,0,240,
        244,5,43,0,0,241,243,3,16,8,0,242,241,1,0,0,0,243,246,1,0,0,0,244,
        242,1,0,0,0,244,245,1,0,0,0,245,33,1,0,0,0,246,244,1,0,0,0,247,248,
        5,14,0,0,248,252,5,43,0,0,249,251,3,16,8,0,250,249,1,0,0,0,251,254,
        1,0,0,0,252,250,1,0,0,0,252,253,1,0,0,0,253,35,1,0,0,0,254,252,1,
        0,0,0,255,256,5,17,0,0,256,257,5,39,0,0,257,258,3,2,1,0,258,259,
        5,40,0,0,259,263,5,37,0,0,260,262,3,32,16,0,261,260,1,0,0,0,262,
        265,1,0,0,0,263,261,1,0,0,0,263,264,1,0,0,0,264,267,1,0,0,0,265,
        263,1,0,0,0,266,268,3,34,17,0,267,266,1,0,0,0,267,268,1,0,0,0,268,
        269,1,0,0,0,269,270,5,38,0,0,270,37,1,0,0,0,27,40,42,50,67,92,94,
        102,113,127,134,143,146,154,168,174,180,188,200,212,220,226,229,
        233,244,252,263,267
    ]

class TyCParser ( Parser ):

    grammarFileName = "TyC.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "'auto'", "'return'", 
                     "'int'", "'float'", "'string'", "'void'", "'struct'", 
                     "'for'", "'while'", "'break'", "'continue'", "'default'", 
                     "'if'", "'else'", "'switch'", "'case'", "'++'", "'--'", 
                     "'+'", "'-'", "'*'", "'/'", "'%'", "'=='", "'!='", 
                     "'<'", "'>'", "'<='", "'>='", "'||'", "'&&'", "'!'", 
                     "'='", "'.'", "'{'", "'}'", "'('", "')'", "';'", "','", 
                     "':'" ]

    symbolicNames = [ "<INVALID>", "BLOCK_CMT", "LINE_CMT", "AUTO", "RETURN", 
                      "INT_KW", "FLOAT_KW", "STRING_KW", "VOID", "STRUCT", 
                      "FOR", "WHILE", "BREAK", "CONTINUE", "DEFAULT", "IF", 
                      "ELSE", "SWITCH", "CASE", "INC_OP", "DEC_OP", "ADD_OP", 
                      "SUB_OP", "MUL_OP", "DIV_OP", "MOD_OP", "EQ_OP", "NOTEQ_OP", 
                      "LESS_OP", "GREAT_OP", "LEQ_OP", "GEQ_OP", "LO_OR", 
                      "LO_AND", "LO_NOT", "ASSIGN", "MEM_ACC", "LB", "RB", 
                      "LP", "RP", "SEMICOLON", "COMMA", "COLON", "INT_LIT", 
                      "FLOAT_LIT", "ILLEGAL_ESCAPE", "UNCLOSE_STRING", "STRING_LIT", 
                      "ID", "WS", "ERROR_CHAR" ]

    RULE_program = 0
    RULE_expr = 1
    RULE_assign_expr = 2
    RULE_expr_list = 3
    RULE_param = 4
    RULE_struct_decl = 5
    RULE_func_decl = 6
    RULE_func_call = 7
    RULE_stmt = 8
    RULE_decl_stmt = 9
    RULE_block_stmt = 10
    RULE_if_stmt = 11
    RULE_while_stmt = 12
    RULE_for_init = 13
    RULE_for_updt = 14
    RULE_for_stmt = 15
    RULE_sw_case = 16
    RULE_sw_def = 17
    RULE_switch_stmt = 18

    ruleNames =  [ "program", "expr", "assign_expr", "expr_list", "param", 
                   "struct_decl", "func_decl", "func_call", "stmt", "decl_stmt", 
                   "block_stmt", "if_stmt", "while_stmt", "for_init", "for_updt", 
                   "for_stmt", "sw_case", "sw_def", "switch_stmt" ]

    EOF = Token.EOF
    BLOCK_CMT=1
    LINE_CMT=2
    AUTO=3
    RETURN=4
    INT_KW=5
    FLOAT_KW=6
    STRING_KW=7
    VOID=8
    STRUCT=9
    FOR=10
    WHILE=11
    BREAK=12
    CONTINUE=13
    DEFAULT=14
    IF=15
    ELSE=16
    SWITCH=17
    CASE=18
    INC_OP=19
    DEC_OP=20
    ADD_OP=21
    SUB_OP=22
    MUL_OP=23
    DIV_OP=24
    MOD_OP=25
    EQ_OP=26
    NOTEQ_OP=27
    LESS_OP=28
    GREAT_OP=29
    LEQ_OP=30
    GEQ_OP=31
    LO_OR=32
    LO_AND=33
    LO_NOT=34
    ASSIGN=35
    MEM_ACC=36
    LB=37
    RB=38
    LP=39
    RP=40
    SEMICOLON=41
    COMMA=42
    COLON=43
    INT_LIT=44
    FLOAT_LIT=45
    ILLEGAL_ESCAPE=46
    UNCLOSE_STRING=47
    STRING_LIT=48
    ID=49
    WS=50
    ERROR_CHAR=51

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(TyCParser.EOF, 0)

        def struct_decl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TyCParser.Struct_declContext)
            else:
                return self.getTypedRuleContext(TyCParser.Struct_declContext,i)


        def func_decl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TyCParser.Func_declContext)
            else:
                return self.getTypedRuleContext(TyCParser.Func_declContext,i)


        def getRuleIndex(self):
            return TyCParser.RULE_program




    def program(self):

        localctx = TyCParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 562949953422304) != 0):
                self.state = 40
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [9]:
                    self.state = 38
                    self.struct_decl()
                    pass
                elif token in [5, 6, 7, 8, 49]:
                    self.state = 39
                    self.func_decl()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 44
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 45
            self.match(TyCParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LB(self):
            return self.getToken(TyCParser.LB, 0)

        def RB(self):
            return self.getToken(TyCParser.RB, 0)

        def expr_list(self):
            return self.getTypedRuleContext(TyCParser.Expr_listContext,0)


        def LP(self):
            return self.getToken(TyCParser.LP, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TyCParser.ExprContext)
            else:
                return self.getTypedRuleContext(TyCParser.ExprContext,i)


        def RP(self):
            return self.getToken(TyCParser.RP, 0)

        def INT_LIT(self):
            return self.getToken(TyCParser.INT_LIT, 0)

        def FLOAT_LIT(self):
            return self.getToken(TyCParser.FLOAT_LIT, 0)

        def STRING_LIT(self):
            return self.getToken(TyCParser.STRING_LIT, 0)

        def ID(self):
            return self.getToken(TyCParser.ID, 0)

        def func_call(self):
            return self.getTypedRuleContext(TyCParser.Func_callContext,0)


        def INC_OP(self):
            return self.getToken(TyCParser.INC_OP, 0)

        def DEC_OP(self):
            return self.getToken(TyCParser.DEC_OP, 0)

        def LO_NOT(self):
            return self.getToken(TyCParser.LO_NOT, 0)

        def SUB_OP(self):
            return self.getToken(TyCParser.SUB_OP, 0)

        def ADD_OP(self):
            return self.getToken(TyCParser.ADD_OP, 0)

        def assign_expr(self):
            return self.getTypedRuleContext(TyCParser.Assign_exprContext,0)


        def MUL_OP(self):
            return self.getToken(TyCParser.MUL_OP, 0)

        def DIV_OP(self):
            return self.getToken(TyCParser.DIV_OP, 0)

        def MOD_OP(self):
            return self.getToken(TyCParser.MOD_OP, 0)

        def LESS_OP(self):
            return self.getToken(TyCParser.LESS_OP, 0)

        def LEQ_OP(self):
            return self.getToken(TyCParser.LEQ_OP, 0)

        def GREAT_OP(self):
            return self.getToken(TyCParser.GREAT_OP, 0)

        def GEQ_OP(self):
            return self.getToken(TyCParser.GEQ_OP, 0)

        def EQ_OP(self):
            return self.getToken(TyCParser.EQ_OP, 0)

        def NOTEQ_OP(self):
            return self.getToken(TyCParser.NOTEQ_OP, 0)

        def LO_AND(self):
            return self.getToken(TyCParser.LO_AND, 0)

        def LO_OR(self):
            return self.getToken(TyCParser.LO_OR, 0)

        def MEM_ACC(self):
            return self.getToken(TyCParser.MEM_ACC, 0)

        def getRuleIndex(self):
            return TyCParser.RULE_expr



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = TyCParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 67
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.state = 48
                self.match(TyCParser.LB)
                self.state = 50
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 897905870766080) != 0):
                    self.state = 49
                    self.expr_list()


                self.state = 52
                self.match(TyCParser.RB)
                pass

            elif la_ == 2:
                self.state = 53
                self.match(TyCParser.LP)
                self.state = 54
                self.expr(0)
                self.state = 55
                self.match(TyCParser.RP)
                pass

            elif la_ == 3:
                self.state = 57
                self.match(TyCParser.INT_LIT)
                pass

            elif la_ == 4:
                self.state = 58
                self.match(TyCParser.FLOAT_LIT)
                pass

            elif la_ == 5:
                self.state = 59
                self.match(TyCParser.STRING_LIT)
                pass

            elif la_ == 6:
                self.state = 60
                self.match(TyCParser.ID)
                pass

            elif la_ == 7:
                self.state = 61
                self.func_call()
                pass

            elif la_ == 8:
                self.state = 62
                _la = self._input.LA(1)
                if not(_la==19 or _la==20):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 63
                self.expr(9)
                pass

            elif la_ == 9:
                self.state = 64
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 17186160640) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 65
                self.expr(8)
                pass

            elif la_ == 10:
                self.state = 66
                self.assign_expr()
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 94
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 92
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                    if la_ == 1:
                        localctx = TyCParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 69
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 70
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 58720256) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 71
                        self.expr(8)
                        pass

                    elif la_ == 2:
                        localctx = TyCParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 72
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 73
                        _la = self._input.LA(1)
                        if not(_la==21 or _la==22):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 74
                        self.expr(7)
                        pass

                    elif la_ == 3:
                        localctx = TyCParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 75
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 76
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 4026531840) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 77
                        self.expr(6)
                        pass

                    elif la_ == 4:
                        localctx = TyCParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 78
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 79
                        _la = self._input.LA(1)
                        if not(_la==26 or _la==27):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 80
                        self.expr(5)
                        pass

                    elif la_ == 5:
                        localctx = TyCParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 81
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 82
                        self.match(TyCParser.LO_AND)
                        self.state = 83
                        self.expr(4)
                        pass

                    elif la_ == 6:
                        localctx = TyCParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 84
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 85
                        self.match(TyCParser.LO_OR)
                        self.state = 86
                        self.expr(3)
                        pass

                    elif la_ == 7:
                        localctx = TyCParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 87
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 88
                        self.match(TyCParser.MEM_ACC)
                        self.state = 89
                        self.match(TyCParser.ID)
                        pass

                    elif la_ == 8:
                        localctx = TyCParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 90
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 91
                        _la = self._input.LA(1)
                        if not(_la==19 or _la==20):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        pass

             
                self.state = 96
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Assign_exprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(TyCParser.ID)
            else:
                return self.getToken(TyCParser.ID, i)

        def ASSIGN(self):
            return self.getToken(TyCParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(TyCParser.ExprContext,0)


        def MEM_ACC(self, i:int=None):
            if i is None:
                return self.getTokens(TyCParser.MEM_ACC)
            else:
                return self.getToken(TyCParser.MEM_ACC, i)

        def getRuleIndex(self):
            return TyCParser.RULE_assign_expr




    def assign_expr(self):

        localctx = TyCParser.Assign_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_assign_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 97
            self.match(TyCParser.ID)
            self.state = 102
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==36:
                self.state = 98
                self.match(TyCParser.MEM_ACC)
                self.state = 99
                self.match(TyCParser.ID)
                self.state = 104
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 105
            self.match(TyCParser.ASSIGN)
            self.state = 106
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Expr_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TyCParser.ExprContext)
            else:
                return self.getTypedRuleContext(TyCParser.ExprContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(TyCParser.COMMA)
            else:
                return self.getToken(TyCParser.COMMA, i)

        def getRuleIndex(self):
            return TyCParser.RULE_expr_list




    def expr_list(self):

        localctx = TyCParser.Expr_listContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_expr_list)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 108
            self.expr(0)
            self.state = 113
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==42:
                self.state = 109
                self.match(TyCParser.COMMA)
                self.state = 110
                self.expr(0)
                self.state = 115
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(TyCParser.ID)
            else:
                return self.getToken(TyCParser.ID, i)

        def INT_KW(self):
            return self.getToken(TyCParser.INT_KW, 0)

        def FLOAT_KW(self):
            return self.getToken(TyCParser.FLOAT_KW, 0)

        def STRING_KW(self):
            return self.getToken(TyCParser.STRING_KW, 0)

        def getRuleIndex(self):
            return TyCParser.RULE_param




    def param(self):

        localctx = TyCParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 116
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 562949953421536) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 117
            self.match(TyCParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Struct_declContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRUCT(self):
            return self.getToken(TyCParser.STRUCT, 0)

        def ID(self):
            return self.getToken(TyCParser.ID, 0)

        def LB(self):
            return self.getToken(TyCParser.LB, 0)

        def RB(self):
            return self.getToken(TyCParser.RB, 0)

        def SEMICOLON(self, i:int=None):
            if i is None:
                return self.getTokens(TyCParser.SEMICOLON)
            else:
                return self.getToken(TyCParser.SEMICOLON, i)

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TyCParser.ParamContext)
            else:
                return self.getTypedRuleContext(TyCParser.ParamContext,i)


        def getRuleIndex(self):
            return TyCParser.RULE_struct_decl




    def struct_decl(self):

        localctx = TyCParser.Struct_declContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_struct_decl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 119
            self.match(TyCParser.STRUCT)
            self.state = 120
            self.match(TyCParser.ID)
            self.state = 121
            self.match(TyCParser.LB)
            self.state = 127
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 562949953421536) != 0):
                self.state = 122
                self.param()
                self.state = 123
                self.match(TyCParser.SEMICOLON)
                self.state = 129
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 130
            self.match(TyCParser.RB)
            self.state = 131
            self.match(TyCParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Func_declContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(TyCParser.ID)
            else:
                return self.getToken(TyCParser.ID, i)

        def LP(self):
            return self.getToken(TyCParser.LP, 0)

        def RP(self):
            return self.getToken(TyCParser.RP, 0)

        def block_stmt(self):
            return self.getTypedRuleContext(TyCParser.Block_stmtContext,0)


        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TyCParser.ParamContext)
            else:
                return self.getTypedRuleContext(TyCParser.ParamContext,i)


        def INT_KW(self):
            return self.getToken(TyCParser.INT_KW, 0)

        def FLOAT_KW(self):
            return self.getToken(TyCParser.FLOAT_KW, 0)

        def STRING_KW(self):
            return self.getToken(TyCParser.STRING_KW, 0)

        def VOID(self):
            return self.getToken(TyCParser.VOID, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(TyCParser.COMMA)
            else:
                return self.getToken(TyCParser.COMMA, i)

        def getRuleIndex(self):
            return TyCParser.RULE_func_decl




    def func_decl(self):

        localctx = TyCParser.Func_declContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_func_decl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 134
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.state = 133
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 562949953421792) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


            self.state = 136
            self.match(TyCParser.ID)
            self.state = 137
            self.match(TyCParser.LP)
            self.state = 146
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 562949953421536) != 0):
                self.state = 138
                self.param()
                self.state = 143
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==42:
                    self.state = 139
                    self.match(TyCParser.COMMA)
                    self.state = 140
                    self.param()
                    self.state = 145
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 148
            self.match(TyCParser.RP)
            self.state = 149
            self.block_stmt()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Func_callContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(TyCParser.ID, 0)

        def LP(self):
            return self.getToken(TyCParser.LP, 0)

        def RP(self):
            return self.getToken(TyCParser.RP, 0)

        def expr_list(self):
            return self.getTypedRuleContext(TyCParser.Expr_listContext,0)


        def getRuleIndex(self):
            return TyCParser.RULE_func_call




    def func_call(self):

        localctx = TyCParser.Func_callContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_func_call)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self.match(TyCParser.ID)
            self.state = 152
            self.match(TyCParser.LP)
            self.state = 154
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 897905870766080) != 0):
                self.state = 153
                self.expr_list()


            self.state = 156
            self.match(TyCParser.RP)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def decl_stmt(self):
            return self.getTypedRuleContext(TyCParser.Decl_stmtContext,0)


        def block_stmt(self):
            return self.getTypedRuleContext(TyCParser.Block_stmtContext,0)


        def if_stmt(self):
            return self.getTypedRuleContext(TyCParser.If_stmtContext,0)


        def while_stmt(self):
            return self.getTypedRuleContext(TyCParser.While_stmtContext,0)


        def for_stmt(self):
            return self.getTypedRuleContext(TyCParser.For_stmtContext,0)


        def switch_stmt(self):
            return self.getTypedRuleContext(TyCParser.Switch_stmtContext,0)


        def SEMICOLON(self):
            return self.getToken(TyCParser.SEMICOLON, 0)

        def BREAK(self):
            return self.getToken(TyCParser.BREAK, 0)

        def CONTINUE(self):
            return self.getToken(TyCParser.CONTINUE, 0)

        def RETURN(self):
            return self.getToken(TyCParser.RETURN, 0)

        def expr(self):
            return self.getTypedRuleContext(TyCParser.ExprContext,0)


        def getRuleIndex(self):
            return TyCParser.RULE_stmt




    def stmt(self):

        localctx = TyCParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_stmt)
        self._la = 0 # Token type
        try:
            self.state = 174
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 158
                self.decl_stmt()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 159
                self.block_stmt()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 160
                self.if_stmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 161
                self.while_stmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 162
                self.for_stmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 163
                self.switch_stmt()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 164
                _la = self._input.LA(1)
                if not(_la==12 or _la==13):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 165
                self.match(TyCParser.SEMICOLON)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 166
                self.match(TyCParser.RETURN)
                self.state = 168
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 897905870766080) != 0):
                    self.state = 167
                    self.expr(0)


                self.state = 170
                self.match(TyCParser.SEMICOLON)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 171
                self.expr(0)
                self.state = 172
                self.match(TyCParser.SEMICOLON)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Decl_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(TyCParser.ID)
            else:
                return self.getToken(TyCParser.ID, i)

        def SEMICOLON(self):
            return self.getToken(TyCParser.SEMICOLON, 0)

        def INT_KW(self):
            return self.getToken(TyCParser.INT_KW, 0)

        def FLOAT_KW(self):
            return self.getToken(TyCParser.FLOAT_KW, 0)

        def STRING_KW(self):
            return self.getToken(TyCParser.STRING_KW, 0)

        def AUTO(self):
            return self.getToken(TyCParser.AUTO, 0)

        def ASSIGN(self):
            return self.getToken(TyCParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(TyCParser.ExprContext,0)


        def getRuleIndex(self):
            return TyCParser.RULE_decl_stmt




    def decl_stmt(self):

        localctx = TyCParser.Decl_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_decl_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 176
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 562949953421544) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 177
            self.match(TyCParser.ID)
            self.state = 180
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==35:
                self.state = 178
                self.match(TyCParser.ASSIGN)
                self.state = 179
                self.expr(0)


            self.state = 182
            self.match(TyCParser.SEMICOLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Block_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LB(self):
            return self.getToken(TyCParser.LB, 0)

        def RB(self):
            return self.getToken(TyCParser.RB, 0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TyCParser.StmtContext)
            else:
                return self.getTypedRuleContext(TyCParser.StmtContext,i)


        def getRuleIndex(self):
            return TyCParser.RULE_block_stmt




    def block_stmt(self):

        localctx = TyCParser.Block_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_block_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 184
            self.match(TyCParser.LB)
            self.state = 188
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 897905870945528) != 0):
                self.state = 185
                self.stmt()
                self.state = 190
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 191
            self.match(TyCParser.RB)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class If_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(TyCParser.IF, 0)

        def LP(self):
            return self.getToken(TyCParser.LP, 0)

        def expr(self):
            return self.getTypedRuleContext(TyCParser.ExprContext,0)


        def RP(self):
            return self.getToken(TyCParser.RP, 0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TyCParser.StmtContext)
            else:
                return self.getTypedRuleContext(TyCParser.StmtContext,i)


        def ELSE(self):
            return self.getToken(TyCParser.ELSE, 0)

        def getRuleIndex(self):
            return TyCParser.RULE_if_stmt




    def if_stmt(self):

        localctx = TyCParser.If_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_if_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 193
            self.match(TyCParser.IF)
            self.state = 194
            self.match(TyCParser.LP)
            self.state = 195
            self.expr(0)
            self.state = 196
            self.match(TyCParser.RP)
            self.state = 197
            self.stmt()
            self.state = 200
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.state = 198
                self.match(TyCParser.ELSE)
                self.state = 199
                self.stmt()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class While_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(TyCParser.WHILE, 0)

        def LP(self):
            return self.getToken(TyCParser.LP, 0)

        def expr(self):
            return self.getTypedRuleContext(TyCParser.ExprContext,0)


        def RP(self):
            return self.getToken(TyCParser.RP, 0)

        def stmt(self):
            return self.getTypedRuleContext(TyCParser.StmtContext,0)


        def getRuleIndex(self):
            return TyCParser.RULE_while_stmt




    def while_stmt(self):

        localctx = TyCParser.While_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_while_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 202
            self.match(TyCParser.WHILE)
            self.state = 203
            self.match(TyCParser.LP)
            self.state = 204
            self.expr(0)
            self.state = 205
            self.match(TyCParser.RP)
            self.state = 206
            self.stmt()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class For_initContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def decl_stmt(self):
            return self.getTypedRuleContext(TyCParser.Decl_stmtContext,0)


        def assign_expr(self):
            return self.getTypedRuleContext(TyCParser.Assign_exprContext,0)


        def SEMICOLON(self):
            return self.getToken(TyCParser.SEMICOLON, 0)

        def getRuleIndex(self):
            return TyCParser.RULE_for_init




    def for_init(self):

        localctx = TyCParser.For_initContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_for_init)
        try:
            self.state = 212
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 208
                self.decl_stmt()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 209
                self.assign_expr()
                self.state = 210
                self.match(TyCParser.SEMICOLON)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class For_updtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assign_expr(self):
            return self.getTypedRuleContext(TyCParser.Assign_exprContext,0)


        def expr(self):
            return self.getTypedRuleContext(TyCParser.ExprContext,0)


        def INC_OP(self):
            return self.getToken(TyCParser.INC_OP, 0)

        def DEC_OP(self):
            return self.getToken(TyCParser.DEC_OP, 0)

        def getRuleIndex(self):
            return TyCParser.RULE_for_updt




    def for_updt(self):

        localctx = TyCParser.For_updtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_for_updt)
        self._la = 0 # Token type
        try:
            self.state = 220
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 214
                self.assign_expr()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 215
                self.expr(0)
                self.state = 216
                _la = self._input.LA(1)
                if not(_la==19 or _la==20):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 218
                _la = self._input.LA(1)
                if not(_la==19 or _la==20):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 219
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class For_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(TyCParser.FOR, 0)

        def LP(self):
            return self.getToken(TyCParser.LP, 0)

        def SEMICOLON(self, i:int=None):
            if i is None:
                return self.getTokens(TyCParser.SEMICOLON)
            else:
                return self.getToken(TyCParser.SEMICOLON, i)

        def RP(self):
            return self.getToken(TyCParser.RP, 0)

        def stmt(self):
            return self.getTypedRuleContext(TyCParser.StmtContext,0)


        def for_init(self):
            return self.getTypedRuleContext(TyCParser.For_initContext,0)


        def expr(self):
            return self.getTypedRuleContext(TyCParser.ExprContext,0)


        def for_updt(self):
            return self.getTypedRuleContext(TyCParser.For_updtContext,0)


        def getRuleIndex(self):
            return TyCParser.RULE_for_stmt




    def for_stmt(self):

        localctx = TyCParser.For_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_for_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 222
            self.match(TyCParser.FOR)
            self.state = 223
            self.match(TyCParser.LP)
            self.state = 226
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3, 5, 6, 7, 49]:
                self.state = 224
                self.for_init()
                pass
            elif token in [41]:
                self.state = 225
                self.match(TyCParser.SEMICOLON)
                pass
            else:
                raise NoViableAltException(self)

            self.state = 229
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 897905870766080) != 0):
                self.state = 228
                self.expr(0)


            self.state = 231
            self.match(TyCParser.SEMICOLON)
            self.state = 233
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 897905870766080) != 0):
                self.state = 232
                self.for_updt()


            self.state = 235
            self.match(TyCParser.RP)
            self.state = 236
            self.stmt()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Sw_caseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CASE(self):
            return self.getToken(TyCParser.CASE, 0)

        def expr(self):
            return self.getTypedRuleContext(TyCParser.ExprContext,0)


        def COLON(self):
            return self.getToken(TyCParser.COLON, 0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TyCParser.StmtContext)
            else:
                return self.getTypedRuleContext(TyCParser.StmtContext,i)


        def getRuleIndex(self):
            return TyCParser.RULE_sw_case




    def sw_case(self):

        localctx = TyCParser.Sw_caseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_sw_case)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 238
            self.match(TyCParser.CASE)
            self.state = 239
            self.expr(0)
            self.state = 240
            self.match(TyCParser.COLON)
            self.state = 244
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 897905870945528) != 0):
                self.state = 241
                self.stmt()
                self.state = 246
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Sw_defContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DEFAULT(self):
            return self.getToken(TyCParser.DEFAULT, 0)

        def COLON(self):
            return self.getToken(TyCParser.COLON, 0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TyCParser.StmtContext)
            else:
                return self.getTypedRuleContext(TyCParser.StmtContext,i)


        def getRuleIndex(self):
            return TyCParser.RULE_sw_def




    def sw_def(self):

        localctx = TyCParser.Sw_defContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_sw_def)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 247
            self.match(TyCParser.DEFAULT)
            self.state = 248
            self.match(TyCParser.COLON)
            self.state = 252
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 897905870945528) != 0):
                self.state = 249
                self.stmt()
                self.state = 254
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Switch_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SWITCH(self):
            return self.getToken(TyCParser.SWITCH, 0)

        def LP(self):
            return self.getToken(TyCParser.LP, 0)

        def expr(self):
            return self.getTypedRuleContext(TyCParser.ExprContext,0)


        def RP(self):
            return self.getToken(TyCParser.RP, 0)

        def LB(self):
            return self.getToken(TyCParser.LB, 0)

        def RB(self):
            return self.getToken(TyCParser.RB, 0)

        def sw_case(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TyCParser.Sw_caseContext)
            else:
                return self.getTypedRuleContext(TyCParser.Sw_caseContext,i)


        def sw_def(self):
            return self.getTypedRuleContext(TyCParser.Sw_defContext,0)


        def getRuleIndex(self):
            return TyCParser.RULE_switch_stmt




    def switch_stmt(self):

        localctx = TyCParser.Switch_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_switch_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 255
            self.match(TyCParser.SWITCH)
            self.state = 256
            self.match(TyCParser.LP)
            self.state = 257
            self.expr(0)
            self.state = 258
            self.match(TyCParser.RP)
            self.state = 259
            self.match(TyCParser.LB)
            self.state = 263
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==18:
                self.state = 260
                self.sw_case()
                self.state = 265
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 267
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 266
                self.sw_def()


            self.state = 269
            self.match(TyCParser.RB)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 10)
         




