import pytest
from tests.utils import ASTGenerator
from src.utils.nodes import *

def test_ast_001():
    """Single void function with no parameters and empty body."""
    source = "void main() {}"
    expected = Program([
        FuncDecl(VoidType(), 'main', [], BlockStmt([]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_002():
    """Single empty struct declaration."""
    source = "struct Empty {};"
    expected = Program([
        StructDecl('Empty', [])
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_003():
    """Function followed by a struct at the top level."""
    source = "void foo() {} struct Bar {};"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([])),
        StructDecl('Bar', []),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_004():
    """Single struct with two int members."""
    source = "struct Point { int x; int y; };"
    expected = Program([
        StructDecl('Point', [
            MemberDecl(IntType(), 'x'),
            MemberDecl(IntType(), 'y'),
        ])
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_005():
    """Struct with all three primitive member types."""
    source = "struct Person { string name; int age; float height; };"
    expected = Program([
        StructDecl('Person', [
            MemberDecl(StringType(), 'name'),
            MemberDecl(IntType(), 'age'),
            MemberDecl(FloatType(), 'height'),
        ])
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_006():
    """Function with explicit int return type and two int parameters."""
    source = "int add(int x, int y) { return x + y; }"
    expected = Program([
        FuncDecl(IntType(), 'add', [
            Param(IntType(), 'x'),
            Param(IntType(), 'y'),
        ], BlockStmt([
            ReturnStmt(BinaryOp(Identifier('x'), '+', Identifier('y')))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_007():
    """Function with inferred return type (omitted)."""
    source = "multiply(float a, float b) { return a * b; }"
    expected = Program([
        FuncDecl(None, 'multiply', [
            Param(FloatType(), 'a'),
            Param(FloatType(), 'b'),
        ], BlockStmt([
            ReturnStmt(BinaryOp(Identifier('a'), '*', Identifier('b')))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_008():
    """void function with a single string parameter and a function call body."""
    source = 'void greet(string name) { printString(name); }'
    expected = Program([
        FuncDecl(VoidType(), 'greet', [
            Param(StringType(), 'name'),
        ], BlockStmt([
            ExprStmt(FuncCall('printString', [Identifier('name')]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_009():
    """Variable declarations: explicit types without initialisation."""
    source = "void foo() { int a; float b; string c; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'a'),
            VarDecl(FloatType(), 'b'),
            VarDecl(StringType(), 'c'),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_010():
    """Variable declarations: auto with literal initialisations."""
    source = 'void foo() { auto x = 10; auto y = 3.14; auto s = "hi"; }'
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'x', IntLiteral(10)),
            VarDecl(None, 'y', FloatLiteral(3.14)),
            VarDecl(None, 's', StringLiteral('hi')),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_011():
    """Variable declarations: explicit types with literal initialisations."""
    source = 'void foo() { int a = 5; float b = 1.5; string c = "ok"; }'
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'a', IntLiteral(5)),
            VarDecl(FloatType(), 'b', FloatLiteral(1.5)),
            VarDecl(StringType(), 'c', StringLiteral('ok')),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_012():
    """Struct with a member that is another struct type."""
    source = "struct A { int v; }; struct B { A a; int w; };"
    expected = Program([
        StructDecl('A', [
            MemberDecl(IntType(), 'v'),
        ]),
        StructDecl('B', [
            MemberDecl(StructType('A'), 'a'),
            MemberDecl(IntType(), 'w'),
        ]),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_013():
    """Mixed top-level: struct then void main with bare return."""
    source = "struct Point { int x; int y; }; void main() { return; }"
    expected = Program([
        StructDecl('Point', [
            MemberDecl(IntType(), 'x'),
            MemberDecl(IntType(), 'y'),
        ]),
        FuncDecl(VoidType(), 'main', [], BlockStmt([
            ReturnStmt()
        ])),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_014():
    """Function with struct-type parameter and struct-type return."""
    source = "Point identity(Point p) { return p; }"
    expected = Program([
        FuncDecl(StructType('Point'), 'identity', [
            Param(StructType('Point'), 'p'),
        ], BlockStmt([
            ReturnStmt(Identifier('p'))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_015():
    """auto variable without initialisation followed by assignment."""
    source = "void foo() { auto x; x = 42; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'x'),
            ExprStmt(AssignExpr(Identifier('x'), IntLiteral(42))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_016():
    """Struct variable declaration: without init and with StructLiteral init."""
    source = "void foo() { Point p1; Point p2 = {10, 20}; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(StructType('Point'), 'p1'),
            VarDecl(StructType('Point'), 'p2',
                    StructLiteral([IntLiteral(10), IntLiteral(20)])),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_017():
    """Return statement with no expression in a void function."""
    source = "void foo() { return; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ReturnStmt()
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_018():
    """Function with four mixed-type parameters."""
    source = "float calc(int a, float b, int c, string s) { return b; }"
    expected = Program([
        FuncDecl(FloatType(), 'calc', [
            Param(IntType(), 'a'),
            Param(FloatType(), 'b'),
            Param(IntType(), 'c'),
            Param(StringType(), 's'),
        ], BlockStmt([
            ReturnStmt(Identifier('b'))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_019():
    """Two structs (one nesting the other); function creates and returns nested struct."""
    source = (
        "struct Vec2 { float x; float y; };"
        "struct Vec3 { Vec2 xy; float z; };"
        "Vec3 make(Vec2 v, float z) { Vec3 r = {v, z}; return r; }"
    )
    expected = Program([
        StructDecl('Vec2', [
            MemberDecl(FloatType(), 'x'),
            MemberDecl(FloatType(), 'y'),
        ]),
        StructDecl('Vec3', [
            MemberDecl(StructType('Vec2'), 'xy'),
            MemberDecl(FloatType(), 'z'),
        ]),
        FuncDecl(StructType('Vec3'), 'make', [
            Param(StructType('Vec2'), 'v'),
            Param(FloatType(), 'z'),
        ], BlockStmt([
            VarDecl(StructType('Vec3'), 'r',
                    StructLiteral([Identifier('v'), Identifier('z')])),
            ReturnStmt(Identifier('r')),
        ])),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_020():
    """Inferred-return function; auto var from member access; member assignments; return struct."""
    source = (
        "struct Pair { int a; int b; };"
        "swap(Pair p) {"
        "    auto tmp = p.a;"
        "    p.a = p.b;"
        "    p.b = tmp;"
        "    return p;"
        "}"
    )
    expected = Program([
        StructDecl('Pair', [
            MemberDecl(IntType(), 'a'),
            MemberDecl(IntType(), 'b'),
        ]),
        FuncDecl(None, 'swap', [
            Param(StructType('Pair'), 'p'),
        ], BlockStmt([
            VarDecl(None, 'tmp', MemberAccess(Identifier('p'), 'a')),
            ExprStmt(AssignExpr(
                MemberAccess(Identifier('p'), 'a'),
                MemberAccess(Identifier('p'), 'b'),
            )),
            ExprStmt(AssignExpr(
                MemberAccess(Identifier('p'), 'b'),
                Identifier('tmp'),
            )),
            ReturnStmt(Identifier('p')),
        ])),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_021():
    """Arithmetic precedence: * and % bind tighter than + and -, left-associative."""
    source = "void foo() { auto x = 1 + 2 * 3 - 8 % 3 + 4 / 2; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'x',
                BinaryOp(
                    BinaryOp(
                        BinaryOp(
                            IntLiteral(1),
                            '+',
                            BinaryOp(IntLiteral(2), '*', IntLiteral(3))
                        ),
                        '-',
                        BinaryOp(IntLiteral(8), '%', IntLiteral(3))
                    ),
                    '+',
                    BinaryOp(IntLiteral(4), '/', IntLiteral(2))
                ))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_022():
    """Left-associativity of * / % across a chain of five operands."""
    source = "void foo() { auto x = 60 / 3 * 2 % 7 / 1; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'x',
                BinaryOp(
                    BinaryOp(
                        BinaryOp(
                            BinaryOp(IntLiteral(60), '/', IntLiteral(3)),
                            '*', IntLiteral(2)
                        ),
                        '%', IntLiteral(7)
                    ),
                    '/', IntLiteral(1)
                ))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_023():
    """Relational operators have lower precedence than arithmetic."""
    source = "void foo() { auto a = 2 + 3 < 4 * 2; auto b = 10 - 1 == 3 * 3; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'a',
                BinaryOp(
                    BinaryOp(IntLiteral(2), '+', IntLiteral(3)),
                    '<',
                    BinaryOp(IntLiteral(4), '*', IntLiteral(2))
                )),
            VarDecl(None, 'b',
                BinaryOp(
                    BinaryOp(IntLiteral(10), '-', IntLiteral(1)),
                    '==',
                    BinaryOp(IntLiteral(3), '*', IntLiteral(3))
                )),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_024():
    """Logical operators: ! has higher precedence than &&, which beats ||; right-to-left for !."""
    source = "void foo() { auto r = !a && b || !c && d; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'r',
                BinaryOp(
                    BinaryOp(
                        PrefixOp('!', Identifier('a')),
                        '&&',
                        Identifier('b')
                    ),
                    '||',
                    BinaryOp(
                        PrefixOp('!', Identifier('c')),
                        '&&',
                        Identifier('d')
                    )
                ))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_025():
    """Prefix ops in expressions: unary minus/plus combined with arithmetic."""
    source = "void foo() { auto a = -x + +y; auto b = -(x * y); auto c = +x - -y; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'a',
                BinaryOp(PrefixOp('-', Identifier('x')), '+', PrefixOp('+', Identifier('y')))),
            VarDecl(None, 'b',
                PrefixOp('-', BinaryOp(Identifier('x'), '*', Identifier('y')))),
            VarDecl(None, 'c',
                BinaryOp(PrefixOp('+', Identifier('x')), '-', PrefixOp('-', Identifier('y')))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_026():
    """Postfix ops in expressions: result used in arithmetic and comparisons."""
    source = "void foo() { int x = 5; int y = 3; auto a = x++ + y--; auto b = x++ > y--; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(5)),
            VarDecl(IntType(), 'y', IntLiteral(3)),
            VarDecl(None, 'a',
                BinaryOp(PostfixOp('++', Identifier('x')), '+', PostfixOp('--', Identifier('y')))),
            VarDecl(None, 'b',
                BinaryOp(PostfixOp('++', Identifier('x')), '>', PostfixOp('--', Identifier('y')))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_027():
    """Precedence: * binds tighter than +."""
    source = "void foo() { auto x = 2 + 3 * 4; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'x',
                BinaryOp(IntLiteral(2), '+',
                    BinaryOp(IntLiteral(3), '*', IntLiteral(4)))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_028():
    """Precedence: relational binds tighter than &&, which binds tighter than ||."""
    source = "void foo() { auto r = 1 < 2 && 3 > 0 || 0; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'r',
                BinaryOp(
                    BinaryOp(
                        BinaryOp(IntLiteral(1), '<', IntLiteral(2)),
                        '&&',
                        BinaryOp(IntLiteral(3), '>', IntLiteral(0))
                    ),
                    '||',
                    IntLiteral(0)
                )),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_029():
    """Left-associativity of + and -."""
    source = "void foo() { auto x = 1 + 2 + 3 - 4; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'x',
                BinaryOp(
                    BinaryOp(
                        BinaryOp(IntLiteral(1), '+', IntLiteral(2)),
                        '+', IntLiteral(3)),
                    '-', IntLiteral(4))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_030():
    """Right-associativity of assignment: x = y = 0."""
    source = "void foo() { int x; int y; x = y = 0; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x'),
            VarDecl(IntType(), 'y'),
            ExprStmt(AssignExpr(
                Identifier('x'),
                AssignExpr(Identifier('y'), IntLiteral(0))
            )),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_031():
    """If with compound arithmetic/logical condition and multi-statement body."""
    source = "void foo() { int x = 4; int y = 9; int z = 1; if (x * 2 + 1 > y - 3 && !z) { x = x + 1; y = y - 1; } }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(4)),
            VarDecl(IntType(), 'y', IntLiteral(9)),
            VarDecl(IntType(), 'z', IntLiteral(1)),
            IfStmt(
                BinaryOp(
                    BinaryOp(
                        BinaryOp(
                            BinaryOp(Identifier('x'), '*', IntLiteral(2)),
                            '+',
                            IntLiteral(1)
                        ),
                        '>',
                        BinaryOp(Identifier('y'), '-', IntLiteral(3))
                    ),
                    '&&',
                    PrefixOp('!', Identifier('z'))
                ),
                BlockStmt([
                    ExprStmt(AssignExpr(Identifier('x'), BinaryOp(Identifier('x'), '+', IntLiteral(1)))),
                    ExprStmt(AssignExpr(Identifier('y'), BinaryOp(Identifier('y'), '-', IntLiteral(1)))),
                ]),
                None
            ),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_032():
    """If-else statement with block bodies."""
    source = "void foo() { int x = 5; if (x > 0) { printInt(1); } else { printInt(0); } }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(5)),
            IfStmt(
                BinaryOp(Identifier('x'), '>', IntLiteral(0)),
                BlockStmt([ExprStmt(FuncCall('printInt', [IntLiteral(1)]))]),
                BlockStmt([ExprStmt(FuncCall('printInt', [IntLiteral(0)]))])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_033():
    """Nested if-else: else binds to innermost if."""
    source = "void foo() { int x = 1; int y = 1; if (x) if (y) printInt(1); else printInt(2); }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(1)),
            VarDecl(IntType(), 'y', IntLiteral(1)),
            IfStmt(
                Identifier('x'),
                IfStmt(
                    Identifier('y'),
                    ExprStmt(FuncCall('printInt', [IntLiteral(1)])),
                    ExprStmt(FuncCall('printInt', [IntLiteral(2)]))
                )
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_034():
    """While loop with compound condition (arithmetic + logical) and multi-statement body."""
    source = "void foo() { int i = 0; int n = 16; int flag = 1; while (i * i < n && i % 2 == 0 || flag) { i = i + 2; n = n - i; flag = 0; } }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'i', IntLiteral(0)),
            VarDecl(IntType(), 'n', IntLiteral(16)),
            VarDecl(IntType(), 'flag', IntLiteral(1)),
            WhileStmt(
                BinaryOp(
                    BinaryOp(
                        BinaryOp(
                            BinaryOp(Identifier('i'), '*', Identifier('i')),
                            '<',
                            Identifier('n')
                        ),
                        '&&',
                        BinaryOp(
                            BinaryOp(Identifier('i'), '%', IntLiteral(2)),
                            '==',
                            IntLiteral(0)
                        )
                    ),
                    '||',
                    Identifier('flag')
                ),
                BlockStmt([
                    ExprStmt(AssignExpr(Identifier('i'), BinaryOp(Identifier('i'), '+', IntLiteral(2)))),
                    ExprStmt(AssignExpr(Identifier('n'), BinaryOp(Identifier('n'), '-', Identifier('i')))),
                    ExprStmt(AssignExpr(Identifier('flag'), IntLiteral(0))),
                ])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_035():
    """While loop with block body containing break."""
    source = "void foo() { while (1) { break; } }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            WhileStmt(
                IntLiteral(1),
                BlockStmt([BreakStmt()])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_036():
    """While loop with continue statement."""
    source = "void foo() { int i = 0; while (i < 5) { i++; continue; } }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'i', IntLiteral(0)),
            WhileStmt(
                BinaryOp(Identifier('i'), '<', IntLiteral(5)),
                BlockStmt([
                    ExprStmt(PostfixOp('++', Identifier('i'))),
                    ContinueStmt(),
                ])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_037():
    """For loop with all three parts present."""
    source = "void foo() { for (int i = 0; i < 10; ++i) printInt(i); }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ForStmt(
                VarDecl(IntType(), 'i', IntLiteral(0)),
                BinaryOp(Identifier('i'), '<', IntLiteral(10)),
                PrefixOp('++', Identifier('i')),
                ExprStmt(FuncCall('printInt', [Identifier('i')]))
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_038():
    """For loop with all parts omitted (infinite loop with break)."""
    source = "void foo() { for (;;) { break; } }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ForStmt(
                None,
                None,
                None,
                BlockStmt([BreakStmt()])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_039():
    """For loop with auto init and postfix update."""
    source = "void foo() { for (auto i = 0; i < 5; i++) { printInt(i); } }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ForStmt(
                VarDecl(None, 'i', IntLiteral(0)),
                BinaryOp(Identifier('i'), '<', IntLiteral(5)),
                PostfixOp('++', Identifier('i')),
                BlockStmt([ExprStmt(FuncCall('printInt', [Identifier('i')]))])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_040():
    """Nested loops: for inside while, with break and continue."""
    source = (
        "void foo() {"
        "    int i = 0;"
        "    while (i < 3) {"
        "        for (int j = 0; j < 3; ++j) {"
        "            if (j == 1) continue;"
        "            printInt(j);"
        "        }"
        "        i++;"
        "    }"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'i', IntLiteral(0)),
            WhileStmt(
                BinaryOp(Identifier('i'), '<', IntLiteral(3)),
                BlockStmt([
                    ForStmt(
                        VarDecl(IntType(), 'j', IntLiteral(0)),
                        BinaryOp(Identifier('j'), '<', IntLiteral(3)),
                        PrefixOp('++', Identifier('j')),
                        BlockStmt([
                            IfStmt(
                                BinaryOp(Identifier('j'), '==', IntLiteral(1)),
                                ContinueStmt()
                            ),
                            ExprStmt(FuncCall('printInt', [Identifier('j')])),
                        ])
                    ),
                    ExprStmt(PostfixOp('++', Identifier('i'))),
                ])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_041():
    """Switch with two cases and a default."""
    source = (
        "void foo() {"
        "    int x = 2;"
        "    switch (x) {"
        "        case 1: printInt(1); break;"
        "        case 2: printInt(2); break;"
        "        default: printInt(0);"
        "    }"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(2)),
            SwitchStmt(
                Identifier('x'),
                [
                    CaseStmt(IntLiteral(1), [
                        ExprStmt(FuncCall('printInt', [IntLiteral(1)])),
                        BreakStmt(),
                    ]),
                    CaseStmt(IntLiteral(2), [
                        ExprStmt(FuncCall('printInt', [IntLiteral(2)])),
                        BreakStmt(),
                    ]),
                ],
                DefaultStmt([ExprStmt(FuncCall('printInt', [IntLiteral(0)]))])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_042():
    """Switch with empty body."""
    source = "void foo() { int x = 1; switch (x) {} }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(1)),
            SwitchStmt(Identifier('x'), [], None)
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_043():
    """Switch fall-through: two consecutive case labels with shared body."""
    source = (
        "void foo() {"
        "    int d = 2;"
        "    switch (d) {"
        "        case 1:"
        "        case 2: printInt(12); break;"
        "        default: printInt(0);"
        "    }"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'd', IntLiteral(2)),
            SwitchStmt(
                Identifier('d'),
                [
                    CaseStmt(IntLiteral(1), []),
                    CaseStmt(IntLiteral(2), [
                        ExprStmt(FuncCall('printInt', [IntLiteral(12)])),
                        BreakStmt(),
                    ]),
                ],
                DefaultStmt([ExprStmt(FuncCall('printInt', [IntLiteral(0)]))])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_044():
    """Switch with negative literal case and unary-plus case."""
    source = (
        "void foo() {"
        "    int x = -1;"
        "    switch (x) {"
        "        case -1: printInt(-1); break;"
        "        case +2: printInt(2); break;"
        "    }"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x', PrefixOp('-', IntLiteral(1))),
            SwitchStmt(
                Identifier('x'),
                [
                    CaseStmt(PrefixOp('-', IntLiteral(1)), [
                        ExprStmt(FuncCall('printInt', [PrefixOp('-', IntLiteral(1))])),
                        BreakStmt(),
                    ]),
                    CaseStmt(PrefixOp('+', IntLiteral(2)), [
                        ExprStmt(FuncCall('printInt', [IntLiteral(2)])),
                        BreakStmt(),
                    ]),
                ],
                None
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_045():
    """Built-in read calls used in non-trivial expressions: arithmetic and relational."""
    source = "void foo() { auto sum = readInt() + readInt(); auto ok = readFloat() > 0.0; auto msg = readString(); printString(msg); printInt(sum); }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'sum',
                BinaryOp(FuncCall('readInt', []), '+', FuncCall('readInt', []))),
            VarDecl(None, 'ok',
                BinaryOp(FuncCall('readFloat', []), '>', FloatLiteral(0.0))),
            VarDecl(None, 'msg', FuncCall('readString', [])),
            ExprStmt(FuncCall('printString', [Identifier('msg')])),
            ExprStmt(FuncCall('printInt', [Identifier('sum')])),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_046():
    """User-defined function call with multiple arguments."""
    source = "int add(int a, int b) { return a + b; } void main() { auto r = add(3, 4); }"
    expected = Program([
        FuncDecl(IntType(), 'add', [
            Param(IntType(), 'a'),
            Param(IntType(), 'b'),
        ], BlockStmt([
            ReturnStmt(BinaryOp(Identifier('a'), '+', Identifier('b')))
        ])),
        FuncDecl(VoidType(), 'main', [], BlockStmt([
            VarDecl(None, 'r', FuncCall('add', [IntLiteral(3), IntLiteral(4)])),
        ])),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_047():
    """Member access in binary expressions: midpoint and comparison."""
    source = "void foo() { auto mid = (a.x + b.x) / 2; auto eq = a.y == b.y; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'mid',
                BinaryOp(
                    BinaryOp(MemberAccess(Identifier('a'), 'x'), '+', MemberAccess(Identifier('b'), 'x')),
                    '/',
                    IntLiteral(2)
                )),
            VarDecl(None, 'eq',
                BinaryOp(MemberAccess(Identifier('a'), 'y'), '==', MemberAccess(Identifier('b'), 'y'))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_048():
    """Member writes: assign computed expressions involving own and other members."""
    source = "void foo() { p.x = p.x * 2 + 1; p.y = p.x - p.y; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ExprStmt(AssignExpr(
                MemberAccess(Identifier('p'), 'x'),
                BinaryOp(
                    BinaryOp(MemberAccess(Identifier('p'), 'x'), '*', IntLiteral(2)),
                    '+',
                    IntLiteral(1)
                )
            )),
            ExprStmt(AssignExpr(
                MemberAccess(Identifier('p'), 'y'),
                BinaryOp(MemberAccess(Identifier('p'), 'x'), '-', MemberAccess(Identifier('p'), 'y'))
            )),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_049():
    """Chained member access (nested struct)."""
    source = "void foo() { auto v = a.b.c; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'v',
                MemberAccess(MemberAccess(Identifier('a'), 'b'), 'c')),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_050():
    """Member access on function call result."""
    source = "void foo() { auto v = getPoint().x; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'v',
                MemberAccess(FuncCall('getPoint', []), 'x')),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_051():
    """Struct literal as function argument."""
    source = "void foo() { bar({1, 2}); }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ExprStmt(FuncCall('bar', [StructLiteral([IntLiteral(1), IntLiteral(2)])]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_052():
    """Assignment used as expression inside a larger expression."""
    source = "void foo() { int x; int y = (x = 5) + 7; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x'),
            VarDecl(IntType(), 'y',
                BinaryOp(AssignExpr(Identifier('x'), IntLiteral(5)), '+', IntLiteral(7))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_053():
    """Postfix ++ on a struct member."""
    source = "void foo() { p.x++; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ExprStmt(PostfixOp('++', MemberAccess(Identifier('p'), 'x')))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_054():
    """Prefix -- on a struct member."""
    source = "void foo() { --p.x; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ExprStmt(PrefixOp('--', MemberAccess(Identifier('p'), 'x')))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_055():
    """Complex expression: arithmetic on member accesses."""
    source = "void foo() { auto dist = p.x * p.x + p.y * p.y; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'dist',
                BinaryOp(
                    BinaryOp(
                        MemberAccess(Identifier('p'), 'x'),
                        '*',
                        MemberAccess(Identifier('p'), 'x')
                    ),
                    '+',
                    BinaryOp(
                        MemberAccess(Identifier('p'), 'y'),
                        '*',
                        MemberAccess(Identifier('p'), 'y')
                    )
                ))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_056():
    """Function call result used directly in arithmetic."""
    source = "void foo() { auto r = add(1, 2) + add(3, 4); }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'r',
                BinaryOp(
                    FuncCall('add', [IntLiteral(1), IntLiteral(2)]),
                    '+',
                    FuncCall('add', [IntLiteral(3), IntLiteral(4)])
                ))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_057():
    """Switch inside a for loop."""
    source = (
        "void foo() {"
        "    for (int i = 0; i < 3; i++) {"
        "        switch (i) {"
        "            case 0: printInt(0); break;"
        "            case 1: printInt(1); break;"
        "            default: printInt(2);"
        "        }"
        "    }"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ForStmt(
                VarDecl(IntType(), 'i', IntLiteral(0)),
                BinaryOp(Identifier('i'), '<', IntLiteral(3)),
                PostfixOp('++', Identifier('i')),
                BlockStmt([
                    SwitchStmt(
                        Identifier('i'),
                        [
                            CaseStmt(IntLiteral(0), [
                                ExprStmt(FuncCall('printInt', [IntLiteral(0)])),
                                BreakStmt(),
                            ]),
                            CaseStmt(IntLiteral(1), [
                                ExprStmt(FuncCall('printInt', [IntLiteral(1)])),
                                BreakStmt(),
                            ]),
                        ],
                        DefaultStmt([ExprStmt(FuncCall('printInt', [IntLiteral(2)]))])
                    )
                ])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_058():
    """Chained assignment to member then use in expression."""
    source = "void foo() { p.x = p.y = 0; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ExprStmt(AssignExpr(
                MemberAccess(Identifier('p'), 'x'),
                AssignExpr(MemberAccess(Identifier('p'), 'y'), IntLiteral(0))
            ))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_059():
    """Struct literal with nested struct literal."""
    source = "void foo() { Vec3 v = {{1, 2}, 3}; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(StructType('Vec3'), 'v',
                StructLiteral([
                    StructLiteral([IntLiteral(1), IntLiteral(2)]),
                    IntLiteral(3),
                ]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_060():
    """Complex: struct member access + arithmetic + function call + if/else."""
    source = (
        "void foo() {"
        "    auto sum = p.x + p.y;"
        "    if (sum > 0) {"
        "        printInt(sum);"
        "    } else {"
        "        printInt(0 - sum);"
        "    }"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'sum',
                BinaryOp(
                    MemberAccess(Identifier('p'), 'x'),
                    '+',
                    MemberAccess(Identifier('p'), 'y')
                )),
            IfStmt(
                BinaryOp(Identifier('sum'), '>', IntLiteral(0)),
                BlockStmt([ExprStmt(FuncCall('printInt', [Identifier('sum')]))]),
                BlockStmt([ExprStmt(FuncCall('printInt', [
                    BinaryOp(IntLiteral(0), '-', Identifier('sum'))
                ]))])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_061():
    """Float literals: various valid forms."""
    source = "void foo() { auto a = 0.0; auto b = 1.; auto c = .5; auto d = 1e4; auto e = 2E-3; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'a', FloatLiteral(0.0)),
            VarDecl(None, 'b', FloatLiteral(1.0)),
            VarDecl(None, 'c', FloatLiteral(0.5)),
            VarDecl(None, 'd', FloatLiteral(1e4)),
            VarDecl(None, 'e', FloatLiteral(2e-3)),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_062():
    """Float arithmetic: mixed int/float operands."""
    source = "void foo() { auto x = 1 + 2.5; auto y = 3.0 * 2; auto z = 10.0 / 4; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'x', BinaryOp(IntLiteral(1), '+', FloatLiteral(2.5))),
            VarDecl(None, 'y', BinaryOp(FloatLiteral(3.0), '*', IntLiteral(2))),
            VarDecl(None, 'z', BinaryOp(FloatLiteral(10.0), '/', IntLiteral(4))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_063():
    """String literals with escape sequences."""
    # r'(content)' for raw string to avoid Python interpreting the escapes
    source = r'void foo() { auto a = "hello\n"; auto b = "say \"hi\""; auto c = "a\\b"; }'
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'a', StringLiteral('hello\\n')),
            VarDecl(None, 'b', StringLiteral('say \\"hi\\"')),
            VarDecl(None, 'c', StringLiteral('a\\\\b')),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_064():
    """String literal with escape sequences stored and printed."""
    source = r'void foo() { auto s = "hello\nworld\t!"; printString(s); }'
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 's', StringLiteral('hello\\nworld\\t!')),
            ExprStmt(FuncCall('printString', [Identifier('s')])),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_065():
    """Recursive function shape: fib(n) with two return paths."""
    source = (
        "int fib(int n) {"
        "    if (n <= 1) return n;"
        "    return fib(n - 1) + fib(n - 2);"
        "}"
    )
    expected = Program([
        FuncDecl(IntType(), 'fib', [Param(IntType(), 'n')], BlockStmt([
            IfStmt(
                BinaryOp(Identifier('n'), '<=', IntLiteral(1)),
                ReturnStmt(Identifier('n'))
            ),
            ReturnStmt(
                BinaryOp(
                    FuncCall('fib', [BinaryOp(Identifier('n'), '-', IntLiteral(1))]),
                    '+',
                    FuncCall('fib', [BinaryOp(Identifier('n'), '-', IntLiteral(2))])
                )
            ),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_066():
    """Multiple functions calling each other."""
    source = (
        "int square(int x) { return x * x; }"
        "int sumSquares(int a, int b) { return square(a) + square(b); }"
    )
    expected = Program([
        FuncDecl(IntType(), 'square', [Param(IntType(), 'x')], BlockStmt([
            ReturnStmt(BinaryOp(Identifier('x'), '*', Identifier('x')))
        ])),
        FuncDecl(IntType(), 'sumSquares', [
            Param(IntType(), 'a'),
            Param(IntType(), 'b'),
        ], BlockStmt([
            ReturnStmt(BinaryOp(
                FuncCall('square', [Identifier('a')]),
                '+',
                FuncCall('square', [Identifier('b')])
            ))
        ])),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_067():
    """For loop with assignment (not declaration) as init."""
    source = "void foo() { int i; for (i = 0; i < 5; i++) printInt(i); }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'i'),
            ForStmt(
                ExprStmt(AssignExpr(Identifier('i'), IntLiteral(0))),
                BinaryOp(Identifier('i'), '<', IntLiteral(5)),
                PostfixOp('++', Identifier('i')),
                ExprStmt(FuncCall('printInt', [Identifier('i')]))
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_068():
    """For loop with member-assignment as update expression."""
    source = "void foo() { for (int i = 0; i < 3; p.x = p.x + 1) i++; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ForStmt(
                VarDecl(IntType(), 'i', IntLiteral(0)),
                BinaryOp(Identifier('i'), '<', IntLiteral(3)),
                AssignExpr(
                    MemberAccess(Identifier('p'), 'x'),
                    BinaryOp(MemberAccess(Identifier('p'), 'x'), '+', IntLiteral(1))
                ),
                ExprStmt(PostfixOp('++', Identifier('i')))
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_069():
    """Switch with constant-expression case (addition)."""
    source = (
        "void foo() {"
        "    int x = 3;"
        "    switch (x) {"
        "        case 1 + 2: printInt(3); break;"
        "        default: printInt(0);"
        "    }"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(3)),
            SwitchStmt(
                Identifier('x'),
                [
                    CaseStmt(BinaryOp(IntLiteral(1), '+', IntLiteral(2)), [
                        ExprStmt(FuncCall('printInt', [IntLiteral(3)])),
                        BreakStmt(),
                    ]),
                ],
                DefaultStmt([ExprStmt(FuncCall('printInt', [IntLiteral(0)]))])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_070():
    """Deeply nested arithmetic expression."""
    source = "void foo() { auto x = (1 + 2) * (3 - 4) / (5 % 3); }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'x',
                BinaryOp(
                    BinaryOp(
                        BinaryOp(IntLiteral(1), '+', IntLiteral(2)),
                        '*',
                        BinaryOp(IntLiteral(3), '-', IntLiteral(4))
                    ),
                    '/',
                    BinaryOp(IntLiteral(5), '%', IntLiteral(3))
                ))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_071():
    """Three-level deep struct nesting."""
    source = (
        "struct A { int v; };"
        "struct B { A a; };"
        "struct C { B b; };"
        "void foo() { auto x = c.b.a.v; }"
    )
    expected = Program([
        StructDecl('A', [MemberDecl(IntType(), 'v')]),
        StructDecl('B', [MemberDecl(StructType('A'), 'a')]),
        StructDecl('C', [MemberDecl(StructType('B'), 'b')]),
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'x',
                MemberAccess(
                    MemberAccess(
                        MemberAccess(Identifier('c'), 'b'),
                        'a'),
                    'v'))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_072():
    """Assign to three-level nested member."""
    source = "void foo() { c.b.a.v = 99; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ExprStmt(AssignExpr(
                MemberAccess(
                    MemberAccess(
                        MemberAccess(Identifier('c'), 'b'),
                        'a'),
                    'v'),
                IntLiteral(99)
            ))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_073():
    """Unary minus on a float literal."""
    source = "void foo() { auto x = -3.14; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'x', PrefixOp('-', FloatLiteral(3.14))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_074():
    """Prefix decrement on a literal, and double NOT."""
    source = "void foo() { auto a = --5; auto b = !!0; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'a', PrefixOp('--', IntLiteral(5))),
            VarDecl(None, 'b', PrefixOp('!', PrefixOp('!', IntLiteral(0)))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_075():
    """Function with multiple return statements on different paths."""
    source = (
        "int abs(int n) {"
        "    if (n < 0) return 0 - n;"
        "    return n;"
        "}"
    )
    expected = Program([
        FuncDecl(IntType(), 'abs', [Param(IntType(), 'n')], BlockStmt([
            IfStmt(
                BinaryOp(Identifier('n'), '<', IntLiteral(0)),
                ReturnStmt(BinaryOp(IntLiteral(0), '-', Identifier('n')))
            ),
            ReturnStmt(Identifier('n')),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_076():
    """printFloat and printString calls with expressions."""
    source = 'void foo() { printFloat(3.14); printString("done"); }'
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ExprStmt(FuncCall('printFloat', [FloatLiteral(3.14)])),
            ExprStmt(FuncCall('printString', [StringLiteral('done')])),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_077():
    """Struct copy via assignment."""
    source = (
        "struct Point { int x; int y; };"
        "void foo() { Point p1 = {1, 2}; Point p2; p2 = p1; }"
    )
    expected = Program([
        StructDecl('Point', [
            MemberDecl(IntType(), 'x'),
            MemberDecl(IntType(), 'y'),
        ]),
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(StructType('Point'), 'p1',
                    StructLiteral([IntLiteral(1), IntLiteral(2)])),
            VarDecl(StructType('Point'), 'p2'),
            ExprStmt(AssignExpr(Identifier('p2'), Identifier('p1'))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_078():
    """Complex while loop: accumulator pattern with multiple statements."""
    source = (
        "int sumTo(int n) {"
        "    int acc = 0;"
        "    int i = 1;"
        "    while (i <= n) {"
        "        acc = acc + i;"
        "        i++;"
        "    }"
        "    return acc;"
        "}"
    )
    expected = Program([
        FuncDecl(IntType(), 'sumTo', [Param(IntType(), 'n')], BlockStmt([
            VarDecl(IntType(), 'acc', IntLiteral(0)),
            VarDecl(IntType(), 'i', IntLiteral(1)),
            WhileStmt(
                BinaryOp(Identifier('i'), '<=', Identifier('n')),
                BlockStmt([
                    ExprStmt(AssignExpr(
                        Identifier('acc'),
                        BinaryOp(Identifier('acc'), '+', Identifier('i'))
                    )),
                    ExprStmt(PostfixOp('++', Identifier('i'))),
                ])
            ),
            ReturnStmt(Identifier('acc')),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_079():
    """Inferred-return function that returns a function-call result."""
    source = (
        "int double(int x) { return x * 2; }"
        "quadruple(int x) { return double(double(x)); }"
    )
    expected = Program([
        FuncDecl(IntType(), 'double', [Param(IntType(), 'x')], BlockStmt([
            ReturnStmt(BinaryOp(Identifier('x'), '*', IntLiteral(2)))
        ])),
        FuncDecl(None, 'quadruple', [Param(IntType(), 'x')], BlockStmt([
            ReturnStmt(FuncCall('double', [FuncCall('double', [Identifier('x')])]))
        ])),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_080():
    """Full program: structs, multiple functions, loops, switch, member access."""
    source = (
        "struct Point { int x; int y; };"
        "int manhattanDist(Point a, Point b) {"
        "    int dx = a.x - b.x;"
        "    int dy = a.y - b.y;"
        "    if (dx < 0) dx = 0 - dx;"
        "    if (dy < 0) dy = 0 - dy;"
        "    return dx + dy;"
        "}"
        "void main() {"
        "    Point p1 = {1, 2};"
        "    Point p2 = {4, 6};"
        "    auto d = manhattanDist(p1, p2);"
        "    switch (d) {"
        "        case 7: printInt(1); break;"
        "        default: printInt(0);"
        "    }"
        "}"
    )
    expected = Program([
        StructDecl('Point', [
            MemberDecl(IntType(), 'x'),
            MemberDecl(IntType(), 'y'),
        ]),
        FuncDecl(IntType(), 'manhattanDist', [
            Param(StructType('Point'), 'a'),
            Param(StructType('Point'), 'b'),
        ], BlockStmt([
            VarDecl(IntType(), 'dx',
                BinaryOp(MemberAccess(Identifier('a'), 'x'),
                         '-', MemberAccess(Identifier('b'), 'x'))),
            VarDecl(IntType(), 'dy',
                BinaryOp(MemberAccess(Identifier('a'), 'y'),
                         '-', MemberAccess(Identifier('b'), 'y'))),
            IfStmt(
                BinaryOp(Identifier('dx'), '<', IntLiteral(0)),
                ExprStmt(AssignExpr(Identifier('dx'),
                    BinaryOp(IntLiteral(0), '-', Identifier('dx'))))
            ),
            IfStmt(
                BinaryOp(Identifier('dy'), '<', IntLiteral(0)),
                ExprStmt(AssignExpr(Identifier('dy'),
                    BinaryOp(IntLiteral(0), '-', Identifier('dy'))))
            ),
            ReturnStmt(BinaryOp(Identifier('dx'), '+', Identifier('dy'))),
        ])),
        FuncDecl(VoidType(), 'main', [], BlockStmt([
            VarDecl(StructType('Point'), 'p1',
                    StructLiteral([IntLiteral(1), IntLiteral(2)])),
            VarDecl(StructType('Point'), 'p2',
                    StructLiteral([IntLiteral(4), IntLiteral(6)])),
            VarDecl(None, 'd',
                FuncCall('manhattanDist', [Identifier('p1'), Identifier('p2')])),
            SwitchStmt(
                Identifier('d'),
                [
                    CaseStmt(IntLiteral(7), [
                        ExprStmt(FuncCall('printInt', [IntLiteral(1)])),
                        BreakStmt(),
                    ]),
                ],
                DefaultStmt([ExprStmt(FuncCall('printInt', [IntLiteral(0)]))])
            ),
        ])),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_081():
    """Equality and inequality operators on floats."""
    source = "void foo() { auto a = 1.0 == 1.0; auto b = 3.14 != 2.71; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'a', BinaryOp(FloatLiteral(1.0), '==', FloatLiteral(1.0))),
            VarDecl(None, 'b', BinaryOp(FloatLiteral(3.14), '!=', FloatLiteral(2.71))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_082():
    """Relational operators on floats."""
    source = "void foo() { auto a = 1.5 < 2.5; auto b = 3.0 >= 3.0; auto c = 0.1 <= 0.2; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'a', BinaryOp(FloatLiteral(1.5), '<', FloatLiteral(2.5))),
            VarDecl(None, 'b', BinaryOp(FloatLiteral(3.0), '>=', FloatLiteral(3.0))),
            VarDecl(None, 'c', BinaryOp(FloatLiteral(0.1), '<=', FloatLiteral(0.2))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_083():
    """All six relational operators in one function."""
    source = "void foo() { auto a=1<2; auto b=1<=2; auto c=2>1; auto d=2>=1; auto e=1==1; auto f=1!=2; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'a', BinaryOp(IntLiteral(1), '<',  IntLiteral(2))),
            VarDecl(None, 'b', BinaryOp(IntLiteral(1), '<=', IntLiteral(2))),
            VarDecl(None, 'c', BinaryOp(IntLiteral(2), '>',  IntLiteral(1))),
            VarDecl(None, 'd', BinaryOp(IntLiteral(2), '>=', IntLiteral(1))),
            VarDecl(None, 'e', BinaryOp(IntLiteral(1), '==', IntLiteral(1))),
            VarDecl(None, 'f', BinaryOp(IntLiteral(1), '!=', IntLiteral(2))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_084():
    """switch with default placed after cases."""
    source = (
        "void foo() {"
        "    int x = 5;"
        "    switch (x) {"
        "        case 1: printInt(1); break;"
        "        case 2: printInt(2); break;"
        "        default: printInt(0); break;"
        "    }"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(5)),
            SwitchStmt(
                Identifier('x'),
                [
                    CaseStmt(IntLiteral(1), [
                        ExprStmt(FuncCall('printInt', [IntLiteral(1)])),
                        BreakStmt(),
                    ]),
                    CaseStmt(IntLiteral(2), [
                        ExprStmt(FuncCall('printInt', [IntLiteral(2)])),
                        BreakStmt(),
                    ]),
                ],
                DefaultStmt([
                    ExprStmt(FuncCall('printInt', [IntLiteral(0)])),
                    BreakStmt(),
                ])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_085():
    """Nested if-else chain (else-if ladder)."""
    source = (
        "void classify(int n) {"
        "    if (n < 0) printInt(-1);"
        "    else if (n == 0) printInt(0);"
        "    else printInt(1);"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'classify', [Param(IntType(), 'n')], BlockStmt([
            IfStmt(
                BinaryOp(Identifier('n'), '<', IntLiteral(0)),
                ExprStmt(FuncCall('printInt', [PrefixOp('-', IntLiteral(1))])),
                IfStmt(
                    BinaryOp(Identifier('n'), '==', IntLiteral(0)),
                    ExprStmt(FuncCall('printInt', [IntLiteral(0)])),
                    ExprStmt(FuncCall('printInt', [IntLiteral(1)]))
                )
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_086():
    """Deeply nested if inside while inside for."""
    source = (
        "void foo() {"
        "    for (int i = 0; i < 3; i++) {"
        "        int j = 0;"
        "        while (j < 3) {"
        "            if (i == j) printInt(i);"
        "            j++;"
        "        }"
        "    }"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ForStmt(
                VarDecl(IntType(), 'i', IntLiteral(0)),
                BinaryOp(Identifier('i'), '<', IntLiteral(3)),
                PostfixOp('++', Identifier('i')),
                BlockStmt([
                    VarDecl(IntType(), 'j', IntLiteral(0)),
                    WhileStmt(
                        BinaryOp(Identifier('j'), '<', IntLiteral(3)),
                        BlockStmt([
                            IfStmt(
                                BinaryOp(Identifier('i'), '==', Identifier('j')),
                                ExprStmt(FuncCall('printInt', [Identifier('i')]))
                            ),
                            ExprStmt(PostfixOp('++', Identifier('j'))),
                        ])
                    ),
                ])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_087():
    """Complex expression tree: logical combining relational and arithmetic."""
    source = "void foo() { auto r = x + 1 > 0 && y - 1 < 10 || !z; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'r',
                BinaryOp(
                    BinaryOp(
                        BinaryOp(
                            BinaryOp(Identifier('x'), '+', IntLiteral(1)),
                            '>',
                            IntLiteral(0)
                        ),
                        '&&',
                        BinaryOp(
                            BinaryOp(Identifier('y'), '-', IntLiteral(1)),
                            '<',
                            IntLiteral(10)
                        )
                    ),
                    '||',
                    PrefixOp('!', Identifier('z'))
                ))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_088():
    """Precedence: postfix ++ has higher precedence than unary -."""
    source = "void foo() { int x = 5; auto a = -x++; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(5)),
            VarDecl(None, 'a', PrefixOp('-', PostfixOp('++', Identifier('x')))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_089():
    """Precedence: member access has highest precedence over prefix op."""
    source = "void foo() { auto a = -p.x; }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'a', PrefixOp('-', MemberAccess(Identifier('p'), 'x'))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_090():
    """Struct with five members; init with all five values."""
    source = (
        "struct Big { int a; float b; string c; int d; float e; };"
        "void foo() { Big v = {1, 2.0, \"x\", 3, 4.0}; }"
    )
    expected = Program([
        StructDecl('Big', [
            MemberDecl(IntType(), 'a'),
            MemberDecl(FloatType(), 'b'),
            MemberDecl(StringType(), 'c'),
            MemberDecl(IntType(), 'd'),
            MemberDecl(FloatType(), 'e'),
        ]),
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(StructType('Big'), 'v',
                StructLiteral([
                    IntLiteral(1),
                    FloatLiteral(2.0),
                    StringLiteral('x'),
                    IntLiteral(3),
                    FloatLiteral(4.0),
                ]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_091():
    """Auto var inferred from chained function calls."""
    source = "void foo() { auto r = add(mul(2, 3), mul(4, 5)); }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'r',
                FuncCall('add', [
                    FuncCall('mul', [IntLiteral(2), IntLiteral(3)]),
                    FuncCall('mul', [IntLiteral(4), IntLiteral(5)]),
                ]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_092():
    """for loop with only condition (no init, no update)."""
    source = "void foo() { int i = 0; for (; i < 10;) { i = i + 1; } }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'i', IntLiteral(0)),
            ForStmt(
                None,
                BinaryOp(Identifier('i'), '<', IntLiteral(10)),
                None,
                BlockStmt([
                    ExprStmt(AssignExpr(
                        Identifier('i'),
                        BinaryOp(Identifier('i'), '+', IntLiteral(1))
                    ))
                ])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_093():
    """switch with only a default clause."""
    source = "void foo() { int x = 9; switch (x) { default: printInt(x); } }"
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(9)),
            SwitchStmt(
                Identifier('x'),
                [],
                DefaultStmt([ExprStmt(FuncCall('printInt', [Identifier('x')]))])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_094():
    """Inferred-return void function (no return statement)."""
    source = "greet(string name) { printString(name); }"
    expected = Program([
        FuncDecl(None, 'greet', [Param(StringType(), 'name')], BlockStmt([
            ExprStmt(FuncCall('printString', [Identifier('name')]))
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_095():
    """Block statement used as then/else body with local variable shadowing."""
    source = (
        "void foo() {"
        "    int x = 1;"
        "    if (x) {"
        "        int x = 2;"
        "        printInt(x);"
        "    } else {"
        "        int x = 3;"
        "        printInt(x);"
        "    }"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(1)),
            IfStmt(
                Identifier('x'),
                BlockStmt([
                    VarDecl(IntType(), 'x', IntLiteral(2)),
                    ExprStmt(FuncCall('printInt', [Identifier('x')])),
                ]),
                BlockStmt([
                    VarDecl(IntType(), 'x', IntLiteral(3)),
                    ExprStmt(FuncCall('printInt', [Identifier('x')])),
                ])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_096():
    """Multiple auto vars inferred from expressions of different types."""
    source = (
        "void foo() {"
        "    auto a = 1 + 2;"
        "    auto b = 1.0 + 2.0;"
        "    auto c = a < 5;"
        "    auto d = b > 0.0;"
        "    auto e = c && d;"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'a', BinaryOp(IntLiteral(1),   '+',  IntLiteral(2))),
            VarDecl(None, 'b', BinaryOp(FloatLiteral(1.0), '+', FloatLiteral(2.0))),
            VarDecl(None, 'c', BinaryOp(Identifier('a'), '<',  IntLiteral(5))),
            VarDecl(None, 'd', BinaryOp(Identifier('b'), '>',  FloatLiteral(0.0))),
            VarDecl(None, 'e', BinaryOp(Identifier('c'), '&&', Identifier('d'))),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_097():
    """Four-level deep struct chain: read and write."""
    source = (
        "struct D { int v; };"
        "struct C { D d; };"
        "struct B { C c; };"
        "struct A { B b; };"
        "void foo() {"
        "    auto x = root.b.c.d.v;"
        "    root.b.c.d.v = 42;"
        "}"
    )
    expected = Program([
        StructDecl('D', [MemberDecl(IntType(), 'v')]),
        StructDecl('C', [MemberDecl(StructType('D'), 'd')]),
        StructDecl('B', [MemberDecl(StructType('C'), 'c')]),
        StructDecl('A', [MemberDecl(StructType('B'), 'b')]),
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'x',
                MemberAccess(
                    MemberAccess(
                        MemberAccess(
                            MemberAccess(Identifier('root'), 'b'),
                            'c'),
                        'd'),
                    'v')),
            ExprStmt(AssignExpr(
                MemberAccess(
                    MemberAccess(
                        MemberAccess(
                            MemberAccess(Identifier('root'), 'b'),
                            'c'),
                        'd'),
                    'v'),
                IntLiteral(42)
            )),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_098():
    """switch with many cases and complex expressions in case bodies."""
    source = (
        "void process(int op, int a, int b) {"
        "    switch (op) {"
        "        case 1: printInt(a + b); break;"
        "        case 2: printInt(a - b); break;"
        "        case 3: printInt(a * b); break;"
        "        case 4: printInt(a / b); break;"
        "        case 5: printInt(a % b); break;"
        "        default: printInt(0);"
        "    }"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'process', [
            Param(IntType(), 'op'),
            Param(IntType(), 'a'),
            Param(IntType(), 'b'),
        ], BlockStmt([
            SwitchStmt(
                Identifier('op'),
                [
                    CaseStmt(IntLiteral(1), [
                        ExprStmt(FuncCall('printInt', [BinaryOp(Identifier('a'), '+', Identifier('b'))])),
                        BreakStmt(),
                    ]),
                    CaseStmt(IntLiteral(2), [
                        ExprStmt(FuncCall('printInt', [BinaryOp(Identifier('a'), '-', Identifier('b'))])),
                        BreakStmt(),
                    ]),
                    CaseStmt(IntLiteral(3), [
                        ExprStmt(FuncCall('printInt', [BinaryOp(Identifier('a'), '*', Identifier('b'))])),
                        BreakStmt(),
                    ]),
                    CaseStmt(IntLiteral(4), [
                        ExprStmt(FuncCall('printInt', [BinaryOp(Identifier('a'), '/', Identifier('b'))])),
                        BreakStmt(),
                    ]),
                    CaseStmt(IntLiteral(5), [
                        ExprStmt(FuncCall('printInt', [BinaryOp(Identifier('a'), '%', Identifier('b'))])),
                        BreakStmt(),
                    ]),
                ],
                DefaultStmt([ExprStmt(FuncCall('printInt', [IntLiteral(0)]))])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_099():
    """Interleaved structs and functions at top level; cross-function struct usage."""
    source = (
        "struct Vec2 { float x; float y; };"
        "Vec2 makeVec(float x, float y) { Vec2 v = {x, y}; return v; }"
        "struct Segment { Vec2 start; Vec2 end; };"
        "float segLen(Segment s) {"
        "    auto dx = s.end.x - s.start.x;"
        "    auto dy = s.end.y - s.start.y;"
        "    return dx * dx + dy * dy;"
        "}"
    )
    expected = Program([
        StructDecl('Vec2', [
            MemberDecl(FloatType(), 'x'),
            MemberDecl(FloatType(), 'y'),
        ]),
        FuncDecl(StructType('Vec2'), 'makeVec', [
            Param(FloatType(), 'x'),
            Param(FloatType(), 'y'),
        ], BlockStmt([
            VarDecl(StructType('Vec2'), 'v',
                StructLiteral([Identifier('x'), Identifier('y')])),
            ReturnStmt(Identifier('v')),
        ])),
        StructDecl('Segment', [
            MemberDecl(StructType('Vec2'), 'start'),
            MemberDecl(StructType('Vec2'), 'end'),
        ]),
        FuncDecl(FloatType(), 'segLen', [Param(StructType('Segment'), 's')], BlockStmt([
            VarDecl(None, 'dx',
                BinaryOp(
                    MemberAccess(MemberAccess(Identifier('s'), 'end'), 'x'),
                    '-',
                    MemberAccess(MemberAccess(Identifier('s'), 'start'), 'x')
                )),
            VarDecl(None, 'dy',
                BinaryOp(
                    MemberAccess(MemberAccess(Identifier('s'), 'end'), 'y'),
                    '-',
                    MemberAccess(MemberAccess(Identifier('s'), 'start'), 'y')
                )),
            ReturnStmt(
                BinaryOp(
                    BinaryOp(Identifier('dx'), '*', Identifier('dx')),
                    '+',
                    BinaryOp(Identifier('dy'), '*', Identifier('dy'))
                )
            ),
        ])),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

def test_ast_100():
    """Maximum complexity: three structs, four functions, nested loops, switch,
    member access at every level, auto and explicit vars, all statement types."""
    source = (
        "struct Color { int r; int g; int b; };"
        "struct Pixel { int x; int y; Color color; };"
        "struct Canvas { int width; int height; };"

        "Color makeColor(int r, int g, int b) {"
        "    Color c = {r, g, b};"
        "    return c;"
        "}"

        "void printPixel(Pixel px) {"
        "    printInt(px.x);"
        "    printInt(px.y);"
        "    printInt(px.color.r);"
        "    printInt(px.color.g);"
        "    printInt(px.color.b);"
        "}"

        "int clamp(int v, int lo, int hi) {"
        "    if (v < lo) return lo;"
        "    if (v > hi) return hi;"
        "    return v;"
        "}"

        "void main() {"
        "    Canvas canvas = {8, 8};"
        "    int i = 0;"
        "    while (i < canvas.width) {"
        "        int j = 0;"
        "        for (; j < canvas.height; j++) {"
        "            auto r = clamp(i * 32, 0, 255);"
        "            auto g = clamp(j * 32, 0, 255);"
        "            auto b = 128;"
        "            Color col = {r, g, b};"
        "            switch (i) {"
        "                case 0: col.r = 255; break;"
        "                default: col.r = r;"
        "            }"
        "            Pixel px = {i, j, col};"
        "            printPixel(px);"
        "        }"
        "        i++;"
        "    }"
        "}"
    )
    expected = Program([
        StructDecl('Color', [
            MemberDecl(IntType(), 'r'),
            MemberDecl(IntType(), 'g'),
            MemberDecl(IntType(), 'b'),
        ]),
        StructDecl('Pixel', [
            MemberDecl(IntType(), 'x'),
            MemberDecl(IntType(), 'y'),
            MemberDecl(StructType('Color'), 'color'),
        ]),
        StructDecl('Canvas', [
            MemberDecl(IntType(), 'width'),
            MemberDecl(IntType(), 'height'),
        ]),
        FuncDecl(StructType('Color'), 'makeColor', [
            Param(IntType(), 'r'),
            Param(IntType(), 'g'),
            Param(IntType(), 'b'),
        ], BlockStmt([
            VarDecl(StructType('Color'), 'c',
                StructLiteral([Identifier('r'), Identifier('g'), Identifier('b')])),
            ReturnStmt(Identifier('c')),
        ])),
        FuncDecl(VoidType(), 'printPixel', [Param(StructType('Pixel'), 'px')], BlockStmt([
            ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('px'), 'x')])),
            ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('px'), 'y')])),
            ExprStmt(FuncCall('printInt', [MemberAccess(MemberAccess(Identifier('px'), 'color'), 'r')])),
            ExprStmt(FuncCall('printInt', [MemberAccess(MemberAccess(Identifier('px'), 'color'), 'g')])),
            ExprStmt(FuncCall('printInt', [MemberAccess(MemberAccess(Identifier('px'), 'color'), 'b')])),
        ])),
        FuncDecl(IntType(), 'clamp', [
            Param(IntType(), 'v'),
            Param(IntType(), 'lo'),
            Param(IntType(), 'hi'),
        ], BlockStmt([
            IfStmt(
                BinaryOp(Identifier('v'), '<', Identifier('lo')),
                ReturnStmt(Identifier('lo'))
            ),
            IfStmt(
                BinaryOp(Identifier('v'), '>', Identifier('hi')),
                ReturnStmt(Identifier('hi'))
            ),
            ReturnStmt(Identifier('v')),
        ])),
        FuncDecl(VoidType(), 'main', [], BlockStmt([
            VarDecl(StructType('Canvas'), 'canvas',
                StructLiteral([IntLiteral(8), IntLiteral(8)])),
            VarDecl(IntType(), 'i', IntLiteral(0)),
            WhileStmt(
                BinaryOp(Identifier('i'), '<', MemberAccess(Identifier('canvas'), 'width')),
                BlockStmt([
                    VarDecl(IntType(), 'j', IntLiteral(0)),
                    ForStmt(
                        None,
                        BinaryOp(Identifier('j'), '<', MemberAccess(Identifier('canvas'), 'height')),
                        PostfixOp('++', Identifier('j')),
                        BlockStmt([
                            VarDecl(None, 'r',
                                FuncCall('clamp', [
                                    BinaryOp(Identifier('i'), '*', IntLiteral(32)),
                                    IntLiteral(0),
                                    IntLiteral(255),
                                ])),
                            VarDecl(None, 'g',
                                FuncCall('clamp', [
                                    BinaryOp(Identifier('j'), '*', IntLiteral(32)),
                                    IntLiteral(0),
                                    IntLiteral(255),
                                ])),
                            VarDecl(None, 'b', IntLiteral(128)),
                            VarDecl(StructType('Color'), 'col',
                                StructLiteral([Identifier('r'), Identifier('g'), Identifier('b')])),
                            SwitchStmt(
                                Identifier('i'),
                                [
                                    CaseStmt(IntLiteral(0), [
                                        ExprStmt(AssignExpr(
                                            MemberAccess(Identifier('col'), 'r'),
                                            IntLiteral(255)
                                        )),
                                        BreakStmt(),
                                    ]),
                                ],
                                DefaultStmt([
                                    ExprStmt(AssignExpr(
                                        MemberAccess(Identifier('col'), 'r'),
                                        Identifier('r')
                                    )),
                                ])
                            ),
                            VarDecl(StructType('Pixel'), 'px',
                                StructLiteral([Identifier('i'), Identifier('j'), Identifier('col')])),
                            ExprStmt(FuncCall('printPixel', [Identifier('px')])),
                        ])
                    ),
                    ExprStmt(PostfixOp('++', Identifier('i'))),
                ])
            ),
        ])),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)

# ──────────────────────────────────────────────────────────────────────────────
# Tests 101-110: Technically correct. Clinically insane.
# ──────────────────────────────────────────────────────────────────────────────

def test_ast_101():
    """for loop: postfix i++ in condition, update, AND body RHS simultaneously."""
    source = (
        "void foo() {"
        "    for (int i = 0; i++ < 10; i++) {"
        "        i = i + i++;"
        "    }"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            ForStmt(
                VarDecl(IntType(), 'i', IntLiteral(0)),
                BinaryOp(PostfixOp('++', Identifier('i')), '<', IntLiteral(10)),
                PostfixOp('++', Identifier('i')),
                BlockStmt([
                    ExprStmt(AssignExpr(
                        Identifier('i'),
                        BinaryOp(Identifier('i'), '+', PostfixOp('++', Identifier('i')))
                    )),
                ])
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_102():
    """5-level struct nesting (A.b.c.d.e.value); member access chain used in arithmetic."""
    source = (
        "struct E { int value; };"
        "struct D { E e; };"
        "struct C { D d; };"
        "struct B { C c; };"
        "struct A { B b; };"
        "void foo() {"
        "    auto r = a.b.c.d.e.value * 2 + a.b.c.d.e.value - 1;"
        "}"
    )
    five_deep = MemberAccess(
        MemberAccess(
            MemberAccess(
                MemberAccess(
                    MemberAccess(Identifier('a'), 'b'),
                    'c'),
                'd'),
            'e'),
        'value')
    expected = Program([
        StructDecl('E', [MemberDecl(IntType(), 'value')]),
        StructDecl('D', [MemberDecl(StructType('E'), 'e')]),
        StructDecl('C', [MemberDecl(StructType('D'), 'd')]),
        StructDecl('B', [MemberDecl(StructType('C'), 'c')]),
        StructDecl('A', [MemberDecl(StructType('B'), 'b')]),
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(None, 'r',
                BinaryOp(
                    BinaryOp(
                        BinaryOp(five_deep, '*', IntLiteral(2)),
                        '+',
                        MemberAccess(
                            MemberAccess(
                                MemberAccess(
                                    MemberAccess(
                                        MemberAccess(Identifier('a'), 'b'),
                                        'c'),
                                    'd'),
                                'e'),
                            'value')
                    ),
                    '-',
                    IntLiteral(1)
                )
            ),
        ])),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_103():
    """switch with 4-operand expr, 4 fall-through cases (no break), and a default."""
    source = (
        "void foo() {"
        "    int x = 3; int y = 5;"
        "    switch (x * y - x + y % x) {"
        "        case 1: printInt(1);"
        "        case 2: printInt(2);"
        "        case 3: printInt(3);"
        "        case 4: printInt(4);"
        "        default: printInt(0);"
        "    }"
        "}"
    )
    switch_expr = BinaryOp(
        BinaryOp(
            BinaryOp(Identifier('x'), '*', Identifier('y')),
            '-',
            Identifier('x')
        ),
        '+',
        BinaryOp(Identifier('y'), '%', Identifier('x'))
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(3)),
            VarDecl(IntType(), 'y', IntLiteral(5)),
            SwitchStmt(
                switch_expr,
                [
                    CaseStmt(IntLiteral(1), [ExprStmt(FuncCall('printInt', [IntLiteral(1)]))]),
                    CaseStmt(IntLiteral(2), [ExprStmt(FuncCall('printInt', [IntLiteral(2)]))]),
                    CaseStmt(IntLiteral(3), [ExprStmt(FuncCall('printInt', [IntLiteral(3)]))]),
                    CaseStmt(IntLiteral(4), [ExprStmt(FuncCall('printInt', [IntLiteral(4)]))]),
                ],
                DefaultStmt([ExprStmt(FuncCall('printInt', [IntLiteral(0)]))])
            ),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_104():
    """Postfix x++ nested as args inside add(x++, mul(x++, x++)), assigned to a member."""
    source = (
        "void foo() {"
        "    int x = 0;"
        "    p.val = add(x++, mul(x++, x++));"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(0)),
            ExprStmt(AssignExpr(
                MemberAccess(Identifier('p'), 'val'),
                FuncCall('add', [
                    PostfixOp('++', Identifier('x')),
                    FuncCall('mul', [
                        PostfixOp('++', Identifier('x')),
                        PostfixOp('++', Identifier('x')),
                    ])
                ])
            )),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_105():
    """while > for > while nesting; compound conditions throughout; innermost body is a switch on -s.val."""
    source = (
        "void foo() {"
        "    int i = 0;"
        "    while (i < 5 && i % 2 == 0 || i == 0) {"
        "        for (int j = i; j < i + 3 && j != 4; j++) {"
        "            int k = 1;"
        "            while (k < j * 2) {"
        "                switch (-s.val) {"
        "                    case 0: break;"
        "                    default: k = k + 1; break;"
        "                }"
        "            }"
        "        }"
        "        i++;"
        "    }"
        "}"
    )
    expected = Program([
        FuncDecl(VoidType(), 'foo', [], BlockStmt([
            VarDecl(IntType(), 'i', IntLiteral(0)),
            WhileStmt(
                BinaryOp(
                    BinaryOp(
                        BinaryOp(Identifier('i'), '<', IntLiteral(5)),
                        '&&',
                        BinaryOp(BinaryOp(Identifier('i'), '%', IntLiteral(2)), '==', IntLiteral(0))
                    ),
                    '||',
                    BinaryOp(Identifier('i'), '==', IntLiteral(0))
                ),
                BlockStmt([
                    ForStmt(
                        VarDecl(IntType(), 'j', Identifier('i')),
                        BinaryOp(
                            BinaryOp(Identifier('j'), '<', BinaryOp(Identifier('i'), '+', IntLiteral(3))),
                            '&&',
                            BinaryOp(Identifier('j'), '!=', IntLiteral(4))
                        ),
                        PostfixOp('++', Identifier('j')),
                        BlockStmt([
                            VarDecl(IntType(), 'k', IntLiteral(1)),
                            WhileStmt(
                                BinaryOp(Identifier('k'), '<', BinaryOp(Identifier('j'), '*', IntLiteral(2))),
                                BlockStmt([
                                    SwitchStmt(
                                        PrefixOp('-', MemberAccess(Identifier('s'), 'val')),
                                        [
                                            CaseStmt(IntLiteral(0), [BreakStmt()]),
                                        ],
                                        DefaultStmt([
                                            ExprStmt(AssignExpr(Identifier('k'),
                                                BinaryOp(Identifier('k'), '+', IntLiteral(1)))),
                                            BreakStmt(),
                                        ])
                                    ),
                                ])
                            ),
                        ])
                    ),
                    ExprStmt(PostfixOp('++', Identifier('i'))),
                ])
            ),
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_106():
    """Single return: a + b*c - d%a/b + -(a*c) - b%d + a — all 5 arithmetic ops, unary minus mid-tree."""
    source = (
        "int cursed(int a, int b, int c, int d) {"
        "    return a + b * c - d % a / b + -(a * c) - b % d + a;"
        "}"
    )
    # Precedence: * / % bind first, then + - left-to-right; unary - tightest.
    # a + (b*c) - ((d%a)/b) + (-(a*c)) - (b%d) + a
    expected = Program([
        FuncDecl(IntType(), 'cursed', [
            Param(IntType(), 'a'),
            Param(IntType(), 'b'),
            Param(IntType(), 'c'),
            Param(IntType(), 'd'),
        ], BlockStmt([
            ReturnStmt(
                BinaryOp(
                    BinaryOp(
                        BinaryOp(
                            BinaryOp(
                                BinaryOp(
                                    Identifier('a'),
                                    '+',
                                    BinaryOp(Identifier('b'), '*', Identifier('c'))
                                ),
                                '-',
                                BinaryOp(
                                    BinaryOp(Identifier('d'), '%', Identifier('a')),
                                    '/',
                                    Identifier('b')
                                )
                            ),
                            '+',
                            PrefixOp('-', BinaryOp(Identifier('a'), '*', Identifier('c')))
                        ),
                        '-',
                        BinaryOp(Identifier('b'), '%', Identifier('d'))
                    ),
                    '+',
                    Identifier('a')
                )
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_107():
    """if/else on compound member-access condition; then assigns computed member expr; else has a switch."""
    source = (
        "struct Node { int val; int left; int right; int depth; };"
        "void process(Node n) {"
        "    if (n.depth % 2 == 0 && n.val > n.left + n.right) {"
        "        n.val = n.left * n.depth - n.right % n.depth + 1;"
        "    } else {"
        "        switch (n.val % 3) {"
        "            case 0: n.left = n.left + 1; break;"
        "            case 1: n.right = n.right - 1; break;"
        "            default: n.depth = n.depth * 2; break;"
        "        }"
        "    }"
        "}"
    )
    expected = Program([
        StructDecl('Node', [
            MemberDecl(IntType(), 'val'),
            MemberDecl(IntType(), 'left'),
            MemberDecl(IntType(), 'right'),
            MemberDecl(IntType(), 'depth'),
        ]),
        FuncDecl(VoidType(), 'process', [Param(StructType('Node'), 'n')], BlockStmt([
            IfStmt(
                BinaryOp(
                    BinaryOp(
                        BinaryOp(MemberAccess(Identifier('n'), 'depth'), '%', IntLiteral(2)),
                        '==',
                        IntLiteral(0)
                    ),
                    '&&',
                    BinaryOp(
                        MemberAccess(Identifier('n'), 'val'),
                        '>',
                        BinaryOp(
                            MemberAccess(Identifier('n'), 'left'),
                            '+',
                            MemberAccess(Identifier('n'), 'right')
                        )
                    )
                ),
                BlockStmt([
                    ExprStmt(AssignExpr(
                        MemberAccess(Identifier('n'), 'val'),
                        BinaryOp(
                            BinaryOp(
                                BinaryOp(
                                    MemberAccess(Identifier('n'), 'left'),
                                    '*',
                                    MemberAccess(Identifier('n'), 'depth')
                                ),
                                '-',
                                BinaryOp(
                                    MemberAccess(Identifier('n'), 'right'),
                                    '%',
                                    MemberAccess(Identifier('n'), 'depth')
                                )
                            ),
                            '+',
                            IntLiteral(1)
                        )
                    )),
                ]),
                BlockStmt([
                    SwitchStmt(
                        BinaryOp(MemberAccess(Identifier('n'), 'val'), '%', IntLiteral(3)),
                        [
                            CaseStmt(IntLiteral(0), [
                                ExprStmt(AssignExpr(
                                    MemberAccess(Identifier('n'), 'left'),
                                    BinaryOp(MemberAccess(Identifier('n'), 'left'), '+', IntLiteral(1))
                                )),
                                BreakStmt(),
                            ]),
                            CaseStmt(IntLiteral(1), [
                                ExprStmt(AssignExpr(
                                    MemberAccess(Identifier('n'), 'right'),
                                    BinaryOp(MemberAccess(Identifier('n'), 'right'), '-', IntLiteral(1))
                                )),
                                BreakStmt(),
                            ]),
                        ],
                        DefaultStmt([
                            ExprStmt(AssignExpr(
                                MemberAccess(Identifier('n'), 'depth'),
                                BinaryOp(MemberAccess(Identifier('n'), 'depth'), '*', IntLiteral(2))
                            )),
                            BreakStmt(),
                        ])
                    ),
                ])
            ),
        ])),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_108():
    """6 mixed-type params; return (a+b) * -(c-d) / (e%f) — prefix minus on a sub-expression."""
    source = (
        "int mayhem(int a, float b, int c, float d, int e, float f) {"
        "    return (a + b) * -(c - d) / (e % f);"
        "}"
    )
    expected = Program([
        FuncDecl(IntType(), 'mayhem', [
            Param(IntType(), 'a'),
            Param(FloatType(), 'b'),
            Param(IntType(), 'c'),
            Param(FloatType(), 'd'),
            Param(IntType(), 'e'),
            Param(FloatType(), 'f'),
        ], BlockStmt([
            ReturnStmt(
                BinaryOp(
                    BinaryOp(
                        BinaryOp(Identifier('a'), '+', Identifier('b')),
                        '*',
                        PrefixOp('-', BinaryOp(Identifier('c'), '-', Identifier('d')))
                    ),
                    '/',
                    BinaryOp(Identifier('e'), '%', Identifier('f'))
                )
            )
        ]))
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_109():
    """Mutual call ring: f -> g -> h -> f; each passes an arithmetic expr, h passes a struct literal."""
    source = (
        "struct T { int x; int y; };"
        "int f(T t) { return g(t.x * t.y - 1) + t.x; }"
        "int g(int n) { return h(n % 7 + n / 2) - n; }"
        "int h(int n) { return f({n, n + 1}) * 2; }"
    )
    expected = Program([
        StructDecl('T', [
            MemberDecl(IntType(), 'x'),
            MemberDecl(IntType(), 'y'),
        ]),
        FuncDecl(IntType(), 'f', [Param(StructType('T'), 't')], BlockStmt([
            ReturnStmt(
                BinaryOp(
                    FuncCall('g', [
                        BinaryOp(
                            BinaryOp(MemberAccess(Identifier('t'), 'x'), '*', MemberAccess(Identifier('t'), 'y')),
                            '-',
                            IntLiteral(1)
                        )
                    ]),
                    '+',
                    MemberAccess(Identifier('t'), 'x')
                )
            )
        ])),
        FuncDecl(IntType(), 'g', [Param(IntType(), 'n')], BlockStmt([
            ReturnStmt(
                BinaryOp(
                    FuncCall('h', [
                        BinaryOp(
                            BinaryOp(Identifier('n'), '%', IntLiteral(7)),
                            '+',
                            BinaryOp(Identifier('n'), '/', IntLiteral(2))
                        )
                    ]),
                    '-',
                    Identifier('n')
                )
            )
        ])),
        FuncDecl(IntType(), 'h', [Param(IntType(), 'n')], BlockStmt([
            ReturnStmt(
                BinaryOp(
                    FuncCall('f', [
                        StructLiteral([
                            Identifier('n'),
                            BinaryOp(Identifier('n'), '+', IntLiteral(1))
                        ])
                    ]),
                    '*',
                    IntLiteral(2)
                )
            )
        ])),
    ])
    assert str(ASTGenerator(source).generate()) == str(expected)


def test_ast_110():
    """Full program: 4 nested structs, 4 functions, every statement/expression type, 3-level member access chain."""
    source = (
        "struct Vec2 { int x; int y; };"
        "struct Vec3 { Vec2 xy; int z; };"
        "struct Ray { Vec3 origin; Vec3 dir; };"
        "struct Hit { Ray ray; float t; int did_hit; };"

        "int dot2(Vec2 a, Vec2 b) { return a.x * b.x + a.y * b.y; }"

        "float rayT(Hit h) {"
        "    if (h.did_hit && h.t > 0.0) {"
        "        return h.t * 2.0 - 1.0;"
        "    }"
        "    return 0.0;"
        "}"

        "void march(Ray r, int steps) {"
        "    int i = 0;"
        "    float dist = 0.0;"
        "    for (int s = 0; s < steps && dist < 100.0; s++) {"
        "        dist = dist + r.dir.xy.x * 1.0 + r.dir.xy.y * 1.0;"
        "        if (dist > 50.0) { break; }"
        "    }"
        "    int j = steps;"
        "    while (j > 0 && dist > 0.0) {"
        "        switch (j % 3) {"
        "            case 0: dist = dist - 1.0; break;"
        "            case 1: dist = dist * 0.5; j--; break;"
        "            default: continue;"
        "        }"
        "        j = j - 1;"
        "    }"
        "    printFloat(dist);"
        "}"

        "void main() {"
        "    auto v = {3, 4};"
        "    auto w = {{v, 0}, {v, 1}};"
        "    auto h = {{w, {v, 2}}, 1.5, dot2(v, v) > 0};"
        "    march(h.ray, 10);"
        "    printFloat(rayT(h));"
        "}"
    )

    # ── structs ──────────────────────────────────────────────────────────────
    vec2  = StructDecl('Vec2', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')])
    vec3  = StructDecl('Vec3', [MemberDecl(StructType('Vec2'), 'xy'), MemberDecl(IntType(), 'z')])
    ray   = StructDecl('Ray',  [MemberDecl(StructType('Vec3'), 'origin'), MemberDecl(StructType('Vec3'), 'dir')])
    hit   = StructDecl('Hit',  [MemberDecl(StructType('Ray'), 'ray'), MemberDecl(FloatType(), 't'), MemberDecl(IntType(), 'did_hit')])

    # ── dot2 ─────────────────────────────────────────────────────────────────
    dot2 = FuncDecl(IntType(), 'dot2', [Param(StructType('Vec2'), 'a'), Param(StructType('Vec2'), 'b')], BlockStmt([
        ReturnStmt(BinaryOp(
            BinaryOp(MemberAccess(Identifier('a'), 'x'), '*', MemberAccess(Identifier('b'), 'x')),
            '+',
            BinaryOp(MemberAccess(Identifier('a'), 'y'), '*', MemberAccess(Identifier('b'), 'y'))
        ))
    ]))

    # ── rayT ─────────────────────────────────────────────────────────────────
    rayT = FuncDecl(FloatType(), 'rayT', [Param(StructType('Hit'), 'h')], BlockStmt([
        IfStmt(
            BinaryOp(
                MemberAccess(Identifier('h'), 'did_hit'),
                '&&',
                BinaryOp(MemberAccess(Identifier('h'), 't'), '>', FloatLiteral(0.0))
            ),
            BlockStmt([
                ReturnStmt(BinaryOp(
                    BinaryOp(MemberAccess(Identifier('h'), 't'), '*', FloatLiteral(2.0)),
                    '-',
                    FloatLiteral(1.0)
                ))
            ]),
            None
        ),
        ReturnStmt(FloatLiteral(0.0)),
    ]))

    # ── march ────────────────────────────────────────────────────────────────
    march = FuncDecl(VoidType(), 'march', [Param(StructType('Ray'), 'r'), Param(IntType(), 'steps')], BlockStmt([
        VarDecl(IntType(), 'i', IntLiteral(0)),
        VarDecl(FloatType(), 'dist', FloatLiteral(0.0)),
        ForStmt(
            VarDecl(IntType(), 's', IntLiteral(0)),
            BinaryOp(
                BinaryOp(Identifier('s'), '<', Identifier('steps')),
                '&&',
                BinaryOp(Identifier('dist'), '<', FloatLiteral(100.0))
            ),
            PostfixOp('++', Identifier('s')),
            BlockStmt([
                # dist = dist + r.dir.xy.x * 1.0 + r.dir.xy.y * 1.0
                ExprStmt(AssignExpr(
                    Identifier('dist'),
                    BinaryOp(
                        BinaryOp(
                            Identifier('dist'),
                            '+',
                            BinaryOp(
                                MemberAccess(MemberAccess(MemberAccess(Identifier('r'), 'dir'), 'xy'), 'x'),
                                '*',
                                FloatLiteral(1.0)
                            )
                        ),
                        '+',
                        BinaryOp(
                            MemberAccess(MemberAccess(MemberAccess(Identifier('r'), 'dir'), 'xy'), 'y'),
                            '*',
                            FloatLiteral(1.0)
                        )
                    )
                )),
                IfStmt(
                    BinaryOp(Identifier('dist'), '>', FloatLiteral(50.0)),
                    BlockStmt([BreakStmt()]),
                    None
                ),
            ])
        ),
        VarDecl(IntType(), 'j', Identifier('steps')),
        WhileStmt(
            BinaryOp(
                BinaryOp(Identifier('j'), '>', IntLiteral(0)),
                '&&',
                BinaryOp(Identifier('dist'), '>', FloatLiteral(0.0))
            ),
            BlockStmt([
                SwitchStmt(
                    BinaryOp(Identifier('j'), '%', IntLiteral(3)),
                    [
                        CaseStmt(IntLiteral(0), [
                            ExprStmt(AssignExpr(Identifier('dist'),
                                BinaryOp(Identifier('dist'), '-', FloatLiteral(1.0)))),
                            BreakStmt(),
                        ]),
                        CaseStmt(IntLiteral(1), [
                            ExprStmt(AssignExpr(Identifier('dist'),
                                BinaryOp(Identifier('dist'), '*', FloatLiteral(0.5)))),
                            ExprStmt(PostfixOp('--', Identifier('j'))),
                            BreakStmt(),
                        ]),
                    ],
                    DefaultStmt([ContinueStmt()])
                ),
                ExprStmt(AssignExpr(Identifier('j'), BinaryOp(Identifier('j'), '-', IntLiteral(1)))),
            ])
        ),
        ExprStmt(FuncCall('printFloat', [Identifier('dist')])),
    ]))

    # ── main ─────────────────────────────────────────────────────────────────
    main = FuncDecl(VoidType(), 'main', [], BlockStmt([
        VarDecl(None, 'v', StructLiteral([IntLiteral(3), IntLiteral(4)])),
        VarDecl(None, 'w', StructLiteral([
            StructLiteral([Identifier('v'), IntLiteral(0)]),
            StructLiteral([Identifier('v'), IntLiteral(1)]),
        ])),
        VarDecl(None, 'h', StructLiteral([
            StructLiteral([Identifier('w'), StructLiteral([Identifier('v'), IntLiteral(2)])]),
            FloatLiteral(1.5),
            BinaryOp(FuncCall('dot2', [Identifier('v'), Identifier('v')]), '>', IntLiteral(0)),
        ])),
        ExprStmt(FuncCall('march', [MemberAccess(Identifier('h'), 'ray'), IntLiteral(10)])),
        ExprStmt(FuncCall('printFloat', [FuncCall('rayT', [Identifier('h')])])),
    ]))

    expected = Program([vec2, vec3, ray, hit, dot2, rayT, march, main])
    assert str(ASTGenerator(source).generate()) == str(expected)


