"""
Test cases for TyC Static Semantic Checker

This module contains test cases for the static semantic checker.
100 test cases covering all error types and comprehensive scenarios.
"""

from tests.utils import Checker
from src.utils.nodes import (
    Program,
    FuncDecl,
    BlockStmt,
    VarDecl,
    AssignExpr,
    ExprStmt,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    Identifier,
    BinaryOp,
    MemberAccess,
    FuncCall,
    StructDecl,
    MemberDecl,
    Param,
    ReturnStmt,
)

def test_valid_programs():
    valid_sources = [
        """
void main() {
    int x = 5;
    int y = x + 1;
}
""",
        """
void main() {
    auto x = 10;
    auto y = 3.14;
    auto z = x + y;
}
""",
        """
int add(int x, int y) {
    return x + y;
}
void main() {
    int sum = add(5, 3);
}
""",
        """
struct Point {
    int x;
    int y;
};
void main() {
    Point p;
    p.x = 10;
    p.y = 20;
}
""",
        """
void main() {
    int x = 10;
    {
        int y = 20;
        int z = x + y;
    }
}
""",
        """
    struct P {
        int x;
        int y;
        float z;
        string t;
    };

    void main() {
        P p;
        p = {1, 2, 3.0, "hello"};
    }   
    """,
        """
    struct Point {
        float x; 
        float y;
    };

    foo(Point p, Point q) {
        p = q;
        return p;
    }
    void main() {}
    """,
        """
    struct Inside {
        int x;
        int y;
    };

    struct Outside {
        Inside i;
        float f;
        string t;
    };

    void main() {
        Outside o = {{1, 2}, 3.14, "hello"};
    }
    """,
        """
    foo(int a, float b){
        return a + b;
    }

    void main() {
        auto x;
        x = foo(1, 2.0);
        printFloat(x);

        auto y = (x = foo(2, 1.0)) + 3;
        printFloat(y);
    }
    """,
        """
    struct S1 {
        int x;
        float y;
    };
    
    struct S2 {
        float x;
        int y;
    };

    int m() {
        S1 s1 = {1, 2.0};
        S2 s2;
        s1.x = (s2 = {1.0, 2}).y;
        return s1.x;
    }
    void main() {}
    """,
        """
    struct S {
        int x; int y; int z;
    };

    foo(S s) {
        return (!s.x) + (s.y && 1) - (s.z || 2)
               * (s.x < 3 && s.x <= 3) / (s.y > 4 && s.y >= 4)
               % (s.z == 5 || s.z != 6) + s.x++ - --s.y;
    }

    int m() {
        S s = {1, 2, 3};
        auto x = (s.x = foo(s)) + (s.y = foo(s)) + (s.z = foo(s));

        return x;
    }
    void main() {}
    """,
        """
    void main() {return;}
    """,
        """
    int m() {
        auto x;
        auto y = x + 5;
        return x - y;
    }
    void main() {}
    """,
        """
    struct foo {
        int a; int b;
    };

    int foo(int a, int b){
        return a * b;
    }

    void main() {
        foo f = {foo(1, 2), foo(3, 4)};
    }
    """,
        """
    void main() {
        int x = 10;
        {
            float x = 3.14;
        }
    }
    """,
        """
    struct Inner { int x; };
    struct Outer { Inner i; float y; };
    void main() {
        Outer o = {{1}, 2.0};
        o.i.x = 5;
    }
    """,
        """
    void main() {
        auto x;
        x++;
        int y = x;
    }
    """,
        """
    void main() {
        float z = ((3.14 + 5) * 2.0) / 1;
        auto x = 5;
        float y = x + z;
    }
    """,
        """
    void main() {
        for (int i = 0; i < 5; i++) {
            int a = i;
        }
        for (i = 0; i < 5; i++) {
            float a = 1.0;
        }
    }
    """,
        """
    fact(int n) {
        if (n <= 1) { return 1.0; }
        return n * fact(n - 1);
    }
    void main() {}
    """,
        """
    void main() {
        auto a;
        switch (a) {
            case 1: { break; }
            case 2: { break; }
            default: { break; }
        }
    }
    """,
        """
    foo() { return 5; }
    void main() {
        auto x = foo();
        int y = x;
    }
    """,
        """
    struct S { int x; };
    void main() {
        S s_obj1;
        S s_obj2;
        s_obj1.x = 10;
        s_obj2.x = s_obj1.x + 5;
    }
    """,
        """
    void main() { switch (1) { case 1: break; } }
    """,
        """
    void main() { auto x; if (x) {} }
    """,
        """
    void main() { auto x; while (x) {} }
    """,
        """
    void main() { auto x; for (int i=0; x; i++) {} }
    """,
        """
    void main() { auto x; switch(x) { case 1: break; } }
    """,
        """
    void main() {
    }
    """,
        """
    void main() {
        while (1) {
            switch(1) {
                case 1: continue;
            }
        }
    }
    """,
        """
    void main() {
        int x = 1;
        {
            float x = 2.0;
        }
    }
    """,
        """
    struct Data { int x; };
    Data Data(Data Data) { return Data; }
    void main() {}
    """,
        """
    void main() {
        int x;
        x = x + 1; 
    }
    """,
        """
    int a() { return 1; }
    struct S { int a; };
    void main() {
        S s = {2};
        int x = s.a; 
    }
    """,
        """
    struct Node { int x; };
    void main() {
        Node a = {1};
        Node b = a; 
    }
    """,
        """
    void main() {
        auto x;
        auto y;
        int z = (x = (y = 5));
    }
    """,
        """
    struct T { int u; };
    T t() { return {1}; } // return struct literal 
    void main() {}
    """,
        """
    void main() {
        int a = 1;
        if (a = a + 1) {}
    }
    """,
        """
    void main() {
        for(int i=0; i<1; i++) break;
    }
    """,
        """
    void foo() { return; }
    void main() {}
    """,
        """
    void main() {
        auto x;
        float f = 1.0;
        int i = 1;
        x = f + i; 
    }
    """,
        """
    void main() {
        int i = 0;
        while (i < 10) {
            if (i == 5) {
                switch(i) {
                    case 5: continue;
                }
            }
        }
    }
    """,
    """
    int calc() {
        auto x;
        float y = (x = 5) + 2.0;
        int z = y >= x++;
        return z;
    }
    void main() {int a = calc();}
    """,
    """
    void main() {
        auto a;
        int x = !a;
    }
    """,
    """
    struct func_map { int struct_map; };
    void struct_map() { int func_map; }
    void main() {}
    """,
    """
    void main() {
        auto a;
        switch(a) { case 1: break; }
    }
    """,
    """
    void step1() {}
    void step2() { step1(); return; }
    void main() {}
    """,
    """
    void main() {
        int x; int y; float z;
        x = y = z >= 1.0;
    }
    """,
    """
    void main() {
        int flag = !!!1;
        float invert = - - -1.5;
    }
    """,
    """
    struct Inner { int data; };
    struct Outer { Inner wrap; };
    void main() {
        Outer o = {{1}};
    }
    """,
    """
    int f(int a, int b, int c) {return a + b + c;}
    void main() {
        int x = f(5, 10, 15);
        return;
    }
    """,
    """
    void main() {
        int resolve = (1 < 2) == (3 >= 4);
    }
    """,
    """
    struct A { int x; };
    struct B { A y; };
    void main() {
        A a; B b;
        a.x = 1; b.y = a;
    }
    """,
    """
    void main() {
        int x = 5;
        if (x == 5) {
            float f = 1.0;
        }
    }
    """,
    """
    void main() {
        auto infinite;
        while(infinite) { break; }
    }
    """,
    """
    void main() {
        { { { int layers; } } }
    }
    """,
    """
    void main() {
        return;
    }
    """,
    """
    void main() {
        for(;;) { { { { break; } } } }
    }
    """,
    """
    void main() {
        while(1) {
            if (1 == 1) {
                break;
            }
        }
    }
    """,
    """
    struct printInt { int runtime; };
    struct printFloat { float env; };
    void main() {}
    """,
    """
    float gen() { return 5.5; }
    void main() {
        float output = 1 + gen();
    }
    """,
    """
    struct Empty {};
    void main() {
        Empty e;
    }
    """,
    """
    void main() {
        int math = 10 % (-2.0 != 3.14);
    }
    """,
    """
    void main() {
        if (1 > 0) {} 
        else if (2 < 1) {} 
        else if (3 == 3) {} 
        else {}
    }
    """,
    """
    void main() {
        auto counter;
        counter++; ++counter;
    }
    """,
    """
    blind() {
        return;
    }
    void main() {
        blind();
    }
    """,
    """
    int map(int x) { return x; }
    void main() {
        int mapped = map(map(map(1)));
    }
    """,
    """
    void main() {
        float grouped = -(+(1.0));
    }
    """,
    """
    void main() {
        auto a;
        int sum = a + 1;
    }
    """,
    """
    struct Prop { int hidden; };
    void main() {
        Prop p;
        p.hidden = 1;
        int expose = p.hidden;
    }
    """,
    """
    void main() {
        { int shed = 1; }
        int shed = 2;
    }
    """,
    """
    void main() {
        printInt(1);
        printFloat(1.5);
        printString("string");
    }
    """,
    """
    void main() {
        auto x; int y;
        y = x; return;
    }
    """,
    """
    void main() {
        auto x;
        int y = x;
    }
    """,
    """
    void main() {
        int x = 2;
        switch (x) {
            case 1:
                int x = 3; // valid shadowing
                break;
            case 2:
                {
                    int x = 4; // valid shadowing
                    break;
                }
        }
    }
    """,
    """
    void main() {
        if (1) int x = 1;
        else int x = 2;
    }
    """,
    """
    void main() {
        auto x;
        if (x + 1) {};
    }
    """
    ]
    for src in valid_sources:
        assert Checker(src).check_from_source() == 'Static checking passed'

# =================================================================== #
# Basic tests for common sense checking                               #
# =================================================================== #

def _assert_error_exact(source: str, expected: str):
    assert Checker(source).check_from_source() == expected


def test_basic_001():
    source = """
    void main() {
        int x;
        int x;
    }
    """
    _assert_error_exact(source, "Redeclared(Variable, x)")


def test_basic_002():
    source = """
    void foo(int x) {
        {
            int x;
        }
    }
    void main() {}
    """
    _assert_error_exact(source, "Redeclared(Variable, x)")


def test_basic_003():
    source = """
    void foo() {}
    int foo() { return 1; }
    void main() {}
    """
    _assert_error_exact(source, "Redeclared(Function, foo)")


def test_basic_004():
    source = """
    struct S { int x; };
    struct S { float y; };
    void main() {}
    """
    _assert_error_exact(source, "Redeclared(Struct, S)")


def test_basic_005():
    source = """
    int add(int a, float a) {
        return 1;
    }
    void main() {}
    """
    _assert_error_exact(source, "Redeclared(Parameter, a)")


def test_basic_006():
    source = """
    struct Point {
        int x;
        int x;
    };
    void main() {}
    """
    _assert_error_exact(source, "Redeclared(Member, x)")


def test_basic_007():
    source = """
    void main() {
        int y = x + 1;
    }
    """
    _assert_error_exact(source, "UndeclaredIdentifier(x)")


def test_basic_008():
    source = """
    void main() {
        int x = x + 1;
    }
    """
    _assert_error_exact(source, "UndeclaredIdentifier(x)")


def test_basic_009():
    source = """
    void main() {
        int y = missingFn();
    }
    """
    _assert_error_exact(source, "UndeclaredFunction(missingFn)")


def test_basic_010():
    source = """
    void main() {
        MissingType v;
    }
    """
    _assert_error_exact(source, "UndeclaredStruct(MissingType)")


def test_basic_011():
    source = """
    void foo(UnknownType p) {}
    void main() {}
    """
    _assert_error_exact(source, "UndeclaredStruct(UnknownType)")


def test_basic_012():
    source = """
    void main() {
        auto x;
    }
    """
    _assert_error_exact(source, "TypeCannotBeInferred(BlockStmt([VarDecl(auto, x)]))")


def test_basic_013():
    source = """
    void main() {
        auto x;
        auto y;
        x = y;
    }
    """
    _assert_error_exact(source, "TypeCannotBeInferred(AssignExpr(Identifier(x) = Identifier(y)))")


def test_basic_014():
    source = """
    void main() {
        auto x;
        auto y;
        int z = x + y;
    }
    """
    _assert_error_exact(source, "TypeCannotBeInferred(BinaryOp(Identifier(x), +, Identifier(y)))")


def test_basic_015():
    source = """
    foo() {
        auto x;
        return x;
    }
    void main() {}
    """
    _assert_error_exact(source, "TypeCannotBeInferred(ReturnStmt(return Identifier(x)))")


def test_basic_016():
    source = """
    void main() {
        auto x = {1};
    }
    """
    _assert_error_exact(source, "TypeCannotBeInferred(VarDecl(auto, x = StructLiteral({IntLiteral(1)})))")


def test_basic_017():
    source = """
    void main() {
        if (1.0) {
        }
    }
    """
    _assert_error_exact(source, "TypeMismatchInStatement(IfStmt(if FloatLiteral(1.0) then BlockStmt([])))")


def test_basic_018():
    source = """
    void main() {
        while ("loop") {
        }
    }
    """
    _assert_error_exact(source, "TypeMismatchInStatement(WhileStmt(while StringLiteral('loop') do BlockStmt([])))")


def test_basic_019():
    source = """
    void main() {
        for (int i = 0; 1.5; i++) {
        }
    }
    """
    _assert_error_exact(source, "TypeMismatchInStatement(ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); FloatLiteral(1.5); PostfixOp(Identifier(i)++) do BlockStmt([])))")


def test_basic_020():
    source = """
    void main() {
        int x;
        x = "hello";
    }
    """
    _assert_error_exact(source, "TypeMismatchInStatement(ExprStmt(AssignExpr(Identifier(x) = StringLiteral('hello'))))")


def test_basic_021():
    source = """
    struct A { int x; };
    struct B { int x; };
    void main() {
        A a;
        B b;
        a = b;
    }
    """
    _assert_error_exact(source, "TypeMismatchInStatement(ExprStmt(AssignExpr(Identifier(a) = Identifier(b))))")


def test_basic_022():
    source = """
    void foo() {
        return 1;
    }
    void main() {}
    """
    _assert_error_exact(source, "TypeMismatchInStatement(ReturnStmt(return IntLiteral(1)))")


def test_basic_023():
    source = """
    int foo() {
        return;
    }
    void main() {}
    """
    _assert_error_exact(source, "TypeMismatchInStatement(ReturnStmt(return))")


def test_basic_024():
    source = """
    void main() {
        switch ("x") {
            case 1:
                break;
        }
    }
    """
    _assert_error_exact(source, "TypeMismatchInStatement(SwitchStmt(switch StringLiteral('x') cases [CaseStmt(case IntLiteral(1): [BreakStmt()])]))")


def test_basic_025():
    source = """
    void main() {
        string s = "a" + "b";
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(BinaryOp(StringLiteral('a'), +, StringLiteral('b')))")


def test_basic_026():
    source = """
    void main() {
        int x = 5 % 2.0;
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(BinaryOp(IntLiteral(5), %, FloatLiteral(2.0)))")


def test_basic_027():
    source = """
    void main() {
        float x = 1.0;
        int y = x && 1;
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(BinaryOp(Identifier(x), &&, IntLiteral(1)))")


def test_basic_028():
    source = """
    void main() {
        string s = "x";
        int y = !s;
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(PrefixOp(!Identifier(s)))")


def test_basic_029():
    source = """
    void main() {
        float x = 1.0;
        ++x;
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(PrefixOp(++Identifier(x)))")


def test_basic_030():
    source = """
    struct S { float f; };
    void main() {
        S s = {1.0};
        s.f--;
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(PostfixOp(MemberAccess(Identifier(s).f)--))")


def test_basic_031():
    source = """
    void main() {
        ++5;
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(PrefixOp(++IntLiteral(5)))")


def test_basic_032():
    source = """
    int foo() { return 1; }
    void main() {
        foo()++;
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(PostfixOp(FuncCall(foo, [])++))")


def test_basic_033():
    source = """
    void main() {
        int x = 1;
        int y = x.member;
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(MemberAccess(Identifier(x).member))")


def test_basic_034():
    source = """
    struct S { int a; };
    void main() {
        S s = {1};
        int y = s.b;
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(MemberAccess(Identifier(s).b))")


def test_basic_035():
    source = """
    int add(int a, int b) { return a + b; }
    void main() {
        int x = add(1);
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(FuncCall(add, [IntLiteral(1)]))")


def test_basic_036():
    source = """
    int add(int a, int b) { return a + b; }
    void main() {
        int x = add(1, 2, 3);
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(FuncCall(add, [IntLiteral(1), IntLiteral(2), IntLiteral(3)]))")


def test_basic_037():
    source = """
    void takesInt(int x) {}
    void main() {
        takesInt(1.5);
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(FuncCall(takesInt, [FloatLiteral(1.5)]))")


def test_basic_038():
    source = """
    struct P { int x; };
    void main() {
        P p = {1, 2};
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(StructLiteral({IntLiteral(1), IntLiteral(2)}))")


def test_basic_039():
    source = """
    struct P { int x; float y; };
    void main() {
        P p = {1.0, 2.0};
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(StructLiteral({FloatLiteral(1.0), FloatLiteral(2.0)}))")


def test_basic_040():
    source = """
    void main() {
        int x;
        int y = (x = 1.5);
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(AssignExpr(Identifier(x) = FloatLiteral(1.5)))")


def test_basic_041():
    source = """
    void main() {
        int x;
        int y = (x = "s");
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(AssignExpr(Identifier(x) = StringLiteral('s')))")


def test_basic_042():
    source = """
    void main() {
        break;
    }
    """
    _assert_error_exact(source, "MustInLoop(BreakStmt())")


def test_basic_043():
    source = """
    void main() {
        continue;
    }
    """
    _assert_error_exact(source, "MustInLoop(ContinueStmt())")


def test_basic_044():
    source = """
    void main() {
        switch (1) {
            case 1:
                continue;
        }
    }
    """
    _assert_error_exact(source, "MustInLoop(ContinueStmt())")


def test_basic_045():
    source = """
    int readInt() { return 1; }
    void main() {}
    """
    _assert_error_exact(source, "Redeclared(Function, readInt)")


def test_basic_046():
    source = """
    struct S { int x; };
    void main() {
        S();
    }
    """
    _assert_error_exact(source, "UndeclaredFunction(S)")


def test_basic_047():
    source = """
    int getX() { return 1; }
    void main() {
        getX = 1;
    }
    """
    _assert_error_exact(source, "UndeclaredIdentifier(getX)")


def test_basic_048():
    source = """
    struct A { int x; };
    void main() {
        A a = {1};
        A b = {2};
        int same = a == b;
    }
    """
    _assert_error_exact(source, "TypeMismatchInExpression(BinaryOp(Identifier(a), ==, Identifier(b)))")


def test_basic_049():
    source = """
    void main() {
        float f = 5;
    }
    """
    _assert_error_exact(source, "TypeMismatchInStatement(VarDecl(FloatType(), f = IntLiteral(5)))")


def test_basic_050():
    source = """
    void main() {
        if (1) {
            break;
        }
    }
    """
    _assert_error_exact(source, "MustInLoop(BreakStmt())")


# =================================================================== #
# Error tests for a variety of scenarios                              #
# =================================================================== #

def test_error_001():
    source = """
    void main() {
        auto x;
        float y;
        if (x || 1) {
            y = 3.14;
        }
        x = y;
    }
    """
    expected = 'TypeMismatchInStatement(ExprStmt(AssignExpr(Identifier(x) = Identifier(y))))'
    assert Checker(source).check_from_source() == expected

def test_error_002():
    source = """
    void main() {
        int x = 1;
        if ({1, 2} == {3, 4}) {
            x = 2;
        }
    }
    """
    expected = 'TypeMismatchInExpression(BinaryOp(StructLiteral({IntLiteral(1), IntLiteral(2)}), ==, StructLiteral({IntLiteral(3), IntLiteral(4)})))'
    assert Checker(source).check_from_source() == expected

def test_error_003():
    source = """
    void main() {
        while (1 + 2 + 3 == 6) {
            int x;
            readInt(x); printInt(x);
            float y;
            readFloat(y); printFloat(y);
            string z;
            readString(z); printString(z);  
        }
    }
    """
    expected = 'TypeMismatchInExpression(FuncCall(readInt, [Identifier(x)]))'
    assert Checker(source).check_from_source() == expected

def test_error_004():
    source = """
    struct Point {
        float x; 
        float y;
    };

    foo(Point p, Point q) {
        p = q;
        return p;
    }

    void main() {
        Point p = {1.2, 3.4};
        foo(p, {5.6, 7.8});

        return 1;
    }
    """
    expected = 'TypeMismatchInStatement(ReturnStmt(return IntLiteral(1)))'
    assert Checker(source).check_from_source() == expected

def test_error_005():
    source = """
    struct Inside {
        int x;
    };

    void main() {
        Inside x = {3};
        auto y = x.x + 1;
        float z = y;
    }
    """
    expected = 'TypeMismatchInStatement(VarDecl(FloatType(), z = Identifier(y)))'
    assert Checker(source).check_from_source() == expected

def test_error_006():
    source = """
    int main() {
        float x = 3.14;
        {
            int y = 1;
            int x = y;
        }
        return x;
    }
    """
    expected = 'TypeMismatchInStatement(ReturnStmt(return Identifier(x)))'
    assert Checker(source).check_from_source() == expected

def test_error_007():
    source = """
    foo() {bar();}
    bar() {foo();}
    """
    expected = 'UndeclaredFunction(bar)'
    assert Checker(source).check_from_source() == expected

def test_error_008():
    source = """
    struct S1 {
        int x;
        float y;
    };
    
    struct S2 {
        float x;
        int y;
    };

    void main() {
        S1 s1; S2 s2;
        s1 = s2;
    }
    """
    expected = 'TypeMismatchInStatement(ExprStmt(AssignExpr(Identifier(s1) = Identifier(s2))))'
    assert Checker(source).check_from_source() == expected

def test_error_009():
    source = """
    foo(int a, int b, int c) {
        for (int i = 0; i <= 10; i++) {
            int x = b + c;
            while (i <= 5) {
            {
                int a = x;
            }
            }
        }
    }
    """
    expected = 'Redeclared(Variable, a)'
    assert Checker(source).check_from_source() == expected

def test_error_010():
    source = """
    foo(string a, string b) {
        return a == b;
    }
    """
    expected = 'TypeMismatchInExpression(BinaryOp(Identifier(a), ==, Identifier(b)))'
    assert Checker(source).check_from_source() == expected

def test_error_011():
    source = """
    void main() {
        auto x;
        auto y;
        x = y;
    }
    """
    expected = 'TypeCannotBeInferred(AssignExpr(Identifier(x) = Identifier(y)))'
    assert Checker(source).check_from_source() == expected

def test_error_012():
    source = """
    struct S { int a; };
    void main() {
        auto x;
        x = {1};
    }
    """
    expected = 'TypeCannotBeInferred(AssignExpr(Identifier(x) = StructLiteral({IntLiteral(1)})))'
    assert Checker(source).check_from_source() == expected

def test_error_013():
    source = """
    void main() {
        Missing s;
    }
    """
    expected = 'UndeclaredStruct(Missing)'
    assert Checker(source).check_from_source() == expected

def test_error_014():
    source = """
    void main() {
        int x;
        float x;
    }
    """
    expected = 'Redeclared(Variable, x)'
    assert Checker(source).check_from_source() == expected

def test_error_015():
    source = """
    void main() {}
    void main() {}
    """
    expected = 'Redeclared(Function, main)'
    assert Checker(source).check_from_source() == expected

def test_error_016():
    source = """
    struct S { int x; };
    struct S { float y; };
    void main() {}
    """
    expected = 'Redeclared(Struct, S)'
    assert Checker(source).check_from_source() == expected

def test_error_017():
    source = """
    void main() {
        int x = 1 + 2.0;
    }
    """
    expected = 'TypeMismatchInStatement(VarDecl(IntType(), x = BinaryOp(IntLiteral(1), +, FloatLiteral(2.0))))'
    assert Checker(source).check_from_source() == expected

def test_error_018():
    source = """
    void main() {
        string s = "hello";
        !s;
    }
    """
    expected = 'TypeMismatchInExpression(PrefixOp(!Identifier(s)))'
    assert Checker(source).check_from_source() == expected

def test_error_019():
    source = """
    struct S { int a; };
    void main() {
        S s1;
        S s2;
        s1 / s2;
    }
    """
    expected = 'TypeMismatchInExpression(BinaryOp(Identifier(s1), /, Identifier(s2)))'
    assert Checker(source).check_from_source() == expected

def test_error_020():
    source = """
    void main() {
        auto x;
        auto y;
        int z = x + y;
    }
    """
    expected = 'TypeCannotBeInferred(BinaryOp(Identifier(x), +, Identifier(y)))'
    assert Checker(source).check_from_source() == expected

def test_error_021():
    source = """
    struct S { int a; };
    void main() {
        S s;
        int x = s.b;
    }
    """
    expected = 'TypeMismatchInExpression(MemberAccess(Identifier(s).b))'
    assert Checker(source).check_from_source() == expected

def test_error_022():
    source = """
    foo(int a) {}
    void main() {
        foo(2.0);
    }
    """
    expected = 'TypeMismatchInExpression(FuncCall(foo, [FloatLiteral(2.0)]))'
    assert Checker(source).check_from_source() == expected

def test_error_023():
    source = """
    foo(int a) {}
    void main() {
        foo();
    }
    """
    expected = 'TypeMismatchInExpression(FuncCall(foo, []))'
    assert Checker(source).check_from_source() == expected

def test_error_024():
    source = """
    struct S { int a; };
    void main() {
        S s = {3.14};
    }
    """
    expected = 'TypeMismatchInExpression(StructLiteral({FloatLiteral(3.14)}))'
    assert Checker(source).check_from_source() == expected

def test_error_025():
    source = """
    void main() {
        string t = "test";
        switch (t) {}
    }
    """
    expected = 'TypeMismatchInStatement(SwitchStmt(switch Identifier(t) cases []))'
    assert Checker(source).check_from_source() == expected

def test_error_026():
    source = """
    void main() { auto x; }
    """
    expected = 'TypeCannotBeInferred(BlockStmt([VarDecl(auto, x)]))'
    assert Checker(source).check_from_source() == expected

def test_error_027():
    source = """
    void main() { float x = 2.0; !x; }
    """
    expected = 'TypeMismatchInExpression(PrefixOp(!Identifier(x)))'
    assert Checker(source).check_from_source() == expected

def test_error_028():
    source = """
    void main() {
        int x = 5.0;
    }
    """
    expected = 'TypeMismatchInStatement(VarDecl(IntType(), x = FloatLiteral(5.0)))'
    assert Checker(source).check_from_source() == expected

def test_error_029():
    source = """
    void main() {
        float f = 5;
    }
    """
    expected = 'TypeMismatchInStatement(VarDecl(FloatType(), f = IntLiteral(5)))'
    assert Checker(source).check_from_source() == expected

def test_error_030():
    source = """
    void main() {
        auto x; auto y;
        int z = x || y;
        x = 1.0; 
    }
    """
    expected = 'TypeMismatchInStatement(ExprStmt(AssignExpr(Identifier(x) = FloatLiteral(1.0))))'
    assert Checker(source).check_from_source() == expected

def test_error_031():
    source = """
    void main() {
        auto x; auto y;
        int z = x < y;
    }
    """
    expected = 'TypeCannotBeInferred(BinaryOp(Identifier(x), <, Identifier(y)))'
    assert Checker(source).check_from_source() == expected

def test_error_032():
    source = """
    void foo(int x) {
        {
            float x = 5.0; 
        }
    }
    void main() {}
    """
    expected = 'Redeclared(Variable, x)'
    assert Checker(source).check_from_source() == expected

def test_error_033():
    source = """
    void main() {
        auto x;
        int y = x; 
        float z = x; 
    }
    """
    expected = 'TypeMismatchInStatement(VarDecl(FloatType(), z = Identifier(x)))'
    assert Checker(source).check_from_source() == expected

def test_error_034():
    source = """
    void main() {
        auto x = {1, 2};
    }
    """
    expected = 'TypeCannotBeInferred(VarDecl(auto, x = StructLiteral({IntLiteral(1), IntLiteral(2)})))'
    assert Checker(source).check_from_source() == expected

def test_error_035():
    source = """
    void foo() {
        return 5;
    }
    void main() {}
    """
    expected = 'TypeMismatchInStatement(ReturnStmt(return IntLiteral(5)))'
    assert Checker(source).check_from_source() == expected

def test_error_036():
    source = """
    void main() {
        auto x;
        auto y = -x; 
    }
    """
    expected = 'TypeCannotBeInferred(PrefixOp(-Identifier(x)))'
    assert Checker(source).check_from_source() == expected

def test_error_037():
    source = """
    struct Node { int val; };
    void main() {
        Node n = {1};
        int val = n.val;
        int error = n.missing;
    }
    """
    expected = 'TypeMismatchInExpression(MemberAccess(Identifier(n).missing))'
    assert Checker(source).check_from_source() == expected

def test_error_038():
    source = """
    void main() {
        auto x;
        if (1.0) {}
    }
    """
    expected = 'TypeMismatchInStatement(IfStmt(if FloatLiteral(1.0) then BlockStmt([])))'
    assert Checker(source).check_from_source() == expected

def test_error_039():
    source = """
    void foo() {}
    void main() {
        auto x = foo();
    }
    """
    expected = 'TypeMismatchInStatement(VarDecl(auto, x = FuncCall(foo, [])))'
    assert Checker(source).check_from_source() == expected

def test_error_040():
    source = """
    struct A { int x; float y; };
    void main() {
        A a = {1.0, 2.0};
    }
    """
    expected = 'TypeMismatchInExpression(StructLiteral({FloatLiteral(1.0), FloatLiteral(2.0)}))'
    assert Checker(source).check_from_source() == expected

def test_error_041():
    source = """
    void main() {
        auto x;
        {
            x = 2.0; 
        }
        int y = x;
    }
    """
    expected = 'TypeMismatchInStatement(VarDecl(IntType(), y = Identifier(x)))'
    assert Checker(source).check_from_source() == expected

def test_error_042():
    source = """
    void main() {
        auto x;
        float y = !!x;
    }
    """
    expected = 'TypeMismatchInStatement(VarDecl(FloatType(), y = PrefixOp(!PrefixOp(!Identifier(x)))))'
    assert Checker(source).check_from_source() == expected

def test_error_043():
    source = """
    struct A { int x; };
    struct B { A a; };
    void main() {
        auto y = { { 1 } }; 
    }
    """
    expected = 'TypeCannotBeInferred(VarDecl(auto, y = StructLiteral({StructLiteral({IntLiteral(1)})})))'
    assert Checker(source).check_from_source() == expected

def test_error_044():
    source = """
    struct A { int x; };
    void main() {
        A a = {1};
        int b = a.y;
    }
    """
    expected = 'TypeMismatchInExpression(MemberAccess(Identifier(a).y))'
    assert Checker(source).check_from_source() == expected

def test_error_045():
    source = """
    void foo(int a, float a) {}
    void main() {}
    """
    expected = 'Redeclared(Parameter, a)'
    assert Checker(source).check_from_source() == expected

def test_error_046():
    source = """
    void loop() { break; }
    void main() { while(1) { loop(); } }
    """
    expected = 'MustInLoop(BreakStmt())'
    assert Checker(source).check_from_source() == expected

def test_error_047():
    source = """
    struct Problem { int x; float x; };
    void main() {}
    """
    expected = 'Redeclared(Member, x)'
    assert Checker(source).check_from_source() == expected

def test_error_048():
    source = """
    void foo(Unknown u) {}
    void main() {}
    """
    expected = 'UndeclaredStruct(Unknown)'
    assert Checker(source).check_from_source() == expected

def test_error_049():
    source = """
    void func(int param) {
        if (1) {
            int param;
        }
    }
    void main() {}
    """
    expected = "Redeclared(Variable, param)"
    assert Checker(source).check_from_source() == expected

def test_error_050():
    source = """
    struct Point {
        int x;
        float y;
        string x;
    };
    void main() {}
    """
    expected = "Redeclared(Member, x)"
    assert Checker(source).check_from_source() == expected

def test_error_051():
    source = """
    struct S { int x; };
    void main() {
        int y = S;
    }
    """
    expected = "UndeclaredIdentifier(S)"
    assert Checker(source).check_from_source() == expected

def test_error_052():
    source = """
    struct S { int x; };
    void main() {
        S();
    }
    """
    expected = "UndeclaredFunction(S)"
    assert Checker(source).check_from_source() == expected

def test_error_053():
    source = """
    int myfunc() { return 1; }
    void main() {
        myfunc x;
    }
    """
    expected = "UndeclaredStruct(myfunc)"
    assert Checker(source).check_from_source() == expected

def test_error_054():
    source = """
    func() {
        auto x;
        return x;
    }
    void main() {}
    """
    expected = "TypeCannotBeInferred(ReturnStmt(return Identifier(x)))"
    assert Checker(source).check_from_source() == expected

def test_error_055():
    source = """
    void main() {
        auto a; auto b; auto c;
        c = a - b;
    }
    """
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(a), -, Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_error_056():
    source = """
    void main() {
        auto a; auto b;
        int c = a >= b;
    }
    """
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(a), >=, Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_error_057():
    source = """
    void main() {
        for(int i = 0; 1.5; ++i) {}
    }
    """
    expected = "TypeMismatchInStatement(ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); FloatLiteral(1.5); PrefixOp(++Identifier(i)) do BlockStmt([])))"
    assert Checker(source).check_from_source() == expected

def test_error_058():
    source = """
    func() {
        if (1) return 1;
        return 1.5;
    }
    void main() {}
    """
    expected = "TypeMismatchInStatement(ReturnStmt(return FloatLiteral(1.5)))"
    assert Checker(source).check_from_source() == expected

def test_error_059():
    source = """
    struct S { int x; };
    void main() {
        S s = {1};
        switch(s) {
            case 1: break;
        }
    }
    """
    expected = "TypeMismatchInStatement(SwitchStmt(switch Identifier(s) cases [CaseStmt(case IntLiteral(1): [BreakStmt()])]))"
    assert Checker(source).check_from_source() == expected

def test_error_060():
    source = """
    struct S { int a; };
    void main() {
        S s = {1};
        int x;
        x = s;
    }
    """
    expected = "TypeMismatchInStatement(ExprStmt(AssignExpr(Identifier(x) = Identifier(s))))"
    assert Checker(source).check_from_source() == expected

def test_error_061():
    source = """
    void main() {
        float f = 3.14;
        int x = !f;
    }
    """
    expected = "TypeMismatchInExpression(PrefixOp(!Identifier(f)))"
    assert Checker(source).check_from_source() == expected

def test_error_062():
    source = """
    void main() {
        int x = 5 % 2.0;
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(5), %, FloatLiteral(2.0)))"
    assert Checker(source).check_from_source() == expected

def test_error_063():
    source = """
    struct S { float a; };
    void main() {
        S s;
        s.a++;
    }
    """
    expected = "TypeMismatchInExpression(PostfixOp(MemberAccess(Identifier(s).a)++))"
    assert Checker(source).check_from_source() == expected

def test_error_064():
    source = """
    void main() {
        string s = "Hello" + "World";
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(StringLiteral('Hello'), +, StringLiteral('World')))"
    assert Checker(source).check_from_source() == expected

def test_error_065():
    source = """
    void main() {
        int x = 5;
        int y = x.member;
    }
    """
    expected = "TypeMismatchInExpression(MemberAccess(Identifier(x).member))"
    assert Checker(source).check_from_source() == expected

def test_error_066():
    source = """
    int add(int a, int b) { return a + b; }
    void main() {
        int x = add(5);
    }
    """
    expected = "TypeMismatchInExpression(FuncCall(add, [IntLiteral(5)]))"
    assert Checker(source).check_from_source() == expected

def test_error_067():
    source = """
    int foo(int a) { return a; }
    void main() {
        int x = foo(1, 2);
    }
    """
    expected = "TypeMismatchInExpression(FuncCall(foo, [IntLiteral(1), IntLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_error_068():
    source = """
    int foo(int a) { return a; }
    void main() {
        int x = foo(1.5);
    }
    """
    expected = "TypeMismatchInExpression(FuncCall(foo, [FloatLiteral(1.5)]))"
    assert Checker(source).check_from_source() == expected

def test_error_069():
    source = """
    void main() {
        string s = "test";
        string s2 = -s;
    }
    """
    expected = "TypeMismatchInExpression(PrefixOp(-Identifier(s)))"
    assert Checker(source).check_from_source() == expected

def test_error_070():
    source = """
    struct S { int x; };
    void main() {
        S s;
        int y = (s.x = "string") + 1;
    }
    """
    expected = "TypeMismatchInExpression(AssignExpr(MemberAccess(Identifier(s).x) = StringLiteral('string')))"
    assert Checker(source).check_from_source() == expected

def test_error_071():
    source = """
    void main() {
        int x;
        int y = (x = 3.14);
    }
    """
    expected = "TypeMismatchInExpression(AssignExpr(Identifier(x) = FloatLiteral(3.14)))"
    assert Checker(source).check_from_source() == expected

def test_error_072():
    source = """
    void main() {
        { break; }
    }
    """
    expected = "MustInLoop(BreakStmt())"
    assert Checker(source).check_from_source() == expected

def test_error_073():
    source = """
    void main() {
        switch(1) {
            case 1: continue;
        }
    }
    """
    expected = "MustInLoop(ContinueStmt())"
    assert Checker(source).check_from_source() == expected

def test_error_074():
    source = """
    void main() {
        if (1) {
            continue;
        }
    }
    """
    expected = "MustInLoop(ContinueStmt())"
    assert Checker(source).check_from_source() == expected

def test_error_075():
    source = """
    struct S { int a; float b; };
    void main() {
        S s = {1, "hello"};
    }
    """
    expected = "TypeMismatchInExpression(StructLiteral({IntLiteral(1), StringLiteral('hello')}))"
    assert Checker(source).check_from_source() == expected

def test_error_076():
    source = """
    struct S { int a; };
    void main() {
        S s = {1, 2};
    }
    """
    expected = "TypeMismatchInExpression(StructLiteral({IntLiteral(1), IntLiteral(2)}))"
    assert Checker(source).check_from_source() == expected

def test_error_077():
    source = """
    struct S { int x; };
    void main() {
        S s = {1};
        int x = s + 5;
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(s), +, IntLiteral(5)))"
    assert Checker(source).check_from_source() == expected

def test_error_078():
    source = """
    int readInt() { return 1; }
    void main() {}
    """
    expected = "Redeclared(Function, readInt)"
    assert Checker(source).check_from_source() == expected

def test_error_079():
    source = """
    struct S { int a; };
    void main() {
        S s1 = {1}; S s2 = {2};
        if (s1 == s2) {}
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(s1), ==, Identifier(s2)))"
    assert Checker(source).check_from_source() == expected

def test_error_080():
    source = """
    void main() {
        float x = 1.0;
        int y = x || 0;
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(x), ||, IntLiteral(0)))"
    assert Checker(source).check_from_source() == expected

def test_error_081():
    source = """
    void main() {
        for(auto i;;){}
    }
    """
    expected = "TypeCannotBeInferred(BlockStmt([ForStmt(for VarDecl(auto, i); None; None do BlockStmt([]))]))"
    assert Checker(source).check_from_source() == expected

def test_error_082():
    source = """
    void main() {
        int x; int y;
        x = y = "str";
    }
    """
    expected = "TypeMismatchInExpression(AssignExpr(Identifier(y) = StringLiteral('str')))"
    assert Checker(source).check_from_source() == expected

def test_error_083():
    source = """
    void main() {
        auto x;
        switch(1) { case x: break; }
        x = 1.5;
    }
    """
    expected = "TypeMismatchInStatement(CaseStmt(case Identifier(x): [BreakStmt()]))"
    assert Checker(source).check_from_source() == expected

def test_error_084():
    source = """
    void main() {
        auto b;
        if(b) {}
        b = "hello";
    }
    """
    expected = "TypeMismatchInStatement(ExprStmt(AssignExpr(Identifier(b) = StringLiteral('hello'))))"
    assert Checker(source).check_from_source() == expected

def test_error_085():
    source = """
    int main() {
        return;
    }
    """
    expected = "TypeMismatchInStatement(ReturnStmt(return))"
    assert Checker(source).check_from_source() == expected

def test_error_086():
    source = """
    func() {
        return;
        return 1.5;
    }
    void main() {}
    """
    expected = "TypeMismatchInStatement(ReturnStmt(return FloatLiteral(1.5)))"
    assert Checker(source).check_from_source() == expected

def test_error_087():
    source = """
    void main() {
        auto a;
        while(a || 1) {}
        a = "str";
    }
    """
    expected = "TypeMismatchInStatement(ExprStmt(AssignExpr(Identifier(a) = StringLiteral('str'))))"
    assert Checker(source).check_from_source() == expected

def test_error_088():
    source = """
    struct Point { int x; };
    struct Circle { int r; };
    void foo(Point p) {}
    void main() {
        Circle c = {5};
        foo(c);
    }
    """
    expected = "TypeMismatchInExpression(FuncCall(foo, [Identifier(c)]))"
    assert Checker(source).check_from_source() == expected

def test_error_089():
    source = """
    struct S { int a; };
    void main() {
        auto x; S s;
        x = s;
        int y = x;
    }
    """
    expected = "TypeMismatchInStatement(VarDecl(IntType(), y = Identifier(x)))"
    assert Checker(source).check_from_source() == expected

def test_error_090():
    source = """
    void foo(int x) {}
    void main() {
        foo({1});
    }
    """
    expected = "TypeMismatchInExpression(FuncCall(foo, [StructLiteral({IntLiteral(1)})]))"
    assert Checker(source).check_from_source() == expected

def test_error_091():
    source = """
    struct S { int x; };
    S getS() { S s; return s; }
    void main() {
        float y = getS().x;
    }
    """
    expected = "TypeMismatchInStatement(VarDecl(FloatType(), y = MemberAccess(FuncCall(getS, []).x)))"
    assert Checker(source).check_from_source() == expected

def test_error_092():
    source = """
    struct S {};
    void main() {
        S s;
        !s;
    }
    """
    expected = "TypeMismatchInExpression(PrefixOp(!Identifier(s)))"
    assert Checker(source).check_from_source() == expected

def test_error_093():
    source = """
    void main() {
        auto x;
        float y = x + 1;
    }
    """
    expected = "TypeMismatchInStatement(VarDecl(FloatType(), y = BinaryOp(Identifier(x), +, IntLiteral(1))))"
    assert Checker(source).check_from_source() == expected

def test_error_094():
    source = """
    void main() {
        int x;
        for(x = 5; "str";) {}
    }
    """
    expected = "TypeMismatchInStatement(ForStmt(for ExprStmt(AssignExpr(Identifier(x) = IntLiteral(5))); StringLiteral('str'); None do BlockStmt([])))"
    assert Checker(source).check_from_source() == expected

def test_error_095():
    source = """
    void foo() {}
    void main() {
        auto x;
        x = foo();
        x + 1;
    }
    """
    expected = "TypeCannotBeInferred(AssignExpr(Identifier(x) = FuncCall(foo, [])))"
    assert Checker(source).check_from_source() == expected

def test_error_096():
    source = """
    void main() {
        int x = x + 1;
    }
    """
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected

def test_error_097():
    source = """
    void main() {
        auto x = 1;
        {
            auto x;
        }
    }
    """
    expected = "TypeCannotBeInferred(BlockStmt([VarDecl(auto, x)]))"
    assert Checker(source).check_from_source() == expected

def test_error_098():
    source = """
    struct S { int a; };
    void foo(int x) {}
    void main() {
        foo(1, 2);
    }
    """
    expected = "TypeMismatchInExpression(FuncCall(foo, [IntLiteral(1), IntLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_error_099():
    source = """
    struct Point { int x; int y; };
    void main() {
        Point p = {1.5, 2};
    }
    """
    expected = "TypeMismatchInExpression(StructLiteral({FloatLiteral(1.5), IntLiteral(2)}))"
    assert Checker(source).check_from_source() == expected

def test_error_100():
    source = """
    void main() {
        int x = {1} + 2;
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(StructLiteral({IntLiteral(1)}), +, IntLiteral(2)))"
    assert Checker(source).check_from_source() == expected

def test_error_101():
    source = """
    func() { return {1}; }
    void main() { auto x = func(); }
    """
    expected = "TypeCannotBeInferred(ReturnStmt(return StructLiteral({IntLiteral(1)})))"
    assert Checker(source).check_from_source() == expected

def test_error_102():
    source = """
    void foo(int x) {
        for(int x = 0; 1; x++) {}
    }
    void main() {}
    """
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected

def test_error_103():
    source = """
    void main() {
        int a;
        Point a = b;
    }
    """
    expected = "Redeclared(Variable, a)"
    assert Checker(source).check_from_source() == expected

def test_error_104():
    source = """
    void main() {
        while(1) auto x = {1};
    }
    """
    expected = "TypeCannotBeInferred(VarDecl(auto, x = StructLiteral({IntLiteral(1)})))"
    assert Checker(source).check_from_source() == expected

def test_error_105():
    source = """
    struct S { int x; };
    void main() {
        auto a;
        S s = {a};
        string y = a;
    }
    """
    expected = "TypeMismatchInStatement(VarDecl(StringType(), y = Identifier(a)))"
    assert Checker(source).check_from_source() == expected

def test_error_106():
    source = """
    struct Inner { float f; };
    struct Outer { Inner i; };
    void main() {
        auto a;
        Outer o = {{a}};
        int z = a;
    }
    """
    expected = "TypeMismatchInStatement(VarDecl(IntType(), z = Identifier(a)))"
    assert Checker(source).check_from_source() == expected

def test_error_107():
    source = """
    struct S { int x; };
    void main() {
        auto a;
        S s = {a, 2};
    }
    """
    expected = "TypeMismatchInExpression(StructLiteral({Identifier(a), IntLiteral(2)}))"
    assert Checker(source).check_from_source() == expected

def test_error_108():
    source = """
    void main() {
        int x = {1}.member;
    }
    """
    expected = "TypeMismatchInExpression(MemberAccess(StructLiteral({IntLiteral(1)}).member))"
    assert Checker(source).check_from_source() == expected

def test_error_109():
    source = """
    Unk foo() { return; }
    void main() {}
    """
    expected = "UndeclaredStruct(Unk)"
    assert Checker(source).check_from_source() == expected

def test_error_110():
    source = """
    void main() {
        if(1) break;
    }
    """
    expected = "MustInLoop(BreakStmt())"
    assert Checker(source).check_from_source() == expected

def test_error_111():
    source = """
    int func() {
        auto a;
        a = "str";
        return a;
    }
    void main() {}
    """
    expected = "TypeMismatchInStatement(ReturnStmt(return Identifier(a)))"
    assert Checker(source).check_from_source() == expected

def test_error_112():
    source = """
    void foo(int x) {}
    void main() {
        auto a; auto b;
        foo(a + b);
    }
    """
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(a), +, Identifier(b)))"
    assert Checker(source).check_from_source() == expected

def test_error_113():
    source = """
    void foo(Missing m) {}
    void main() {}
    """
    expected = "UndeclaredStruct(Missing)"
    assert Checker(source).check_from_source() == expected

def test_error_114():
    source = """
    int getX() { return 1; }
    void main() {
        getX = 1;
    }
    """
    expected = "UndeclaredIdentifier(getX)"
    assert Checker(source).check_from_source() == expected

def test_error_115():
    source = """
    struct A { int x; };
    struct B { int x; };
    void main() {
        A a; B b;
        a = b;
    }
    """
    expected = "TypeMismatchInStatement(ExprStmt(AssignExpr(Identifier(a) = Identifier(b))))"
    assert Checker(source).check_from_source() == expected

def test_error_116():
    source = """
    void main() {
        auto x;
        switch(x) {}
        string y = x + "str";
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(Identifier(x), +, StringLiteral('str')))"
    assert Checker(source).check_from_source() == expected

def test_error_117():
    source = """
    struct S { int a; };
    void main() {
        S s;
        s.a = 2;
        switch (s.a) {
            case 1: 
                int a = 2;
                break;
            case 2:
                int a = 3;
            default:
                a = 4;
        }
    }
    """
    expected = "Redeclared(Variable, a)"
    assert Checker(source).check_from_source() == expected

def test_error_118():
    source = """
    struct Inner { int x; };
    struct Outer { Inner i; };
    void main() {
        Outer o;
        int y = o.x;
    }
    """
    expected = "TypeMismatchInExpression(MemberAccess(Identifier(o).x))"
    assert Checker(source).check_from_source() == expected

def test_error_119():
    source = """
    int foo() { return 1; }
    void main() {
        ++foo();
    }
    """
    expected = "TypeMismatchInExpression(PrefixOp(++FuncCall(foo, [])))"
    assert Checker(source).check_from_source() == expected

def test_error_120():
    source = """
    int foo() { return 1; }
    void main() {
        foo()++;
    }
    """
    expected = "TypeMismatchInExpression(PostfixOp(FuncCall(foo, [])++))"
    assert Checker(source).check_from_source() == expected

def test_error_121():
    source = """
    void main() {
        switch(1) {
            default: funcX();
        }
    }
    """
    expected = "UndeclaredFunction(funcX)"
    assert Checker(source).check_from_source() == expected

def test_error_122():
    source = """
    void main() {
        readInt(1);
    }
    """
    expected = "TypeMismatchInExpression(FuncCall(readInt, [IntLiteral(1)]))"
    assert Checker(source).check_from_source() == expected

def test_error_123():
    source = """
    void foo(int x, float x) {}
    void main() {}
    """
    expected = "Redeclared(Parameter, x)"
    assert Checker(source).check_from_source() == expected

def test_error_124():
    source = """
    void foo(int x) { int x; }
    void main() {}
    """
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected

def test_error_125():
    source = """
    void main() {
        int x = {1};
    }
    """
    expected = "TypeMismatchInStatement(VarDecl(IntType(), x = StructLiteral({IntLiteral(1)})))"
    assert Checker(source).check_from_source() == expected

def test_error_126():
    source = """
    void main() {
        int x = 1 >= "str";
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(IntLiteral(1), >=, StringLiteral('str')))"
    assert Checker(source).check_from_source() == expected

def test_error_127():
    source = """
    struct T { int a; };
    void main() {
        auto z;
        T t = {z};
        z = "hello";
    }
    """
    expected = "TypeMismatchInStatement(ExprStmt(AssignExpr(Identifier(z) = StringLiteral('hello'))))"
    assert Checker(source).check_from_source() == expected

def test_error_128():
    source = """
    void main() {
        auto a;
        int x = a = "str";
    }
    """
    expected = "TypeMismatchInStatement(VarDecl(IntType(), x = AssignExpr(Identifier(a) = StringLiteral('str'))))"
    assert Checker(source).check_from_source() == expected

def test_error_129():
    source = """
    void main() {
        int a = "hello" == "world";
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(StringLiteral('hello'), ==, StringLiteral('world')))"
    assert Checker(source).check_from_source() == expected

def test_error_130():
    source = """
    void main() {
        auto x;
        int y = x++;
        float z = x;
    }
    """
    expected = "TypeMismatchInStatement(VarDecl(FloatType(), z = Identifier(x)))"
    assert Checker(source).check_from_source() == expected

def test_error_131():
    source = """
    void main() {
        switch(1) {
            case 1: continue;
        }
    }
    """
    expected = "MustInLoop(ContinueStmt())"
    assert Checker(source).check_from_source() == expected

def test_error_132():
    source = """
    void main() {
        for(int i=0; a < 5; i++) {
            int a = 1;
        }
    }
    """
    expected = "UndeclaredIdentifier(a)"
    assert Checker(source).check_from_source() == expected

def test_error_133():
    source = """
    void main() {
        auto x = 1;
        { break; }
    }
    """
    expected = "MustInLoop(BreakStmt())"
    assert Checker(source).check_from_source() == expected

def test_error_134():
    source = """
    void x() {}
    void x(int a) {}
    void main() {}
    """
    expected = "Redeclared(Function, x)"
    assert Checker(source).check_from_source() == expected

def test_error_135():
    source = """
    void printInt() {}
    void main() {}
    """
    expected = "Redeclared(Function, printInt)"
    assert Checker(source).check_from_source() == expected

def test_error_136():
    source = """
    struct Point {
        int x; int y;
    };
    void complex(int a, float b, Point a) {}
    void main() {}
    """
    expected = "Redeclared(Parameter, a)"
    assert Checker(source).check_from_source() == expected

def test_error_137():
    source = """
    void main() {
        if (1) { int f = 1; }
        else { int f = 2; }
        f = 3;
    }
    """
    expected = "UndeclaredIdentifier(f)"
    assert Checker(source).check_from_source() == expected

def test_error_138():
    source = """
    void foo(int x) {
        while(1) {
            int x = 5;
        }
    }
    void main() {}
    """
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected

def test_error_139():
    source = """
    struct Map { int y; };
    void main() {
        Map = 1;
    }
    """
    expected = "UndeclaredIdentifier(Map)"
    assert Checker(source).check_from_source() == expected

def test_error_140():
    source = """
    struct Data { int z; };
    void main() {
        z = 5;
    }
    """
    expected = "UndeclaredIdentifier(z)"
    assert Checker(source).check_from_source() == expected

def test_error_141():
    source = """
    void calc(int x) {}
    void main() {
        calc(randomFunction());
    }
    """
    expected = "UndeclaredFunction(randomFunction)"
    assert Checker(source).check_from_source() == expected

def test_error_142():
    source = """
    struct Pair { int a; float a; };
    void main() {}
    """
    expected = "Redeclared(Member, a)"
    assert Checker(source).check_from_source() == expected

def test_error_143():
    source = """
    void main() {
        switch(1) {
            case 1:
                int loop;
                float loop;
        }
    }
    """
    expected = "Redeclared(Variable, loop)"
    assert Checker(source).check_from_source() == expected

def test_error_144():
    source = """
    void main() {
        switch(1) {
            default:
                string k;
                int k;
        }
    }
    """
    expected = "Redeclared(Variable, k)"
    assert Checker(source).check_from_source() == expected

def test_error_145():
    source = """
    void process(int value) {
        if (value > 0) {
            int value = 10; 
            printInt(value);
        }
    }

    void main() {}
    """
    expected = "Redeclared(Variable, value)"
    assert Checker(source).check_from_source() == expected

def test_error_146():
    source = """
    void main() {
        if(1) {
            continue;
        }
    }
    """
    expected = "MustInLoop(ContinueStmt())"
    assert Checker(source).check_from_source() == expected

def test_error_147():
    source = """
    void main() {
        int a; int b; 
        auto c; c.x = a;
    }
    """
    expected = "TypeCannotBeInferred(MemberAccess(Identifier(c).x))"
    assert Checker(source).check_from_source() == expected

def test_error_148():
    source = """
    void main() {
        ++doSomething();
    }
    """
    expected = "UndeclaredFunction(doSomething)"
    assert Checker(source).check_from_source() == expected

def test_error_149():
    source = """
    struct Node { int size; };
    void main() {
        Node n;
        int size = n.val;
    }
    """
    expected = "TypeMismatchInExpression(MemberAccess(Identifier(n).val))"
    assert Checker(source).check_from_source() == expected

def test_error_150():
    source = """
    void main() {
        int x = {1}++;
    }
    """
    expected = "TypeMismatchInExpression(PostfixOp(StructLiteral({IntLiteral(1)})++))"
    assert Checker(source).check_from_source() == expected

def test_error_151():
    source = """
    struct Infinite { Infinite cycle; };
    void main() {}
    """
    expected = "UndeclaredStruct(Infinite)"
    assert Checker(source).check_from_source() == expected

def test_error_152():
    source = """
    struct Infinite { Infinite cycle; };
    void main() {}
    """
    expected = "UndeclaredStruct(Infinite)"
    assert Checker(source).check_from_source() == expected

def test_error_153():
    source = """
    void main() {
        int equality = "alpha" == "beta";
        int difference = "alpha" != "beta";
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(StringLiteral('alpha'), ==, StringLiteral('beta')))"
    assert Checker(source).check_from_source() == expected

def test_error_154():
    source = """
    void main() {
        auto a; auto b; auto c; auto d;
    }
    """
    expected = "TypeCannotBeInferred(BlockStmt([VarDecl(auto, a), VarDecl(auto, b), VarDecl(auto, c), VarDecl(auto, d)]))"
    assert Checker(source).check_from_source() == expected

def test_error_155():
    source = """
    void main() {
        for (;;) {
            auto i;
        }
    }
    """
    expected = "TypeCannotBeInferred(BlockStmt([VarDecl(auto, i)]))"
    assert Checker(source).check_from_source() == expected

def test_error_156():
    source = """
    void main() {
        auto x; -x;
    }
    """
    expected = "TypeCannotBeInferred(PrefixOp(-Identifier(x)))"
    assert Checker(source).check_from_source() == expected

def test_error_157():
    source = """
    void main() {
        int a = 1;
        float b = 2.0;
        auto c;
        if ((a > 0) && (b < 3.0) || (c == 1)) {
            c = c + 1;
        }
    }
    """
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(c), ==, IntLiteral(1)))"
    assert Checker(source).check_from_source() == expected

def test_error_158():
    source = """
    void main() { auto x; x < 1.0; }
    """
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(x), <, FloatLiteral(1.0)))"
    assert Checker(source).check_from_source() == expected

def test_error_159():
    source = """
    void main() { auto x; int y = (x == 1.0); }
    """
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(x), ==, FloatLiteral(1.0)))"
    assert Checker(source).check_from_source() == expected


# =================================================================== #
# Extra tests for edge/stupid scenarios                               #
# =================================================================== #

def test_extra_001():
    source = """
    int foo() {auto a; return a;}
    struct foo {int x; int y;};
    void main() {
        int b = foo();  
        auto m; auto n; foo f = {m, n};
        auto p; auto q; f = {p, q};
        return;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_002():
    source = """
    void main() {
        for (int a = 0; a < 5; a++) 
            float a = 5.0 + 1;

        {
            float a = 1.0;
            {
                string a = "hello";
                int b = 5;
            }
            float b = 5.0;
        }
        string b = "hello";

        while (a < 10) {
            int a = 11;
        }

        a = 5;
        while (a++ < 10)
            int a = 11;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_003():
    source = """
    void main() {
        int x = x % x;
        return;
    }
    """
    expected = "UndeclaredIdentifier(x)"
    assert Checker(source).check_from_source() == expected

def test_extra_004():
    source = """
    void main() {
        int a = 5;
        {
            auto a;
            auto b;
            b = 10;
        }
        float c = a + 3.1;
    }
    """
    expected = "TypeCannotBeInferred(BlockStmt([VarDecl(auto, a), VarDecl(auto, b), ExprStmt(AssignExpr(Identifier(b) = IntLiteral(10)))]))"
    assert Checker(source).check_from_source() == expected

def test_extra_005():
    source = """
    void main() {
        auto x; auto y = !x;
        switch (x + y) {
            case 3 + 2:
                auto x = 5.0;
                break;
            case 3 % 2:
                auto x = 1;
                break;
            default:
                auto z = "hello";
        }

        printInt(x * y);
    }
    """
    expected = "Redeclared(Variable, x)"
    assert Checker(source).check_from_source() == expected

def test_extra_006():
    source = """
    foo(int a, int b) {
        return a + b;
    }

    void main() {
        printInt(foo(3, 4));
        return;
    }

    foo(float a, float b) {
        return a * b;
    }
    """
    expected = "Redeclared(Function, foo)"
    assert Checker(source).check_from_source() == expected

def test_extra_007():
    source = """
    foo() {
        return "hello";
        return 3.14;
        return 1;
    }

    void main() {
        printString(foo());
    }
    """
    expected = "TypeMismatchInStatement(ReturnStmt(return FloatLiteral(3.14)))"
    assert Checker(source).check_from_source() == expected

def test_extra_008():
    source = """
    struct Point { float x; float y; };
    struct Complex { float re; float im; };
    
    Point foo(float a, float b) {
        return {a + 0.0, b + 0.0};
    }

    void main() {
        Complex c = {3.0, 4.0};
        Point p = foo(c.re, c.im);
        p = foo(p.x, p.y);
        c = foo(p.x, p.y);
    }
    """
    expected = "TypeMismatchInStatement(ExprStmt(AssignExpr(Identifier(c) = FuncCall(foo, [MemberAccess(Identifier(p).x), MemberAccess(Identifier(p).y)]))))"
    assert Checker(source).check_from_source() == expected

def test_extra_009():
    source = """
    void main() {
        int x; float y;
        y = (x = 5) + readFloat();
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_010():
    source = """
    void main() {
        float x;
        x = readFloat() + readInt() - readFloat();
        printFloat(x);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def text_extra_011():
    source = """
    int bar() {return 1;}

    void main() {
        int bar;
        readInt(bar);
        bar = bar + bar();
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_012():
    source = """
    void foo(int x) {
        printInt(x);
    }
    void main() {
        auto a; auto b;
        foo(!a == !b); foo(a <= b);
        foo(a >= b);
        foo(a != b);
        printInt(a); 
        printFloat(b + 1.0);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_013():
    source = """
    void main() {
        string s; string r;
        printString(s = "hi");
        printString(r = (s = "hello"));
        printString(s = r = s = r = s);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_014():
    source = """
    void main() {
        int x; float y;
        printInt(x = (2 <= (y = 3.14)));
        printFloat(1.0 + (x = (2 <= (y = 3.14))));
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_015():
    source = """
    void main() {
        printInt(readInt() % readInt());
        printFloat((readFloat() == readFloat()) + readFloat());
        printString(readString());
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_016():
    source = """
    void f() {}
    h() {return f();}
    """
    expected = "TypeCannotBeInferred(ReturnStmt(return FuncCall(f, [])))"
    assert Checker(source).check_from_source() == expected

def test_extra_017():
    source = """
    void f() {}
    void g() {return f();}
    """
    expected = "TypeMismatchInStatement(ReturnStmt(return FuncCall(f, [])))"
    assert Checker(source).check_from_source() == expected

def test_extra_018():
    source = """
    foo() {return foo() + 1;}

    void main() {
        printInt(foo());
    }
    """
    expected = "TypeCannotBeInferred(ReturnStmt(return BinaryOp(FuncCall(foo, []), +, IntLiteral(1))))"
    assert Checker(source).check_from_source() == expected

def test_extra_019():
    source = """
    struct structName { int structName; };
    void main() {
        structName s;
        s.structName = 5;
        printInt(s.structName);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_020():
    source = """
    void main() {
        int x = 3; int y = 4;
        if ({x, y} == 3 + 4) {
            printString("Equal");
        } else {
            printString("Not equal");
        }
    }
    """
    expected = "TypeMismatchInExpression(BinaryOp(StructLiteral({Identifier(x), Identifier(y)}), ==, BinaryOp(IntLiteral(3), +, IntLiteral(4))))"
    assert Checker(source).check_from_source() == expected

def test_extra_021():
    source = """
    struct Point1 {int x; int y;};
    struct Point2 {int x; int y;};

    void foo(Point1 p){
        p.x = 1; p.y = 1.0;
    }

    void main() {
        Point1 p1;
        foo(p1);
    }
    """
    expected = "TypeMismatchInStatement(ExprStmt(AssignExpr(MemberAccess(Identifier(p).y) = FloatLiteral(1.0))))"
    assert Checker(source).check_from_source() == expected

def test_extra_022():
    source = """
    struct Point1 {int x; int y;};
    struct Point2 {int x; int y;};

    void foo(Point1 p){
        p.x = 1; p.y = 1;
    }   

    void main() {
        auto p1;
        foo(p1);
        Point2 p2 = {1, 2};
        p1 = p2;
    }
    """
    expected = "TypeMismatchInStatement(ExprStmt(AssignExpr(Identifier(p1) = Identifier(p2))))"
    assert Checker(source).check_from_source() == expected

def test_extra_023():
    source = """
    foo() {
        int x = foo();
        return 1;
    }
    void main() {}
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_024():
    source = """
    foo() {
        int x = foo();
        return 1.0;
    }
    """
    expected = "TypeMismatchInStatement(VarDecl(IntType(), x = FuncCall(foo, [])))"
    assert Checker(source).check_from_source() == expected

def test_extra_025():
    source = """
    foo() {
        auto x = foo();
        return 1.0;
    }
    void main() {}
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_026():
    source = """
    foo() {return foo();}
    """
    expected = "TypeCannotBeInferred(ReturnStmt(return FuncCall(foo, [])))"
    assert Checker(source).check_from_source() == expected

def test_extra_027():
    source = """
    int factorial(int n){
        if (n <= 1) return 1;
        return n * factorial(n-1);
    }

    void main() {
        printInt(factorial(5));
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_028():
    source = """
    void main() {
        int x;
        {x, 1}++;
    }
    """
    expected = "TypeMismatchInExpression(PostfixOp(StructLiteral({Identifier(x), IntLiteral(1)})++))"
    assert Checker(source).check_from_source() == expected

def test_extra_029():
    source = """
    foo() {
        auto a = foo();
        a++;
        return 1;
    }
    void main() {}
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_030():
    source = """
    struct Point {
        int x; int y;
    };
    
    Point hi(){
        auto p; return p;
    }

    void main() {
        int x = hi().x++;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_031():
    source = """
    void main() {
        auto x;
        if (1) x = 1;
        x = 3.5;
    }
    """
    expected = "TypeMismatchInStatement(ExprStmt(AssignExpr(Identifier(x) = FloatLiteral(3.5))))"
    assert Checker(source).check_from_source() == expected

def test_extra_032():
    source = """
    void main() {
        int a;
        switch (1) {
            case (a = 5):
                printInt(a);
                break;
            default:
                printInt(a);
        }
    }
    """
    expected = "TypeMismatchInStatement(CaseStmt(case AssignExpr(Identifier(a) = IntLiteral(5)): [ExprStmt(FuncCall(printInt, [Identifier(a)])), BreakStmt()]))"
    assert Checker(source).check_from_source() == expected

def test_extra_033():
    source = """
    void main() {
        int a = 5;
        {
            auto a;
            auto b;
            b = 10;
        }
        float c = a + 3.1;
    }
    """
    expected = "TypeCannotBeInferred(BlockStmt([VarDecl(auto, a), VarDecl(auto, b), ExprStmt(AssignExpr(Identifier(b) = IntLiteral(10)))]))"
    assert Checker(source).check_from_source() == expected

def test_extra_034():
    source = """
    void main() {
        auto x;
        if (x == "abc") {}
        return;
    }
    """
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(x), ==, StringLiteral('abc')))"
    assert Checker(source).check_from_source() == expected

def test_extra_035():
    source = """
    foo() {
        auto x;
        x = (x + 1.0) == 0.0;
    }
    """
    expected = "TypeCannotBeInferred(BinaryOp(Identifier(x), +, FloatLiteral(1.0)))"
    assert Checker(source).check_from_source() == expected

def test_extra_036():
    source = """
    int main() {
        return 1;
    }
    """
    expected = "UndeclaredFunction(main)"
    assert Checker(source).check_from_source() == expected

def test_extra_037():
    source = """
    main() { return; }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_038():
    source = """
    void main(int x) {
        return;
    }
    """
    expected = "UndeclaredFunction(main)"
    assert Checker(source).check_from_source() == expected

def test_extra_039():
    source = """
    struct A {
        int x;
        int y;
    };
    struct B{
        A x;
        A y;
    };
    struct C {
        B b;
        string c;
        A a;
    };
    void foo(B b, int x) {}
    void main() {
        C c1 = {{{1, 2}, {3, 4}}, "hello", {5, 3.14}}; // invalid, last field should be int, not float
        foo(c1.b, c1.b.x.x); // valid
    }
    """
    expected = "TypeMismatchInExpression(StructLiteral({IntLiteral(5), FloatLiteral(3.14)}))"
    assert Checker(source).check_from_source() == expected

def test_extra_040():
    source = """
    foo() {foo();}
    bar() {}
    void main() {}
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_041():
    source = """
    void main() {
        if ("abc") {};
    }
    """
    expected = "TypeMismatchInStatement(IfStmt(if StringLiteral('abc') then ExprStmt(StructLiteral({}))))"
    assert Checker(source).check_from_source() == expected

def test_extra_042():
    source = """
    void main() {
        auto a;
        a;
    }
    """
    expected = "TypeCannotBeInferred(ExprStmt(Identifier(a)))"
    assert Checker(source).check_from_source() == expected

def test_extra_043():
    source = """
    void main() {
        auto x;
        {1, x};
    }
    """
    expected = "TypeCannotBeInferred(ExprStmt(StructLiteral({IntLiteral(1), Identifier(x)})))"
    assert Checker(source).check_from_source() == expected

def test_extra_044():
    source = """
    void main() {
        int x; float y;
        {x, y, x, y, x, y};
        x; x; y; y;
        auto z; auto t;
        {!z, z, z, z, z, z};
        {t + 1, t, t, t, t, t};
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_extra_045():
    source = """
    struct Point {float x; int y;};
    void main() {
        auto t; Point p = {t, t + 1};
    }
    """
    expected = "TypeMismatchInExpression(StructLiteral({Identifier(t), BinaryOp(Identifier(t), +, IntLiteral(1))}))"
    assert Checker(source).check_from_source() == expected

def test_extra_046():
    source = """
    struct Point {float x; int y;};
    void main() {
        auto t; Point p;
        p = {t, t + 1};
    }
    """
    expected = "TypeMismatchInExpression(StructLiteral({Identifier(t), BinaryOp(Identifier(t), +, IntLiteral(1))}))"
    assert Checker(source).check_from_source() == expected

def test_extra_047():
    source = """
    struct Point {int x; float z; int y;};
    void main() {
        auto t; Point p = {t, 1.0 + t, t + 1};
        auto m; p = {m, 1.0 + m, m + 1};
    }
    """
    expected = "TypeCannotBeInferred(BinaryOp(FloatLiteral(1.0), +, Identifier(t)))"
    assert Checker(source).check_from_source() == expected

def test_main_001():
    source = """
    int main() { return 1;}
    float main() { return 1.0;}
    """
    expected = "Redeclared(Function, main)"
    assert Checker(source).check_from_source() == expected

def test_main_002():
    source = """
    main() { main(); }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_main_003():
    source = """
    int foo() { main(); return 1; }
    void main() {}
    """
    expected = "UndeclaredFunction(main)"
    assert Checker(source).check_from_source() == expected