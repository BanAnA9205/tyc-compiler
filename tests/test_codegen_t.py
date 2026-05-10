from src.utils.nodes import *
from tests.utils import *


def test_001():
    source = "void main() { printString(\"Hello World\"); }"
    expected = "Hello World"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_002():
    source = "void main() { printInt(42); }"
    expected = "42"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_003():
    source = "void main() { printFloat(3.14); }"
    expected = "3.14"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_004():
    source = "void main() { int x = 10; printInt(x); }"
    expected = "10"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_005():
    source = "void main() { printInt(5 + 3); }"
    expected = "8"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_006():
    source = "void main() { printInt(6 * 7); }"
    expected = "42"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)

def test_007():
    source = "void main() { if (1 < 2) { printString(\"yes\"); } else { printString(\"no\"); } }"
    expected = "yes"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_008():
    source = "void main() { int i = 0; while (i < 3) { printInt(i); i = i + 1; } }"
    expected = "012"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_009():
    source = "int add(int a, int b) { return a + b; } void main() { printInt(add(20, 22)); }"
    expected = "42"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_010():
    source = "void main() { int x = 10; int y = 20; printInt(x + y); }"
    expected = "30"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_011():
    source = "void main() { printInt(1 + 2 * 3); }"
    expected = "7"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_012():
    source = '''
    int fibo(int n) {
        if (n <= 1) return n;
        return fibo(n - 1) + fibo(n - 2);
    }
    void main() { printInt(fibo(10)); }
    '''
    expected = "55"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_013():
    source = '''
    void main() {
        switch (2) {
            case 1: printInt(1);
            case 2: printInt(2);
            case 3: printInt(3);
        }
    }
    '''
    expected = "23"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_014():
    source = '''
    struct Point { int x; int y; };
    struct Line { Point start; Point end; };
    void main() {
        Line l = {{1, 2}, {3, 4}};
        l.start.x = 10;
        l.end.y = 20;
        printInt(l.start.x); printInt(l.start.y);
        printInt(l.end.x); printInt(l.end.y);
    }
    '''
    expected = "10" "2" "3" "20"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_015():
    source = '''
    void main() {
        switch (2) {
            case 1: printInt(1); break;
            case 2: printInt(2); break;
            case 3: printInt(3); break;
        }
    }
    '''
    expected = "2"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_016():
    source = '''
    void main() {
        switch (2) {
            case 1: printInt(1);
            case 2:
            case 3: printInt(3);
        }
    }
    '''
    expected = "3"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_017():
    source = '''
    void main() {
        int x = 2;
        switch (2) {
            case 1: x = x * 2; printInt(x);
            case 2: x = x * 2; printInt(x);
            case 3: x = x * 2; printInt(x);
            case 4: x = x * 2; printInt(x);
            default: x = x * 2; printInt(x);
        }
    }
    '''
    expected = "481632"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_018():
    source = '''
    int f() {
        switch (2) {
            case 1: return 1;
            case 2: return 2;
            case 3: return 3;
        }
        return 0;
    }
    void main() { printInt(f()); }
    '''
    expected = "2"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_019():
    source = '''
    void main() {
        int x = 10;
        while (x--) switch (x) {
            case 9: printInt(9); break;
            case 5: printInt(5); break;
            case 0: printInt(0); break;
        }
    }
    '''
    expected = "950"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_020():
    source = '''
    void main() {
        int x = 10;
        while (x--) switch (x) {
            case 9: printInt(9);
            case 5: printInt(5);
            case 0: printInt(0);
        }
    }
    '''
    expected = "950500"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_021():
    source = '''
    void f() { for (int i = 0; i < 3; i++) printInt(i); }
    void main() { f(); }
    '''
    expected = "012"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_022():
    source = '''
    struct Point { int x; int y; };
    void main() { Point p = {1, 2}; printInt(p.x); printInt(p.y); }
    '''
    expected = "12"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_023():
    source = '''
    struct Point { int x; int y; };
    void main() { Point p = {1, 2}; Point q = p; printInt(q.x); printInt(q.y); }
    '''
    expected = "12"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_024():
    source = '''
    struct Point { int x; int y; };
    struct Line { Point start; Point end; };
    void main() {
        Line l = {{1, 2}, {3, 4}};
        printInt(l.start.x); printInt(l.start.y);
        printInt(l.end.x); printInt(l.end.y);
    }
    '''
    expected = "1234"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_025():
    source = '''
    void main() {
        printInt(1-2);
        printInt(4/2);
        printInt(5%3);
        printFloat(1.2 + 1);
        printFloat(3.5 * 2);
        printFloat(5.0 / 2);
        printInt(!1);
        printInt(!0);
        printInt(!2);
        printInt(1 && 0);
        printInt(1 && 2);
        printInt(2 || 0);
        printInt(0 || 0);
        printInt(2 >= 2);
        printInt(2 <= 2);
        printInt(2 == 2);
        printInt(2 != 2);
        printInt(2.0 == 2);
        printInt(2.0 != 2);
        printInt(2.0 == 2.0);
        printInt(2.0 != 2.0);
    }
    '''
    expected = "-1"\
               "2"\
               "2"\
               "2.2"\
               "7.0"\
               "2.5"\
               "0"\
               "1"\
               "0"\
               "0"\
               "1"\
               "1"\
               "0"\
               "1"\
               "1"\
               "1"\
               "0"\
               "1"\
               "0"\
               "1"\
               "0"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_026():
    source = '''
    struct Point { int x; int y; };
    void main() {
        Point p = {1, 2};
        p.x = 10;
        printInt(p.x);
    }
    '''
    expected = "10"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_027():
    source = '''
    struct Point { int x; int y; };
    int getInt() { return 1; }
    float getFloat() { return 2.5; }
    string getString() { return "hello"; }
    Point getPoint() { return {3, 4}; }
    void main() {
        int x = getInt();
        float f = getFloat();
        string s = getString();
        Point p = getPoint();
        printInt(x);
        printFloat(f);
        printString(s);
        printInt(p.x);
        printInt(p.y);
    }
    '''
    expected = "1" "2.5" "hello" "3" "4"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_028():
    source = '''
    void main() {
        switch (10) {
            case 1+2+3: printInt(6); break;
            case 4*5: printInt(20); break;
            case 9+8/7: printInt(10); break;
            default: printInt(0); break;
        }
    }
    '''
    expected = "10"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_029():
    source = '''
    void main() {
        for (int i = 0; i < 5;) switch (i++) {
            case 0: printInt(0); continue;
            case 1: printInt(1); continue;
            case 2: printInt(2); continue;
            default: printInt(3); continue;
        }
    }
    '''
    expected = "01233"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_030():
    source = '''
    void main() {
        for (int i = 0; i < 4; i++) if (i % 2) {
            int x = i; string text = "The odd number are ";
            printString(text); printInt(x);
        } else {
            string the = "The ";
            string even = "even ";
            string number = "number ";
            string are = "are ";
            int x = i;
            printString(the); printString(even); printString(number); printString(are); printInt(x);
        }
    }
    '''
    expected = "The even number are 0"\
               "The odd number are 1"\
               "The even number are 2"\
               "The odd number are 3"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_031():
    source = '''
    void main() {
        int x = 10;
        while (x--) int x = 5;
        printInt(x);
    }
    '''
    expected = "-1"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_032():
    source = '''
    void main() {
        int x = 256;
        for (;;) {
            printInt(x);
            if (x == 1) break;
            x = x / 2;
        }
    }
    '''
    expected = "256" "128" "64" "32" "16" "8" "4" "2" "1"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_033():
    source = '''
    void main() {
        int x = 256;
        for (;;x = x / 2) {
            printInt(x);
            if (x == 1) break;
        }
    }
    '''
    expected = "256" "128" "64" "32" "16" "8" "4" "2" "1"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_034():
    source = '''
    void main() {
        int x = 10;
        while (x--) switch (x) {
            case 9: printInt(9); continue;
            case 5: printInt(5); continue;
            case 0: printInt(0); continue;
        }
    }
    '''
    expected = "950"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_035():
    source = "struct Point { int x; int y; }; void main() { Point p = {1, 2}; auto q = p.x; printInt(q); }"
    expected = "1"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_036():
    source = "void main() { int x = 10; auto y = x * 2; printInt(y); }"
    expected = "20"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_037():
    source = "int f() { return 2; } void main() { auto x = f(); printInt(x); }"
    expected = "2"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_038():
    source = "void main() { int x = 1; auto y = x = 2; printInt(y); }"
    expected = "2"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_039():
    source = '''
    fibo(int n) {
        if (n <= 1) return n;
        auto res = fibo(n - 1) + fibo(n - 2);
        return res;
    }
    void main() { printInt(fibo(10)); }
    '''
    expected = "55"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_040():
    source = '''
    void main() {
        for (int i = 0; i < 4; i++) {
            int x = i;
            if (i % 2) {
                string text = "The odd number are ";
                printString(text);
            } else {
                string the = "The ";
                string even = "even ";
                string number = "number ";
                string are = "are ";
                printString(the); printString(even); printString(number); printString(are);
            }
            printInt(x);
        }
    }
    '''
    expected = "The even number are 0"\
               "The odd number are 1"\
               "The even number are 2"\
               "The odd number are 3"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_041():
    source = '''
    void prettyPrint(string text, int x) {
        printString(text);
        printInt(x);
    }
    void recursive(int n) {
        if (n <= 0) return;
        prettyPrint("Enter ", n);
        recursive(n - 1);
        prettyPrint("Leave ", n);
    }
    void main() { recursive(3); }
    '''
    expected = "Enter 3""Enter 2""Enter 1""Leave 1""Leave 2""Leave 3"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_042():
    source = '''
    f() { auto x; return x = 0; }
    void main() { printInt(f()); }
    '''
    expected = "0"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_043():
    source = "void main() { printInt(1 + 2 * 3 - 5 / 2); }"
    expected = "5"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_044():
    source = "void main() { 1 + 2 * 3 - 5 / 2; }"
    expected = ""
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_045():
    source = '''
    struct Point { int x; int y; };
    struct Line { Point start; Point end; };
    void printLine(Line l) {
        printInt(l.start.x); printString(" ");
        printInt(l.start.y); printString(" ");
        printInt(l.end.x); printString(" ");
        printInt(l.end.y);
    }
    void main() {
        Line l = {{1, 2}, {3, 4}};
        Line m = l;
        printLine(m);
        m.start.x = 10;
        printLine(m);
        m.end = {5, 6};
        printLine(m);
    }
    '''
    expected = "1 2 3 4""10 2 3 4""10 2 5 6"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_046():
    source = '''
    void main() {
        int x;
        x = (x = 10) + x + (x++) + (++x);
        printInt(x);
    }
    '''
    expected = "42"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_047():
    source = '''
    void main() {
        auto x;
        x = (x = 10);
        x = x + (x++) + (++x);
        printInt(x);
    }
    '''
    expected = "32"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_048():
    source = '''
    struct Int { int x; };
    void main() {
        Int x;
        x.x = (x.x = 10) + x.x + (x.x++) + (++x.x);
        printInt(x.x);
    }
    '''
    expected = "42"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_049():
    source = '''
    struct Int { int x; };
    struct I { Int x; };
    void main() {
        I x;
        x.x.x = (x.x.x = 10) + x.x.x + (x.x.x++) + (++x.x.x);
        printInt(x.x.x);
    }
    '''
    expected = "42"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_050():
    source = '''
    void printText(int x) {
        if (x % 2) {
            string text = "The odd number are ";
            printString(text);
            return;
        } else {
            string the = "The ";
            string even = "even ";
            string number = "number ";
            string are = "are ";
            printString(the); printString(even); printString(number); printString(are);
            return;
        }
    }
    void main() {
        for (int i = 0; i < 4; i++) {
            printText(i);
            printInt(i);
        }
    }
    '''
    expected = "The even number are 0"\
               "The odd number are 1"\
               "The even number are 2"\
               "The odd number are 3"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_051():
    source = '''
    void main() {
        int x = 10;
        { int x = 5; printInt(x); }
        printInt(x);
    }
    '''
    expected = "510"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
    
def test_052():
    source = '''
    int a() { printString("a"); return 1; }
    int b() { printString("b"); return 2; }
    void main() { a() || b(); }
    '''
    expected = "a"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_053():
    source = '''
    int a() { printString("a"); return 0; }
    int b() { printString("b"); return 2; }
    void main() { a() && b(); }
    '''
    expected = "a"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_054():
    source = '''
    int a() { printString("a"); return 1; }
    int b() { printString("b"); return 2; }
    void main() { (a() - 1) && (b() + 1); }
    '''
    expected = "a"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_055():
    source = '''
    int a() { printString("a"); return 1; }
    int b() { printString("b"); return 2; }
    void main() { printInt(a() + b() + 3); }
    '''
    expected = "ab6"
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_056():
    source = "void main() { for (int i = 0; i < 3; i++) int i = 0; }"
    expected = ""
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_057():
    source = "void main() { int i = 0; if (i) int i = 1; }"
    expected = ""
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_058():
    source = "void main() { int i = 0; if (i) int i = 0; else int i = 0; }"
    expected = ""
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_059():
    source = "void main() { for (int i = 0; i < 3; i++) continue; }"
    expected = ""
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_060():
    source = "void main() {}"
    expected = ""
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_061():
    source = "void main() { int i = 5; while (i--) int i = 1; }"
    expected = ""
    ast = ASTGenerator(source).generate()
    assert Checker(ast=ast).check_from_ast() == "Static checking passed"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

# TODO: test type inference