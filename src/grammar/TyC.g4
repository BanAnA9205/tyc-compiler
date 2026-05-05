grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

program: (struct_decl | func_decl)* EOF;

////////////////////////////// LEXER //////////////////////////////

// Comments
BLOCK_CMT: '/*' .*? '*/' -> skip ;
LINE_CMT: '//' ~[\r\n]* -> skip ;

// Keywords (higher priority than Identifier)
AUTO: 'auto' ; 

// MAIN: 'main' ;
RETURN: 'return' ;

INT_KW: 'int' ;
FLOAT_KW: 'float' ;
STRING_KW: 'string' ;

VOID: 'void' ;
STRUCT: 'struct' ;

FOR: 'for' ;
WHILE: 'while' ;

BREAK: 'break' ;
CONTINUE: 'continue' ;
DEFAULT: 'default' ;

IF: 'if' ;
ELSE: 'else' ;
SWITCH: 'switch' ;
CASE: 'case' ;

// Operators
INC_OP: '++' ;
DEC_OP: '--' ;

ADD_OP: '+' ;
SUB_OP: '-' ;
MUL_OP: '*' ;
DIV_OP: '/' ;
MOD_OP: '%' ;

EQ_OP: '==' ;
NOTEQ_OP: '!=' ;

LESS_OP: '<' ;
GREAT_OP: '>' ;
LEQ_OP: '<=' ;
GEQ_OP: '>=' ;

LO_OR: '||' ;
LO_AND: '&&' ;
LO_NOT: '!' ;

ASSIGN: '=' ;

MEM_ACC: '.' ;

// Separators
LB: '{' ;
RB: '}' ;

LP: '(' ;
RP: ')' ;

SEMICOLON: ';' ;
COMMA: ',' ;
COLON: ':' ;

// Literals
INT_LIT: [0-9]+ ;
FLOAT_LIT: ([0-9]* '.' [0-9]+ | [0-9]+ '.' [0-9]*) ([eE] [+-]? [0-9]+)? 
         | [0-9]+ [eE] [+-]? [0-9]+ ;

fragment ESCAPE_SEQ: '\\b' | '\\f' | '\\r' | '\\n' | '\\t' | '\\"' | '\\\\' ;
fragment STRING_CHR: ESCAPE_SEQ | ~["\\\r\n] ;

// String errors
ILLEGAL_ESCAPE: '"' STRING_CHR* '\\' ~[bfrnt"\\\n\r]
                { self.text = self.text[1:] } ;

UNCLOSE_STRING: '"' STRING_CHR* '\\'? ([\r\n] | EOF)
                { self.text = self.text[1:].rstrip('\r\n') } ;

STRING_LIT: '"' STRING_CHR* '"' 
            { self.text = self.text[1:-1] } ;

// Identifier
ID: [a-zA-Z_] [a-zA-Z0-9_]* ;  

WS : [ \t\f\r\n]+ -> skip ; // skip spaces, tabs

ERROR_CHAR: .;

////////////////////////////// PARSER //////////////////////////////

// Expression

expr: LB expr_list? RB 
    | LP expr RP 
    | INT_LIT | FLOAT_LIT | STRING_LIT 
    | ID
    | expr MEM_ACC ID 
    | func_call
    | expr (INC_OP | DEC_OP)
    | <assoc=right> (INC_OP | DEC_OP) expr
    | <assoc=right> (LO_NOT | SUB_OP | ADD_OP) expr
    | expr (MUL_OP | DIV_OP | MOD_OP) expr
    | expr (ADD_OP | SUB_OP) expr
    | expr (LESS_OP | LEQ_OP | GREAT_OP | GEQ_OP) expr
    | expr (EQ_OP | NOTEQ_OP) expr
    | expr LO_AND expr
    | expr LO_OR expr
    | <assoc=right> expr ASSIGN expr ;

expr_list: expr (COMMA expr)* ;

// Function
param: (INT_KW | FLOAT_KW | STRING_KW | ID) ID ;

// Struct
struct_decl: STRUCT ID LB (param SEMICOLON)* 
             RB SEMICOLON ;

func_decl: (INT_KW | FLOAT_KW | STRING_KW | ID | VOID)? 
           ID LP (param (COMMA param)*)? RP block_stmt ;

func_call: ID LP expr_list? RP ;

// Statements
stmt: decl_stmt
    | block_stmt
    | if_stmt
    | while_stmt
    | for_stmt
    | switch_stmt
    | (BREAK | CONTINUE) SEMICOLON
    | RETURN expr? SEMICOLON
    | expr SEMICOLON ;

decl_stmt: (INT_KW | FLOAT_KW | STRING_KW | ID | AUTO) 
            ID (ASSIGN expr)? SEMICOLON ;

block_stmt: LB stmt* RB ;

// ANTLR is very convenient, in the sense that
// it groups "else" to the nearest "if" so yayyy
if_stmt: IF LP expr RP stmt (ELSE stmt)? ;

while_stmt: WHILE LP expr RP stmt ;

for_init: decl_stmt | expr SEMICOLON ;
for_updt: expr ;

for_stmt: FOR LP 
                (for_init | SEMICOLON)
                expr? SEMICOLON
                for_updt?
              RP 
          stmt ; 

sw_case: CASE expr COLON stmt* ;
sw_def: DEFAULT COLON stmt* ;

switch_stmt: SWITCH LP expr RP LB sw_case* sw_def? RB ;

