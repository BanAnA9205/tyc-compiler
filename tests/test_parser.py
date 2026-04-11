"""Parser test cases for TyC compiler."""

from tests.utils import Parser


def test_parser_000():
    source = ""
    assert Parser(source).parse() == "success"


def test_parser_001():
    source = "void main() {}"
    assert Parser(source).parse() == "success"


def test_parser_002():
    source = "main() {}"
    assert Parser(source).parse() == "success"


def test_parser_003():
    source = "struct Empty {};"
    assert Parser(source).parse() == "success"


def test_parser_004():
    source = "struct Point { int x; float y; };"
    assert Parser(source).parse() == "success"


def test_parser_005():
    source = "int add(int x, int y) { return x + y; }"
    assert Parser(source).parse() == "success"


def test_parser_006():
    source = "void main() { int x; float y; string s; }"
    assert Parser(source).parse() == "success"


def test_parser_007():
    source = "void main() { auto x = 1; }"
    assert Parser(source).parse() == "success"


def test_parser_008():
    source = "void main() { int x; x = 1; }"
    assert Parser(source).parse() == "success"


def test_parser_009():
    source = "void main() { if (1) { } }"
    assert Parser(source).parse() == "success"


def test_parser_010():
    source = "void main() { if (1) return; else return; }"
    assert Parser(source).parse() == "success"


def test_parser_011():
    source = "void main() { while (1) { continue; } }"
    assert Parser(source).parse() == "success"


def test_parser_012():
    source = "void main() { for (int i = 0; i < 10; i = i + 1) { } }"
    assert Parser(source).parse() == "success"


def test_parser_013():
    source = "void main() { switch (1) { case 1: break; default: break; } }"
    assert Parser(source).parse() == "success"


def test_parser_014():
    source = "void main() { foo(1, 2); }"
    assert Parser(source).parse() == "success"


def test_parser_015():
    source = "struct Point { int x; int y; }; void main() { Point p = {1, 2}; }"
    assert Parser(source).parse() == "success"


def test_parser_016():
    source = "struct Point { int x; }; void main() { Point p; p.x++; }"
    assert Parser(source).parse() == "success"


def test_parser_017():
    source = "void main() { int x; x = 1 + 2 * 3; }"
    assert Parser(source).parse() == "success"


def test_parser_018():
    source = "void main() { int x; x = 1 - 2 - 3; }"
    assert Parser(source).parse() == "success"


def test_parser_019():
    source = "void main() { int x }"
    assert Parser(source).parse() == "Error on line 1 col 20: }"


def test_parser_020():
    source = "void main() { if (1) { } else }"
    assert Parser(source).parse() == "Error on line 1 col 30: }"


def test_parser_021():
    source = "void main() { int x; x = (1 + 2) * 3; }"
    assert Parser(source).parse() == "success"


def test_parser_022():
    source = "void main() { int x; x = -1 + +2; }"
    assert Parser(source).parse() == "success"


def test_parser_023():
    source = "void main() { int x; x = !1 && 0 || 1; }"
    assert Parser(source).parse() == "success"


def test_parser_024():
    source = "void main() { int x; x = 1 == 2 < 3; }"
    assert Parser(source).parse() == "success"


def test_parser_025():
    source = "void main() { int x; x = y = 1; }"
    assert Parser(source).parse() == "success"


def test_parser_026():
    source = "void main() { int x; x = ++y + z--; }"
    assert Parser(source).parse() == "success"


def test_parser_027():
    source = "void main() { int x; x = foo(1, 2) + bar(); }"
    assert Parser(source).parse() == "success"


def test_parser_028():
    source = "struct Pair { int x; int y; }; void foo(Pair p) { } void main() { foo({1, 2}); }"
    assert Parser(source).parse() == "success"


def test_parser_029():
    source = "void main() { int x; x = (a.b).c; }"
    assert Parser(source).parse() == "success"


def test_parser_030():
    source = "void main() { int x; x = a.b++ + --c.d; }"
    assert Parser(source).parse() == "success"


def test_parser_031():
    source = "void main() { if (1) if (0) return; else return; }"
    assert Parser(source).parse() == "success"


def test_parser_032():
    source = "void main() { { int x; x = 1; } }"
    assert Parser(source).parse() == "success"


def test_parser_033():
    source = "void main() { for (; i < 10; ) { } }"
    assert Parser(source).parse() == "success"


def test_parser_034():
    source = "void main() { int i; for (i = 0; i < 10; i++) { } }"
    assert Parser(source).parse() == "success"


def test_parser_035():
    source = "void main() { while (i) i = i - 1; }"
    assert Parser(source).parse() == "success"


def test_parser_036():
    source = "void main() { switch (1) { case 1: break; case 2: break; default: break; } }"
    assert Parser(source).parse() == "success"


def test_parser_037():
    source = "int calc() { return 1 + 2 * 3; } void main() {}"
    assert Parser(source).parse() == "success"


def test_parser_038():
    source = "void main() { for (;;) { if (1) break; else continue; } }"
    assert Parser(source).parse() == "success"


def test_parser_039():
    source = "void main() { a.b.c = d.e; }"
    assert Parser(source).parse() == "success"


def test_parser_040():
    source = "void main() { if (1) else return; }"
    expected = "Error on line 1 col 21: else"
    assert Parser(source).parse() == expected


def test_parser_041():
    source = "void main() { int x; x = a < b + c * d == e || f && g < h; }"
    assert Parser(source).parse() == "success"


def test_parser_042():
    source = "void main() { int x; x = a + b - c + d * e / f % g; }"
    assert Parser(source).parse() == "success"


def test_parser_043():
    source = "void main() { int x; x = a == b < c == d < e; }"
    assert Parser(source).parse() == "success"


def test_parser_044():
    source = "void main() { int x; x = a = b < c == d && e || f; }"
    assert Parser(source).parse() == "success"


def test_parser_045():
    source = "void main() { int x; x = a.b++ * --c.d + e.f-- / g; }"
    assert Parser(source).parse() == "success"


def test_parser_046():
    source = "void main() { int x; x = ++a + b-- * -c + !d; }"
    assert Parser(source).parse() == "success"


def test_parser_047():
    source = "void main() { int x; x = a = b = c = d + e * f < g; }"
    assert Parser(source).parse() == "success"


def test_parser_048():
    source = "void main() { int x; x = a.b.c = d.e + f * g - h / i % j; }"
    assert Parser(source).parse() == "success"


def test_parser_049():
    source = "void main() { int x; x = a < b && c == d || e != f && g < h; }"
    assert Parser(source).parse() == "success"


def test_parser_050():
    source = "void main() { int x; x = a + b < c == d != e < f; }"
    assert Parser(source).parse() == "success"


def test_parser_051():
    source = "void main() { int x; x = a.b + c.d * e.f < g.h || i.j; }"
    assert Parser(source).parse() == "success"


def test_parser_052():
    source = "void main() { int x; x = a = b == c != d < e; }"
    assert Parser(source).parse() == "success"


def test_parser_053():
    source = "void main() { int x; x = a < b < c; }"
    assert Parser(source).parse() == "success"


def test_parser_054():
    source = "void main() { int x; x = a + b * c == d && e || f; }"
    assert Parser(source).parse() == "success"


def test_parser_055():
    source = "void main() { int x; x = a = b + c * d == e; }"
    assert Parser(source).parse() == "success"


def test_parser_056():
    source = "void main() { int x; x = a && b || c && d || e; }"
    assert Parser(source).parse() == "success"


def test_parser_057():
    source = "void main() { int x; x = a = b = c + d * e / f % g; }"
    assert Parser(source).parse() == "success"


def test_parser_058():
    source = "void main() { int x; x = a.b++ + --c.d * e - f / g + h; }"
    assert Parser(source).parse() == "success"


def test_parser_059():
    source = "void main() { int x; x = !a + b * c; }"
    assert Parser(source).parse() == "success"


def test_parser_060():
    source = "void main() { int x; x = a = b < c && d < e || f; }"
    assert Parser(source).parse() == "success"


def test_parser_061():
    source = "struct S { int x; }; void main() { S s; int x; x = s.x < a + b * c || d < e && f < g; }"
    assert Parser(source).parse() == "success"


def test_parser_062():
    source = "void main() { int x; x = a + b++ * --c / d % e - f; }"
    assert Parser(source).parse() == "success"


def test_parser_063():
    source = "void main() { int x; x = a = b = c.d + e * f - g / h; }"
    assert Parser(source).parse() == "success"


def test_parser_064():
    source = "void main() { int x; x = a = b == c < d || e && f; }"
    assert Parser(source).parse() == "success"


def test_parser_065():
    source = "void main() { int x; x = a.b.c++ * --d.e.f + g.h--; }"
    assert Parser(source).parse() == "success"


def test_parser_066():
    source = "void main() { int x; x = a = b == c != d; }"
    assert Parser(source).parse() == "success"


def test_parser_067():
    source = (
        "struct Pair { int x; int y; }; int foo(Pair p, int v) { return v; } "
        "int bar(int d) { return d; } int baz() { return 1; } "
        "void main() { int a; int b; int c; int d; int x; "
        "x = foo({1,2}, a + b * c) != bar(d) && baz(); }"
    )
    assert Parser(source).parse() == "success"


def test_parser_068():
    source = (
        "struct Pair { int x; int y; }; int sumPair(Pair p) { return p.x + p.y * 2; } "
        "void main() { Pair p = {1,2}; int x; x = sumPair(p); }"
    )
    assert Parser(source).parse() == "success"


def test_parser_069():
    source = "void main() { for (int i = 0; i = i + 1 < 10 && j < k; i++) { } }"
    assert Parser(source).parse() == "success"


def test_parser_070():
    source = "void main() { while (a = b < c || d && e) { continue; } }"
    assert Parser(source).parse() == "success"


def test_parser_071():
    source = "void main() { if (a < b == c < d && e != f) return; }"
    assert Parser(source).parse() == "success"


def test_parser_072():
    source = "void main() { switch (a + b * c) { case 1+2: break; case -3: break; default: break; } }"
    assert Parser(source).parse() == "success"


def test_parser_073():
    source = "int calc() { return a = b = c = d + e * f - g; } void main() {}"
    assert Parser(source).parse() == "success"


def test_parser_074():
    source = "void main() { a = b = c == d != e == f; }"
    assert Parser(source).parse() == "success"


def test_parser_075():
    source = "void main() { if (a && b || c && d == e < f) return; }"
    assert Parser(source).parse() == "success"


def test_parser_076():
    source = (
        "void main() { for (; i = i + 1 < 10 && j < k || l < m; ) if (i && j || k && l < m) break; }"
    )
    assert Parser(source).parse() == "success"


def test_parser_077():
    source = "void main() { int x; x = a + b * c + d / e - f % g; }"
    assert Parser(source).parse() == "success"


def test_parser_078():
    source = "void main() { int x; x = a < b + c * d == e; }"
    assert Parser(source).parse() == "success"


def test_parser_079():
    source = "void main() { int x; x = a.b++ + ++c.d - e.f--; }"
    assert Parser(source).parse() == "success"


def test_parser_080():
    source = "void main() { int x; x = a + b < c == d && e || f; }"
    assert Parser(source).parse() == "success"


def test_parser_081():
    source = (
        "struct Vec { int x; int y; }; struct Line { Vec a; Vec b; }; "
        "int sum(Vec v) { return v.x + v.y; } "
        "int main() { Line l = {{1,2},{3,4}}; int s; s = sum(l.a) + sum(l.b) * 2; return s; }"
    )
    assert Parser(source).parse() == "success"


def test_parser_082():
    source = "compute(int a, int b) { return a + b * (a - b); } void main() { int r; r = compute(1, 2); }"
    assert Parser(source).parse() == "success"


def test_parser_083():
    source = (
        "void main() { for (int i = 0; i < 3; ++i) { switch (i + 1 * 2) "
        "{ case 1: i = i + 1; break; case 2: i = i + 2; default: break; } } }"
    )
    assert Parser(source).parse() == "success"


def test_parser_084():
    source = "void main() { while (a) if (b) if (c) break; else continue; }"
    assert Parser(source).parse() == "success"


def test_parser_085():
    source = (
        "struct Pair { int x; int y; }; int dot(Pair p) { return p.x * p.y; } "
        "int main() { Pair p = {1,2}; int v; v = dot(p) + p.x; return v; }"
    )
    assert Parser(source).parse() == "success"


def test_parser_086():
    source = "struct Empty {}; void use(Empty e) { } void main() { Empty e = { }; }"
    assert Parser(source).parse() == "success"


def test_parser_087():
    source = "void main() { int x; while (x = a.b + c.d * e.f) { x = x - 1; } }"
    assert Parser(source).parse() == "success"


def test_parser_088():
    source = "int main() { return a < b == c < d || e && f; }"
    assert Parser(source).parse() == "success"


def test_parser_089():
    source = "void main() { for (i = 0; i < 10; a.b++) { if (i % 2 == 0) continue; } }"
    assert Parser(source).parse() == "success"


def test_parser_090():
    source = "void main() { switch (x) { case 1: if (y) y = y + 1; default: { int y; y = 1; } } }"
    assert Parser(source).parse() == "success"


def test_parser_091():
    source = "struct Bad { int x; }"
    expected = "Error on line 1 col 21: <EOF>"
    assert Parser(source).parse() == expected


def test_parser_092():
    source = "void main() { for (int i = 0 i < 10; i++) { } }"
    expected = "Error on line 1 col 29: i"
    assert Parser(source).parse() == expected


def test_parser_093():
    source = (
        "struct Point { int x; int y; }; int sumCoords(int a, int b) { return a + b; } "
        "void main() { Point p = {1,2}; int r; r = sumCoords(p.x, p.y * 2); }"
    )
    assert Parser(source).parse() == "success"


def test_parser_094():
    source = "float avg(int a, int b) { return (a + b) / 2; } void main() { auto x = avg(1,2); auto y = avg(x, 4); }"
    assert Parser(source).parse() == "success"


def test_parser_095():
    source = "void main() { if (a) { for (int i = 0; i < 2; i++) { if (i) break; } } else { return; } }"
    assert Parser(source).parse() == "success"


def test_parser_096():
    source = "void main() { a.b.c = d.e.f = g + h * i; }"
    assert Parser(source).parse() == "success"


def test_parser_097():
    source = "void main() { int x; x = --a.b + (c.d--); }"
    assert Parser(source).parse() == "success"


def test_parser_098():
    source = "void main() { for (int i = 0; i < 3; i++) { switch (i) { case 0: if (a || b && c) break; default: continue; } } }"
    assert Parser(source).parse() == "success"


def test_parser_099():
    source = "struct Node { int value; }; struct Box { Node n; }; void main() { Box b; b.n = {1}; }"
    assert Parser(source).parse() == "success"


def test_parser_100():
    source = (
        "struct A { int x; int y; }; struct B { A a; int z; }; "
        "calc(A a, int k) { return a.x + a.y * k; } "
        "int main() { B b = {{1,2},3}; int r; r = calc(b.a, b.z) == 7 || b.z < 10 && b.a.x < b.a.y; "
        "if (r) { for (int i = 0; i < 2; i = i + 1) { b.z = b.z + i; } } return r; }"
    )
    assert Parser(source).parse() == "success"


def test_parser_101():
    source = "void main( { }"
    expected = "Error on line 1 col 11: {"
    assert Parser(source).parse() == expected


def test_parser_102():
    source = "struct S { int x int y; };"
    expected = "Error on line 1 col 17: int"
    assert Parser(source).parse() == expected


def test_parser_103():
    source = "void main() { if (1) { return; } else else return; }"
    expected = "Error on line 1 col 38: else"
    assert Parser(source).parse() == expected


def test_parser_104():
    source = "void main() { while (1) break }"
    expected = "Error on line 1 col 30: }"
    assert Parser(source).parse() == expected


def test_parser_105():
    source = "void main() { for (int i = 0; i < 10 i++) { } }"
    expected = "Error on line 1 col 37: i"
    assert Parser(source).parse() == expected


def test_parser_106():
    source = "void main() { switch (1) { case: break; } }"
    expected = "Error on line 1 col 31: :"
    assert Parser(source).parse() == expected


def test_parser_107():
    source = "void main() { return 1 + ; }"
    expected = "Error on line 1 col 25: ;"
    assert Parser(source).parse() == expected


def test_parser_108():
    source = "void main() { int x = 1 +; }"
    expected = "Error on line 1 col 25: ;"
    assert Parser(source).parse() == expected


def test_parser_109():
    source = "void main() { for (;; ) break }"
    expected = "Error on line 1 col 30: }"
    assert Parser(source).parse() == expected


def test_parser_110():
    source = "struct S { int x; }; void main() { S s = {1,}; }"
    expected = "Error on line 1 col 44: }"
    assert Parser(source).parse() == expected


def test_parser_111():
    source = "void main() { if (1) { } else { "
    expected = "Error on line 1 col 32: <EOF>"
    assert Parser(source).parse() == expected


def test_parser_112():
    source = "void main() { int x; x = (1 + 2; }"
    expected = "Error on line 1 col 31: ;"
    assert Parser(source).parse() == expected


def test_parser_113():
    source = "void main() { int x; x = 1 + * 2; }"
    expected = "Error on line 1 col 29: *"
    assert Parser(source).parse() == expected


def test_parser_114():
    source = "void main() { for (int i = 0; i < 3; i++) switch (i) { case 0: break default: break; } }"
    expected = "Error on line 1 col 69: default"
    assert Parser(source).parse() == expected


def test_parser_115():
    source = "struct A { int x; } struct B { int y; };"
    expected = "Error on line 1 col 20: struct"
    assert Parser(source).parse() == expected


def test_parser_116():
    source = "void main() { while (1) { continue } }"
    expected = "Error on line 1 col 35: }"
    assert Parser(source).parse() == expected


def test_parser_117():
    source = "void main() { if (1) return else return; }"
    expected = "Error on line 1 col 28: else"
    assert Parser(source).parse() == expected


def test_parser_118():
    source = "void main() { a..b = 1; }"
    expected = "Error on line 1 col 16: ."
    assert Parser(source).parse() == expected


def test_parser_119():
    source = "void main() { int x; x = {1 2}; }"
    expected = "Error on line 1 col 28: 2"
    assert Parser(source).parse() == expected


def test_parser_120():
    source = "void main() { for (int i = 0; i < 3; i++) { case 1: break; } }"
    expected = "Error on line 1 col 44: case"  
    assert Parser(source).parse() == expected


def test_parser_121():
    source = "struct A { int x; int y; }; struct B { A a int z; }; void main() { B b; }"
    expected = "Error on line 1 col 43: int"
    assert Parser(source).parse() == expected


def test_parser_122():
    source = (
        "struct P { int x; int y; }; int sum(P p) { return p.x +; } "
        "int main() { P p = {1,2}; return sum(p); }"
    )
    expected = "Error on line 1 col 55: ;"
    assert Parser(source).parse() == expected


def test_parser_123():
    source = (
        "struct P { int x; int y; }; int sum(P p) { return p.x + p.y; } "
        "int main() { P p = {1,2}; return sum(p) }"
    )
    expected = "Error on line 1 col 103: }"
    assert Parser(source).parse() == expected


def test_parser_124():
    source = (
        "struct P { int x; int y; }; int main() { P p = {1,2}; if (p.x < p.y) { return 1; } "
        "else { return 0; }"
    )
    expected = "Error on line 1 col 101: <EOF>"
    assert Parser(source).parse() == expected


def test_parser_125():
    source = (
        "struct N { int v; }; struct M { N n; }; int main() { M m = {{1}}; "
        "switch (m.n.v) { case 1 break; default: break; } }"
    )
    expected = "Error on line 1 col 90: break"
    assert Parser(source).parse() == expected


def test_parser_126():
    source = (
        "struct A { int x; }; int main() { A a; for (int i = 0; i < 2; i++) { a.x = a.x + i } "
        "return a.x; }"
    )
    expected = "Error on line 1 col 85: return"
    assert Parser(source).parse() == expected


def test_parser_127():
    source = (
        "struct A { int x; }; int main() { A a; while (a.x < 10) { a.x = a.x + 1; } else return 0; }"
    )
    expected = "Error on line 1 col 75: else"
    assert Parser(source).parse() == expected


def test_parser_128():
    source = "struct A { int x; }; int main() { A a; a.x = (1 + 2; return a.x; }"
    expected = "Error on line 1 col 51: ;"
    assert Parser(source).parse() == expected


def test_parser_129():
    source = "struct A { int x; int y; }; int main() { A a = {1,2,}; return a.x; }"
    expected = "Error on line 1 col 52: }"
    assert Parser(source).parse() == expected


def test_parser_130():
    source = (
        "struct A { int x; }; int f(int x) { return x; } int main() { A a; a.x = f(1,2; return a.x; }"
    )
    expected = "Error on line 1 col 77: ;"
    assert Parser(source).parse() == expected


def test_parser_131():
    source = (
        "struct A { int x; int y; }; int main() { A a = {1,2}; if (a.x < a.y) return 1 else return 0; }"
    )
    expected = "Error on line 1 col 78: else"
    assert Parser(source).parse() == expected


def test_parser_132():
    source = (
        "struct A { int x; }; int main() { switch (a.x) { case 1: { int y; y = 1; } "
        "case 2: break; default: break; "
    )
    expected = "Error on line 1 col 106: <EOF>"
    assert Parser(source).parse() == expected


def test_parser_133():
    source = "struct A { int x; }; int main() { for (int i = 0; i < 2; i+) { a.x = a.x + i; } return a.x; }"
    expected = "Error on line 1 col 59: )"
    assert Parser(source).parse() == expected


def test_parser_134():
    source = "struct A { int x; }; int main() { for (int i = 0; i < 2; i++) { if (i) break; } return i }"
    expected = "Error on line 1 col 89: }"
    assert Parser(source).parse() == expected


def test_parser_135():
    source = "struct A { int x; }; int main() { int i; for (i = 0; i < 2; i++) { } } return i;"
    expected = "Error on line 1 col 71: return"
    assert Parser(source).parse() == expected


def test_parser_136():
    source = "struct A { int x; }; int main() { A a; a.x = 1; if (a.x) { return a.x; } else { return a.x; }"
    expected = "Error on line 1 col 93: <EOF>"
    assert Parser(source).parse() == expected


def test_parser_137():
    source = "struct A { int x; }; int main() { A a; switch (a.x) { case 1:: break; default: break; } }"
    expected = "Error on line 1 col 61: :"
    assert Parser(source).parse() == expected


def test_parser_138():
    source = "struct A { int x; int y; }; int main() { A a; a..x = 1; return a.x; }"
    expected = "Error on line 1 col 48: ."
    assert Parser(source).parse() == expected


def test_parser_139():
    source = (
        "struct A { int x; }; int main() { A a; for (int i = 0; i < 2; i++) { if (i) { return a.x; } "
        "else { return a.x; } }"
    )
    expected = "Error on line 1 col 114: <EOF>"
    assert Parser(source).parse() == expected


def test_parser_140():
    source = (
        "struct A { int x; int y; }; struct B { A a; }; int main() { B b = {{1,2}}; "
        "if (b.a.x < b.a.y) { return b.a.x; } else { return b.a.y; }"
    )
    expected = "Error on line 1 col 134: <EOF>"
    assert Parser(source).parse() == expected


def test_parser_141():
    source = (
        "void main() { int x; x = a.b++ + --c.d * -e.f / +g % h == i != j < k <= l > m >= n && !o || p; }"
    )
    assert Parser(source).parse() == "success"


def test_parser_142():
    source = "void main() { int x; x = a = b = c.d = e + f * g - h / i % j; }"
    assert Parser(source).parse() == "success"


def test_parser_143():
    source = "void main() { int x; x = !a < b && c == d || e != f && ++g < h--; }"
    assert Parser(source).parse() == "success"


def test_parser_144():
    source = "void main() { int x; x = a + b * c - d / e % f + g * h - i; }"
    assert Parser(source).parse() == "success"


def test_parser_145():
    source = "void main() { int x; x = a = b + c == d = e - f && g = h * i || j = k / l; }"
    assert Parser(source).parse() == "success"


def test_parser_146():
    source = (
        "struct S { int x; }; void main() { S s; { int i; for (i = 0; i < 2; i++) { "
        "while (i < 1) { break; } } } }"
    )
    assert Parser(source).parse() == "success"


def test_parser_147():
    source = "int main() { int x; switch (x) { case 0: { int y; y = 1; } break; default: return 0; } }"
    assert Parser(source).parse() == "success"


def test_parser_148():
    source = "void main() { switch (1) { default: break; default: break; } }"
    expected = "Error on line 1 col 43: default"
    assert Parser(source).parse() == expected


def test_parser_149():
    source = "void main() { switch (x) { case 1: break; case 2: break; default: break; default: break; } }"
    expected = "Error on line 1 col 73: default"
    assert Parser(source).parse() == expected


def test_parser_150():
    source = "void main() { while (1) { switch (x) { case 1: break; default: break; default: break; } } }"
    expected = "Error on line 1 col 70: default"
    assert Parser(source).parse() == expected


def test_parser_151():
    source = "int main() { a.b++ * -c + d == e && f || g = h; if (a || b = 3) return 1; return 0; }"
    assert Parser(source).parse() == "success"


def test_parser_152():
    source = "\nvoid main() {\n    for (;;) loop();\n    for ( ; x ; ) loop();\n    for ( ; ; x++ ) loop();\n    for ( i = 0 ; i < 10 ; i++ ) loop();\n}\n"
    assert Parser(source).parse() == "success"
