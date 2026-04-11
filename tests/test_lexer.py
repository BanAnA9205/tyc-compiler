"""
Lexer test cases for TyC compiler
"""

import pytest

from tests.utils import Tokenizer


def assert_tokens(source: str, 
                  expected_tokens: str) -> None:
    tokenizer = Tokenizer(source)
    tokens = tokenizer.get_tokens_as_string()

    assert tokens == expected_tokens


def test_lexer_001():
    source = "int main() { return 0; }"
    expected_tokens = "int,main,(,),{,return,0,;,},<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_002():
    source = "auto break case continue default else float for if int return string struct switch void while"
    expected_tokens = (
        "auto,break,case,continue,default,else,"
        "float,for,if,int,return,string,struct,"
        "switch,void,while,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_003():
    source = "_x x1 X_2 a_b9"
    expected_tokens = "_x,x1,X_2,a_b9,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_004():
    source = "Auto Int String"
    expected_tokens = "Auto,Int,String,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_005():
    source = "{ } ( ) ; , :"
    expected_tokens = "{,},(,),;,,,:,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_006():
    source = "+ - * / % == != < > <= >= || && ! ++ -- = ."
    expected_tokens = (
        "+,-,*,/,%,==,!=,<,"
        ">,<=,>=,||,&&,!,++,--,"
        "=,.,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_007():
    source = "a<=b>=c==d!=e&&f||g"
    expected_tokens = (
        "a,<=,b,>=,c,==,d,!=,e,"
        "&&,f,||,g,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_008():
    source = "p.x.y"
    expected_tokens = "p,.,x,.,y,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_009():
    source = "x=1+2*3-4/5%6;"
    expected_tokens = (
        "x,=,1,+,2,*,3,-,"
        "4,/,5,%,6,;,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_010():
    source = "++x; x--; !x;"
    expected_tokens = (
        "++,x,;,x,--,;,!,x,;,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_011():
    source = "int x; // comment\nfloat y; int z; /* comment\nmore */ float w;"
    expected_tokens = (
        "int,x,;,float,y,;,int,z,;,"
        "float,w,;,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_012():
    source = "int a = 5;;"
    expected_tokens = "int,a,=,5,;,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_013():
    source = "// comment /* not block\nint x; /* comment // not line */ int y;"
    expected_tokens = "int,x,;,int,y,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_014():
    source = "int a = \xf6\xfc Project ;"
    assert_tokens(source, "int,a,=,Error Token \xf6")


def test_lexer_015():
    source = "/* outer /* inner */ int x; int/*c*/y;"
    expected_tokens = "int,x,;,int,y,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_016():
    source = "/* string s1 = \" \xf6\xfc \"; */\n" \
             "string s2 = \" \xf6\xfc Project \";\n" \
             "string s3 = \" touhou \";\n" \
             "// string s4 = \" \xf6\xfc Project \" ;\n"
    expected_tokens = "string,s2,=, \xf6\xfc Project ,;," \
                      "string,s3,=, touhou ,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_017():
    source = "int\tx\n=\t5; int x\r\f=1;"
    expected_tokens = (
        "int,x,=,5,;,int,x,=,1,"
        ";,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_018():
    source = "int a = -69; int b = --69; " \
             "int c = ---69; int d = ----69;" \
             "int e = +69; int f = ++69; " \
             "int g = +++69; int h = ++++69;"
    expected_tokens = (
        "int,a,=,-,69,;,"
        "int,b,=,--,69,;,"
        "int,c,=,--,-,69,;,"
        "int,d,=,--,--,69,;,"
        "int,e,=,+,69,;,"
        "int,f,=,++,69,;,"
        "int,g,=,++,+,69,;,"
        "int,h,=,++,++,69,;,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_019():
    source = "/*a*/ //b\n\nint y;"
    expected_tokens = "int,y,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_020():
    source = "intx auto_1 _auto"
    expected_tokens = "intx,auto_1,_auto,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_021():
    source = "0 123 999"
    expected_tokens = "0,123,999,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_022():
    source = "x=-45;"
    expected_tokens = "x,=,-,45,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_023():
    source = "007"
    expected_tokens = "007,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_024():
    source = "0.0 3.14 1. .5 1e4 2E-3 5.67E+2 1.2e-3 10e2"
    expected_tokens = (
        "0.0,3.14,1.,.5,1e4,2E-3,"
        "5.67E+2,1.2e-3,10e2,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_025():
    source = "string s = \"hello world\n"
    assert_tokens(source, "string,s,=,Unclosed String: hello world")


def test_lexer_026():
    source = "{ { { int x; } { float y; { string s; } } } auto v={{1,2},{3,4}}; }"
    expected_tokens = (
        "{,{,{,int,x,;,},{,float,y,;,{,"
        "string,s,;,},},},auto,v,=,{,{,1,"
        ",,2,},,,{,3,,,4,},},;,},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_027():
    source = "a+++++b--/**/--c"
    expected_tokens = "a,++,++,+,b,--,--,c,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_028():
    source = "struct S{int x;}; { { S s; s.x=1; { { s.x = s.x + 1; } } } }"
    expected_tokens = (
        "struct,S,{,int,x,;,},;,{,{,S,s,;,"
        "s,.,x,=,1,;,{,{,s,.,x,=,s,"
        ".,x,+,1,;,},},},},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_029():
    source = "printString(\"/*\\\"//\\\"*/\"); // line\n{ { { } } }"
    expected_tokens = (
        "printString,(,/*\\\"//\\\"*/,),;,{,{,{,},},},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_030():
    source = "a=b+++c-- - --d; x=1..2; y=.5e+2+1e2; z=(a&&b)||!c; f(g(1,2),{3,{4,5}});"
    expected_tokens = (
        "a,=,b,++,+,c,--,-,--,d,;,"
        "x,=,1.,.2,;,y,=,.5e+2,+,"
        "1e2,;,z,=,(,a,&&,b,),||,!,c,"
        ";,f,(,g,(,1,,,2,),,,{,3,,,"
        "{,4,,,5,},},),;,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_031():
    source = "{ { { int i; } } while(i<10){i++;} } //c\nstruct A{int x;}; A a; a.x=--i;"
    expected_tokens = (
        "{,{,{,int,i,;,},},while,(,i,<,10,"
        "),{,i,++,;,},},struct,A,{,int,x,;,"
        "},;,A,a,;,a,.,x,=,--,i,;,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_032():
    source = "switch(x){case 1: y=1; case 2: {y=2;}} default: y=3;"
    expected_tokens = (
        "switch,(,x,),{,case,1,:,y,=,1,;,"
        "case,2,:,{,y,=,2,;,},},default,:,"
        "y,=,3,;,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_033():
    source = "1+2.0+3e4"
    expected_tokens = "1,+,2.0,+,3e4,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_034():
    source = "1..2"
    expected_tokens = "1.,.2,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_035():
    source = "\"\" \"a\\tb\" \"//\" \"/*x*/\" \"C:\\\\p\\\\f\""
    expected_tokens = (
        ",a\\tb,//,/*x*/,C:\\\\p\\\\f,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_036():
    source = "for(;;){} for(;i<1;){} for(i=0;;i++){} for(; ; ++i){}"
    expected_tokens = (
        "for,(,;,;,),{,},"
        "for,(,;,i,<,1,;,),{,},"
        "for,(,i,=,0,;,;,i,++,),{,},"
        "for,(,;,;,++,i,),{,},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_037():
    source = "if(a) if(b) c=1; else c=2; while(a){ if(!b) break; else continue; } return;"
    expected_tokens = (
        "if,(,a,),if,(,b,),c,=,1,;,"
        "else,c,=,2,;,while,(,a,),{,if,(,"
        "!,b,),break,;,else,continue,;,},"
        "return,;,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_038():
    source = "switch(x){case 0: break; default: return;} struct T{int x;}; void f(){return;}"
    expected_tokens = (
        "switch,(,x,),{,case,0,:,break,;,"
        "default,:,return,;,},struct,T,{,int,x,"
        ";,},;,void,f,(,),{,return,;,},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_039():
    source = "struct Node{int v; Node next;}; Node n; while(n!=0){n=n.next;}"
    expected_tokens = (
        "struct,Node,{,int,v,;,Node,next,;,},;,"
        "Node,n,;,while,(,n,!=,0,),{,n,=,n,"
        ".,next,;,},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_040():
    source = "for(;;){switch(x){case 1: if(y) break; else continue; default: {return;}}}"
    expected_tokens = (
        "for,(,;,;,),{,switch,(,x,),{,case,1"
        ",:,if,(,y,),break,;,else,continue,;,default"
        ",:,{,return,;,},},},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_041():
    source = (
        "struct Person{string name; int age;}; "
        "void main(){Person p={\"Bob\",30}; p.age=p.age+1; printString(p.name);}"
    )
    expected_tokens = (
        "struct,Person,{,string,name,;,int,age,;,},"
        ";,void,main,(,),{,Person,p,=,{,Bob,,,"
        "30,},;,p,.,age,=,p,.,age,+,1,"
        ";,printString,(,p,.,name,),;,},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_042(): # stress test 1
    depth = 100
    source = "".join(["{" for _ in range(depth)]) + "int x;" + "".join(["}" for _ in range(depth)])
    tokens = []
    for _ in range(depth):
        tokens.extend(["{"])
    tokens.extend(["int", "x", ";"])
    for _ in range(depth):
        tokens.extend(["}"])
    tokens.append("<EOF>")
    expected_tokens = ",".join(tokens)
    assert_tokens(source, expected_tokens)


def test_lexer_043(): # stress test 2
    depth = 5
    repeats = 4

    def build_tree(level: int) -> str:
        if level == 0:
            return "".join(["if(a){b++;}" for _ in range(repeats)])
        return "".join(["{" + build_tree(level - 1) + "}" for _ in range(repeats)])

    source = build_tree(depth)

    def tokens_for_tree(level: int) -> list[str]:
        if level == 0:
            leaf_tokens = []
            for _ in range(repeats):
                leaf_tokens.extend([
                    "if", "(", "a", ")", "{", "b",
                    "++", ";", "}",
                ])
            return leaf_tokens

        node_tokens = []
        for _ in range(repeats):
            node_tokens.extend(["{"])
            node_tokens.extend(tokens_for_tree(level - 1))
            node_tokens.extend(["}"])
        return node_tokens

    tokens = tokens_for_tree(depth)
    tokens.append("<EOF>")
    expected_tokens = ",".join(tokens)
    assert_tokens(source, expected_tokens)


def test_lexer_044():
    source = "auto s = \"bad\\a\""
    assert_tokens(source, "auto,s,=,Illegal Escape In String: bad\\a")


def test_lexer_045():
    source = "string s = \"ok\\n\\q\""
    assert_tokens(source, "string,s,=,Illegal Escape In String: ok\\n\\q")


def test_lexer_046():
    source = "string s = \"unclosed\n"
    assert_tokens(source, "string,s,=,Unclosed String: unclosed")


def test_lexer_047():
    source = "int x = 1; string s = \"unclosed\r"
    assert_tokens(source, "int,x,=,1,;,string,s,=,Unclosed String: unclosed")


def test_lexer_048():
    source = "\"unclosed"
    assert_tokens(source, "Unclosed String: unclosed")


def test_lexer_049():
    source = "x = \"bad\\q\n\""
    assert_tokens(source, "x,=,Illegal Escape In String: bad\\q")


def test_lexer_050():
    source = "x = \"bad\\\n\""
    assert_tokens(source, "x,=,Unclosed String: bad\\")


def test_lexer_051():
    source = "x = @"
    assert_tokens(source, "x,=,Error Token @")


def test_lexer_052():
    source = "x = $"
    assert_tokens(source, "x,=,Error Token $")


def test_lexer_053():
    source = "struct Point { int x; int y; };"
    expected_tokens = (
        "struct,Point,{,int,x,;,int,y,;,"
        "},;,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_054():
    source = "struct Empty {};"
    expected_tokens = "struct,Empty,{,},;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_055():
    source = "struct B { A a; };"
    expected_tokens = "struct,B,{,A,a,;,},;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_056():
    source = "int add(int x, int y){return x+y;}"
    expected_tokens = (
        "int,add,(,int,x,,,int,y,),{,return,"
        "x,+,y,;,},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_057():
    source = "add(int x){return x;}"
    expected_tokens = "add,(,int,x,),{,return,x,;,},<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_058():
    source = "void main(){return;}"
    expected_tokens = "void,main,(,),{,return,;,},<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_059():
    source = "auto x = 1;"
    expected_tokens = "auto,x,=,1,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_060():
    source = "Point p;"
    expected_tokens = "Point,p,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_061():
    source = "Point3D p = {{1,2},{3,4}};"
    expected_tokens = (
        "Point3D,p,=,{,{,1,,,2,},,,{,"
        "3,,,4,},},;,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_062():
    source = "p.pos.x = p.pos.x + 1;"
    expected_tokens = (
        "p,.,pos,.,x,=,p,.,pos,.,x,"
        "+,1,;,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_063():
    source = "if(x) if(y) z=1; else z=2;"
    expected_tokens = (
        "if,(,x,),if,(,y,),z,=,1,;,"
        "else,z,=,2,;,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_064():
    source = "while(i<10){ if(i%2==0){i++;continue;} i++; }"
    expected_tokens = (
        "while,(,i,<,10,),{,if,(,i,%,"
        "2,==,0,),{,i,++,;,continue,"
        ";,},i,++,;,},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_065():
    source = "for(;i<10;){for(j=0;j<2;j++){} i++;}"
    expected_tokens = (
        "for,(,;,i,<,10,;,),{,for,(,"
        "j,=,0,;,j,<,2,;,j,++,"
        "),{,},i,++,;,},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_066():
    source = "for(int i=10; i>=0; --i) { }"
    expected_tokens = (
        "for,(,int,i,=,10,;,i,>=,0,"
        ";,--,i,),{,},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_067():
    source = "switch(x){case 1: {y=1;} case 2: y=2; default: {break;} }"
    expected_tokens = (
        "switch,(,x,),{,case,1,:,{,y,=,1,"
        ";,},case,2,:,y,=,2,;,default,"
        ":,{,break,;,},},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_068():
    source = "{ int x; { float y; { string s; } } }"
    expected_tokens = (
        "{,int,x,;,{,float,y,;,{,string,"
        "s,;,},},},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_069():
    source = "a&&b||c&&(!d||e)"
    expected_tokens = "a,&&,b,||,c,&&,(,!,d,||,e,),<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_070():
    source = "a<=b/*c*/>=c//d\n<e"
    expected_tokens = (
        "a,<=,b,>=,c,<,e,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_071():
    source = "a=b.c=d;"
    expected_tokens = "a,=,b,.,c,=,d,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_072():
    source = "++a--;"
    expected_tokens = "++,a,--,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_073():
    source = "a.b.c.d++;"
    expected_tokens = "a,.,b,.,c,.,d,++,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_074():
    source = "f(g(1,2), {3,4}, h());"
    expected_tokens = (
        "f,(,g,(,1,,,2,),,,{,3,,,4,"
        "},,,h,(,),),;,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_075():
    source = "printString(\"\\\\\"//\\\"\");"
    expected_tokens = "printString,(,\\\\,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_076():
    source = "printString(\"/*//*/\");"
    expected_tokens = "printString,(,/*//*/,),;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_077():
    source = "string s=\"line1\\nline2\";"
    expected_tokens = "string,s,=,line1\\nline2,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_078():
    source = "string s=\"a\\\\\";"
    expected_tokens = "string,s,=,a\\\\,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_079():
    source = "auto s = \"bad\\q\r\""
    assert_tokens(source, "auto,s,=,Illegal Escape In String: bad\\q")


def test_lexer_080():
    source = "int x = 1 @ 2;"
    assert_tokens(source, "int,x,=,1,Error Token @")


def test_lexer_081():
    source = "string s = \"abc\\n"
    assert_tokens(source, "string,s,=,Unclosed String: abc\\n")


def test_lexer_082():
    source = "string s = \"a\\tb\\zc\""
    assert_tokens(source, "string,s,=,Illegal Escape In String: a\\tb\\z")


def test_lexer_083():
    source = "/*c1*/int/*c2*/x/*c3*/=/*c4*/1/*c5*/;/*c6*/"
    expected_tokens = "int,x,=,1,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_084():
    source = "auto_auto auto autoauto _auto auto1"
    expected_tokens = "auto_auto,auto,autoauto,_auto,auto1,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_085():
    source = "0.0e+0 123456789012345 9e9 7.0e-10"
    expected_tokens = (
        "0.0e+0,123456789012345,9e9,7.0e-10,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_086():
    source = "{{({})}}"
    expected_tokens = "{,{,(,{,},),},},<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_087():
    source = "1.0.2"
    expected_tokens = "1.0,.2,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_088():
    source = ".5e+2"
    expected_tokens = ".5e+2,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_089():
    source = "1e+2.3"
    expected_tokens = "1e+2,.3,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_090():
    source = "0..5"
    expected_tokens = "0.,.5,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_091():
    source = "a+++b-- - --c"
    expected_tokens = "a,++,+,b,--,-,--,c,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_092():
    source = "a/*/b*/c"
    expected_tokens = "a,c,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_093():
    source = "/*a*/\"str\"/*b*/"
    expected_tokens = "str,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_094():
    source = "/*a*/ //b\n\"x\""
    expected_tokens = "x,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_095():
    source = "switch(x){case 1: case 2: y=3;}"
    expected_tokens = (
        "switch,(,x,),{,case,1,:,case,2,:,"
        "y,=,3,;,},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_096():
    source = "f({{1,2},3}, g({4,5}));"
    expected_tokens = (
        "f,(,{,{,1,,,2,},,,3,},,,g,"
        "(,{,4,,,5,},),),;,<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_097():
    source = "int main(){for(i=0;i<2;i++){if(i==1){printString(\"one\");}else{printString(\"zero\");}}}"
    expected_tokens = (
        "int,main,(,),{,for,(,i,=,0,;,i,"
        "<,2,;,i,++,),{,if,(,i,==,1,"
        "),{,printString,(,one,),;,},else,{,printString,"
        "(,zero,),;,},},},<EOF>"
    )
    assert_tokens(source, expected_tokens)


def test_lexer_098():
    source = "string s=\"\\b\\f\\r\\n\\t\\\"\\\\\";"
    expected_tokens = "string,s,=,\\b\\f\\r\\n\\t\\\"\\\\,;,<EOF>"
    assert_tokens(source, expected_tokens)


def test_lexer_099():
    source = "string s = \"bad\\x"
    assert_tokens(source, "string,s,=,Illegal Escape In String: bad\\x")


def test_lexer_100():
    source = "/*hdr*/struct S{int x;}; auto v={{1,2},{3,4}}; if(a&&b||!c){f(g(1,2),h(3,4));}"
    expected_tokens = (
        "struct,S,{,int,x,;,},;,auto,v,=,"
        "{,{,1,,,2,},,,{,3,,,4,},},"
        ";,if,(,a,&&,b,||,!,c,),{,f,(,g,"
        "(,1,,,2,),,,h,(,3,,,4,),),;"
        ",},<EOF>"
    )
    assert_tokens(source, expected_tokens)


