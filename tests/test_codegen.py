"""
Test cases for TyC code generation.
"""

from src.utils.nodes import *
from tests.utils import CodeGenerator


def test_001():
    """Test 1: Hello World - print string"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("Hello World")]))
            ])
        )
    ])
    expected = "Hello World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_002():
    """Test 2: Print integer"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [IntLiteral(42)]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_003():
    """Test 3: Print float"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printFloat", [FloatLiteral(3.14)]))
            ])
        )
    ])
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_004():
    """Test 4: Variable declaration and assignment"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ])
        )
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_005():
    """Test 5: Binary operation - addition"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(IntLiteral(5), "+", IntLiteral(3))
                ]))
            ])
        )
    ])
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_006():
    """Test 6: Binary operation - multiplication"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(IntLiteral(6), "*", IntLiteral(7))
                ]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_007():
    """Test 7: If statement"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                IfStmt(
                    BinaryOp(IntLiteral(1), "<", IntLiteral(2)),
                    ExprStmt(FuncCall("printString", [StringLiteral("yes")])),
                    ExprStmt(FuncCall("printString", [StringLiteral("no")]))
                )
            ])
        )
    ])
    expected = "yes"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_008():
    """Test 8: While loop"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                WhileStmt(
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    BlockStmt([
                        ExprStmt(FuncCall("printInt", [Identifier("i")])),
                        ExprStmt(AssignExpr(
                            Identifier("i"),
                            BinaryOp(Identifier("i"), "+", IntLiteral(1))
                        ))
                    ])
                )
            ])
        )
    ])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_009():
    """Test 9: Function call with return value"""
    ast = Program([
        FuncDecl(
            IntType(),
            "add",
            [Param(IntType(), "a"), Param(IntType(), "b")],
            BlockStmt([
                ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
            ])
        ),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                ExprStmt(FuncCall("printInt", [
                    FuncCall("add", [IntLiteral(20), IntLiteral(22)])
                ]))
            ])
        )
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_010():
    """Test 10: Multiple statements - arithmetic operations"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(10)),
                VarDecl(IntType(), "y", IntLiteral(20)),
                ExprStmt(FuncCall("printInt", [
                    BinaryOp(Identifier("x"), "+", Identifier("y"))
                ]))
            ])
        )
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_011():
    """Test 11: Struct member assignment and access"""
    ast = Program([
        StructDecl("Point", [
            MemberDecl(IntType(), "x"),
            MemberDecl(IntType(), "y"),
        ]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Point"), "p", StructLiteral([
                    IntLiteral(0),
                    IntLiteral(0),
                ])),
                ExprStmt(AssignExpr(
                    MemberAccess(Identifier("p"), "x"),
                    IntLiteral(10),
                )),
                ExprStmt(AssignExpr(
                    MemberAccess(Identifier("p"), "y"),
                    IntLiteral(20),
                )),
                ExprStmt(FuncCall("printInt", [
                    MemberAccess(Identifier("p"), "x")
                ])),
                ExprStmt(FuncCall("printInt", [
                    MemberAccess(Identifier("p"), "y")
                ])),
            ])
        )
    ])
    expected = "1020"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_012():
    """Test 12: Nested struct literal and access"""
    ast = Program([
        StructDecl("Inside", [
            MemberDecl(IntType(), "x"),
            MemberDecl(IntType(), "y"),
        ]),
        StructDecl("Outside", [
            MemberDecl(StructType("Inside"), "i"),
            MemberDecl(FloatType(), "f"),
            MemberDecl(StringType(), "t"),
        ]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Outside"), "o", StructLiteral([
                    StructLiteral([IntLiteral(1), IntLiteral(2)]),
                    FloatLiteral(3.14),
                    StringLiteral("hello"),
                ])),
                ExprStmt(FuncCall("printInt", [
                    MemberAccess(MemberAccess(Identifier("o"), "i"), "x")
                ])),
                ExprStmt(FuncCall("printString", [
                    MemberAccess(Identifier("o"), "t")
                ])),
            ])
        )
    ])
    expected = "1hello"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_013():
    """Test 13: Prefix vs postfix increment"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(1)),
                VarDecl(IntType(), "y", PrefixOp("++", Identifier("x"))),
                VarDecl(IntType(), "z", PostfixOp("++", Identifier("x"))),
                ExprStmt(FuncCall("printInt", [Identifier("y")])),
                ExprStmt(FuncCall("printInt", [Identifier("z")])),
                ExprStmt(FuncCall("printInt", [Identifier("x")])),
            ])
        )
    ])
    expected = "223"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_014():
    """Test 14: Switch fall-through"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(2)),
                SwitchStmt(
                    Identifier("x"),
                    [
                        CaseStmt(IntLiteral(1), [
                            ExprStmt(FuncCall("printString", [StringLiteral("A")])),
                            BreakStmt(),
                        ]),
                        CaseStmt(IntLiteral(2), [
                            ExprStmt(FuncCall("printString", [StringLiteral("B")]))
                        ]),
                        CaseStmt(IntLiteral(3), [
                            ExprStmt(FuncCall("printString", [StringLiteral("C")])),
                            BreakStmt(),
                        ]),
                    ],
                    DefaultStmt([
                        ExprStmt(FuncCall("printString", [StringLiteral("D")]))
                    ]),
                )
            ])
        )
    ])
    expected = "BC"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_015():
    """Test 15: For loop with continue"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                    ForStmt(
                        AssignExpr(Identifier("i"), IntLiteral(0)),
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    PostfixOp("++", Identifier("i")),
                    BlockStmt([
                        IfStmt(
                            BinaryOp(Identifier("i"), "==", IntLiteral(1)),
                            ContinueStmt(),
                        ),
                        ExprStmt(FuncCall("printInt", [Identifier("i")]))
                    ]),
                )
            ])
        )
    ])
    expected = "02"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_016():
    """Test 16: Postfix increment on struct member"""
    ast = Program([
        StructDecl("Box", [
            MemberDecl(IntType(), "x"),
        ]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Box"), "b", StructLiteral([
                    IntLiteral(5)
                ])),
                ExprStmt(PostfixOp("++", MemberAccess(Identifier("b"), "x"))),
                ExprStmt(FuncCall("printInt", [
                    MemberAccess(Identifier("b"), "x")
                ])),
            ])
        )
    ])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_017():
    """Test 17: Struct assignment copy"""
    ast = Program([
        StructDecl("Node", [
            MemberDecl(IntType(), "x"),
        ]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Node"), "a", StructLiteral([
                    IntLiteral(1)
                ])),
                VarDecl(StructType("Node"), "b"),
                ExprStmt(AssignExpr(Identifier("b"), Identifier("a"))),
                ExprStmt(FuncCall("printInt", [
                    MemberAccess(Identifier("b"), "x")
                ])),
            ])
        )
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_018():
    """Test 18: Nested member assignment"""
    ast = Program([
        StructDecl("Inner", [
            MemberDecl(IntType(), "x"),
            MemberDecl(IntType(), "y"),
        ]),
        StructDecl("Outer", [
            MemberDecl(StructType("Inner"), "i"),
            MemberDecl(FloatType(), "f"),
            MemberDecl(StringType(), "t"),
        ]),
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(StructType("Outer"), "o", StructLiteral([
                    StructLiteral([IntLiteral(1), IntLiteral(2)]),
                    FloatLiteral(3.14),
                    StringLiteral("hi"),
                ])),
                ExprStmt(AssignExpr(
                    MemberAccess(MemberAccess(Identifier("o"), "i"), "x"),
                    IntLiteral(5),
                )),
                ExprStmt(FuncCall("printInt", [
                    MemberAccess(MemberAccess(Identifier("o"), "i"), "x")
                ])),
            ])
        )
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_019():
    """Test 19: For loop with prefix update"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "i", IntLiteral(0)),
                    ForStmt(
                        AssignExpr(Identifier("i"), IntLiteral(0)),
                    BinaryOp(Identifier("i"), "<", IntLiteral(3)),
                    PrefixOp("++", Identifier("i")),
                    ExprStmt(FuncCall("printInt", [Identifier("i")])),
                )
            ])
        )
    ])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_020():
    """Test 20: Switch default"""
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                SwitchStmt(
                    IntLiteral(2),
                    [
                        CaseStmt(IntLiteral(1), [
                            ExprStmt(FuncCall("printString", [StringLiteral("A")])),
                            BreakStmt(),
                        ])
                    ],
                    DefaultStmt([
                        ExprStmt(FuncCall("printString", [StringLiteral("D")]))
                    ]),
                )
            ])
        )
    ])
    expected = "D"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_021():
    """Test 21: Auto type inference and basic arithmetic"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(None, 'x', FloatLiteral(10.0)),
            VarDecl(None, 'y', FloatLiteral(3.14)),
            VarDecl(None, 'z', BinaryOp(Identifier('x'), '+', Identifier('y'))),
            ExprStmt(FuncCall('printFloat', [
            Identifier('z')
        ]))
        ]))
        ])
    expected = '13.14'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_022():
    """Test 22: Function calling with arguments and return"""
    ast = Program([
            FuncDecl(IntType(), 'add', [
            Param(IntType(), 'a'),
            Param(IntType(), 'b')
        ], BlockStmt([
            ReturnStmt(BinaryOp(Identifier('a'), '+', Identifier('b')))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('printInt', [
            FuncCall('add', [
            IntLiteral(5),
            IntLiteral(7)
        ])
        ]))
        ]))
        ])
    expected = '12'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_023():
    """Test 23: Struct literal and member access"""
    ast = Program([
            StructDecl('Point', [
            MemberDecl(IntType(), 'x'),
            MemberDecl(IntType(), 'y')
        ]),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(StructType('Point'), 'p', StructLiteral([
            IntLiteral(10),
            IntLiteral(20)
        ])),
            ExprStmt(FuncCall('printInt', [
            BinaryOp(MemberAccess(Identifier('p'), 'x'), '+', MemberAccess(Identifier('p'), 'y'))
        ]))
        ]))
        ])
    expected = '30'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_024():
    """Test 24: Nested struct member access"""
    ast = Program([
            StructDecl('Inner', [
            MemberDecl(IntType(), 'val')
        ]),
            StructDecl('Outer', [
            MemberDecl(StructType('Inner'), 'i'),
            MemberDecl(FloatType(), 'f')
        ]),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(StructType('Outer'), 'o', StructLiteral([
            StructLiteral([
            IntLiteral(5)
        ]),
            FloatLiteral(2.5)
        ])),
            ExprStmt(FuncCall('printInt', [
            MemberAccess(MemberAccess(Identifier('o'), 'i'), 'val')
        ])),
            ExprStmt(FuncCall('printFloat', [
            MemberAccess(Identifier('o'), 'f')
        ]))
        ]))
        ])
    expected = '52.5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_025():
    """Test 25: For loop with arithmetic"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'sum', IntLiteral(0)),
            ForStmt(VarDecl(IntType(), 'i', IntLiteral(0)), BinaryOp(Identifier('i'), '<', IntLiteral(5)), PostfixOp('++', Identifier('i')), BlockStmt([
            ExprStmt(AssignExpr(Identifier('sum'), BinaryOp(Identifier('sum'), '+', Identifier('i'))))
        ])),
            ExprStmt(FuncCall('printInt', [
            Identifier('sum')
        ]))
        ]))
        ])
    expected = '10'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_026():
    """Test 26: While loop with continue and break"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'i', IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier('i'), '<', IntLiteral(10)), BlockStmt([
            ExprStmt(PostfixOp('++', Identifier('i'))),
            IfStmt(BinaryOp(Identifier('i'), '==', IntLiteral(2)), BlockStmt([
            ContinueStmt()
        ]), None),
            IfStmt(BinaryOp(Identifier('i'), '==', IntLiteral(4)), BlockStmt([
            BreakStmt()
        ]), None),
            ExprStmt(FuncCall('printInt', [
            Identifier('i')
        ]))
        ]))
        ]))
        ])
    expected = '13'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_027():
    """Test 27: Switch with multiple cases and default"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ForStmt(VarDecl(IntType(), 'i', IntLiteral(1)), BinaryOp(Identifier('i'), '<=', IntLiteral(3)), PostfixOp('++', Identifier('i')), BlockStmt([
            SwitchStmt(Identifier('i'), [
            CaseStmt(IntLiteral(1), [
            BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(10)
        ])),
            BreakStmt()
        ])
        ]),
            CaseStmt(IntLiteral(2), [
            BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(20)
        ])),
            BreakStmt()
        ])
        ])
        ], DefaultStmt([
            BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(30)
        ]))
        ])
        ]))
        ]))
        ]))
        ])
    expected = '102030'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_028():
    """Test 28: Prefix and postfix increment/decrement"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'a', IntLiteral(5)),
            ExprStmt(FuncCall('printInt', [
            PostfixOp('++', Identifier('a'))
        ])),
            ExprStmt(FuncCall('printInt', [
            PrefixOp('++', Identifier('a'))
        ])),
            ExprStmt(FuncCall('printInt', [
            PostfixOp('--', Identifier('a'))
        ])),
            ExprStmt(FuncCall('printInt', [
            PrefixOp('--', Identifier('a'))
        ]))
        ]))
        ])
    expected = '5775'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_029():
    """Test 29: Logical operators (&&, ||, !)"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            IfStmt(BinaryOp(IntLiteral(1), '&&', IntLiteral(1)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(1)
        ]))
        ]), None),
            IfStmt(BinaryOp(IntLiteral(1), '&&', IntLiteral(0)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(2)
        ]))
        ]), None),
            IfStmt(BinaryOp(IntLiteral(0), '||', IntLiteral(1)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(3)
        ]))
        ]), None),
            IfStmt(PrefixOp('!', IntLiteral(0)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(4)
        ]))
        ]), None)
        ]))
        ])
    expected = '134'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_030():
    """Test 30: Relational operators"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            IfStmt(BinaryOp(IntLiteral(5), '>', IntLiteral(3)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(1)
        ]))
        ]), None),
            IfStmt(BinaryOp(IntLiteral(2), '>=', IntLiteral(2)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(2)
        ]))
        ]), None),
            IfStmt(BinaryOp(IntLiteral(1), '<', IntLiteral(0)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(3)
        ]))
        ]), None),
            IfStmt(BinaryOp(IntLiteral(4), '<=', IntLiteral(5)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(4)
        ]))
        ]), None),
            IfStmt(BinaryOp(IntLiteral(6), '==', IntLiteral(6)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(5)
        ]))
        ]), None),
            IfStmt(BinaryOp(IntLiteral(7), '!=', IntLiteral(7)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(6)
        ]))
        ]), None)
        ]))
        ])
    expected = '1245'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_031():
    """Test 31: Complex assignment expressions"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'a', None),
            VarDecl(IntType(), 'b', None),
            VarDecl(IntType(), 'c', None),
            ExprStmt(AssignExpr(Identifier('a'), AssignExpr(Identifier('b'), AssignExpr(Identifier('c'), IntLiteral(10))))),
            ExprStmt(FuncCall('printInt', [
            Identifier('a')
        ])),
            ExprStmt(FuncCall('printInt', [
            Identifier('b')
        ])),
            ExprStmt(FuncCall('printInt', [
            Identifier('c')
        ]))
        ]))
        ])
    expected = '101010'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_032():
    """Test 32: Nested block shadowing"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(1)),
            BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(2)),
            ExprStmt(FuncCall('printInt', [
            Identifier('x')
        ]))
        ]),
            ExprStmt(FuncCall('printInt', [
            Identifier('x')
        ]))
        ]))
        ])
    expected = '21'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_033():
    """Test 33: Recursive function (factorial)"""
    ast = Program([
            FuncDecl(IntType(), 'fact', [
            Param(IntType(), 'n')
        ], BlockStmt([
            IfStmt(BinaryOp(Identifier('n'), '<=', IntLiteral(1)), BlockStmt([
            ReturnStmt(IntLiteral(1))
        ]), None),
            ReturnStmt(BinaryOp(Identifier('n'), '*', FuncCall('fact', [
            BinaryOp(Identifier('n'), '-', IntLiteral(1))
        ])))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('printInt', [
            FuncCall('fact', [
            IntLiteral(5)
        ])
        ]))
        ]))
        ])
    expected = '120'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_034():
    """Test 34: Function calls inside expressions"""
    ast = Program([
            FuncDecl(IntType(), 'foo', [
            
        ], BlockStmt([
            ReturnStmt(IntLiteral(2))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('printInt', [
            BinaryOp(BinaryOp(FuncCall('foo', [
            
        ]), '*', FuncCall('foo', [
            
        ])), '+', IntLiteral(1))
        ]))
        ]))
        ])
    expected = '5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_035():
    """Test 35: Struct parameter passing"""
    ast = Program([
            StructDecl('S', [
            MemberDecl(IntType(), 'a')
        ]),
            FuncDecl(VoidType(), 'modify', [
            Param(StructType('S'), 's')
        ], BlockStmt([
            ExprStmt(FuncCall('printInt', [
            MemberAccess(Identifier('s'), 'a')
        ]))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(StructType('S'), 's', StructLiteral([
            IntLiteral(99)
        ])),
            ExprStmt(FuncCall('modify', [
            Identifier('s')
        ]))
        ]))
        ])
    expected = '99'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_036():
    """Test 36: Return struct from function"""
    ast = Program([
        StructDecl('S', [MemberDecl(FloatType(), 'a')]),
        FuncDecl(StructType('S'), 'getS', [], BlockStmt([
            VarDecl(StructType('S'), 'tmp', StructLiteral([FloatLiteral(3.5)])),
            ReturnStmt(Identifier('tmp'))
        ])),
        FuncDecl(VoidType(), 'main', [], BlockStmt([
            VarDecl(StructType('S'), 's', FuncCall('getS', [])),
            ExprStmt(FuncCall('printFloat', [MemberAccess(Identifier('s'), 'a')]))
        ]))
    ])
    expected = '3.5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_037():
    """Test 37: Complex nested loop with break/continue"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ForStmt(VarDecl(IntType(), 'i', IntLiteral(0)), BinaryOp(Identifier('i'), '<', IntLiteral(3)), PostfixOp('++', Identifier('i')), BlockStmt([
            ForStmt(VarDecl(IntType(), 'j', IntLiteral(0)), BinaryOp(Identifier('j'), '<', IntLiteral(3)), PostfixOp('++', Identifier('j')), BlockStmt([
            IfStmt(BinaryOp(Identifier('i'), '==', IntLiteral(1)), BlockStmt([
            ContinueStmt()
        ]), None),
            IfStmt(BinaryOp(Identifier('j'), '==', IntLiteral(2)), BlockStmt([
            BreakStmt()
        ]), None),
            ExprStmt(FuncCall('printInt', [
            Identifier('i')
        ])),
            ExprStmt(FuncCall('printInt', [
            Identifier('j')
        ]))
        ]))
        ]))
        ]))
        ])
    expected = '00012021'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_038():
    """Test 38: Struct assignment (struct = struct)"""
    ast = Program([
        StructDecl('P', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]),
        FuncDecl(VoidType(), 'main', [], BlockStmt([
            VarDecl(StructType('P'), 'p1', StructLiteral([IntLiteral(1), IntLiteral(2)])),
            VarDecl(StructType('P'), 'p2', Identifier('p1')),
            ExprStmt(AssignExpr(MemberAccess(Identifier('p1'), 'x'), IntLiteral(9))),
            ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('p2'), 'x')])),
            ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('p2'), 'y')]))
        ]))
    ])
    expected = '92'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_039():
    """Test 39: Multiple variable declarations"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'a', IntLiteral(1)),
            VarDecl(IntType(), 'b', IntLiteral(2)),
            VarDecl(IntType(), 'c', BinaryOp(Identifier('a'), '+', Identifier('b'))),
            ExprStmt(FuncCall('printInt', [
            Identifier('c')
        ]))
        ]))
        ])
    expected = '3'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_040():
    """Test 40: Auto type inferred from another variable"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'origin', IntLiteral(42)),
            VarDecl(None, 'inferred', Identifier('origin')),
            ExprStmt(FuncCall('printInt', [
            Identifier('inferred')
        ]))
        ]))
        ])
    expected = '42'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_041():
    """Test 41: Float arithmetic"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(FloatType(), 'a', FloatLiteral(5.0)),
            VarDecl(FloatType(), 'b', FloatLiteral(2.0)),
            ExprStmt(FuncCall('printFloat', [
            BinaryOp(Identifier('a'), '/', Identifier('b'))
        ]))
        ]))
        ])
    expected = '2.5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_042():
    """Test 42: Float comparisons"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            IfStmt(BinaryOp(FloatLiteral(3.14), '>', FloatLiteral(3.0)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(1)
        ]))
        ]), None),
            IfStmt(BinaryOp(FloatLiteral(2.5), '<=', FloatLiteral(2.5)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(2)
        ]))
        ]), None)
        ]))
        ])
    expected = '12'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_043():
    """Test 43: String printing"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('printString', [
            StringLiteral('Hello')
        ])),
            ExprStmt(FuncCall('printString', [
            StringLiteral('World')
        ]))
        ]))
        ])
    expected = 'HelloWorld'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_044():
    """Test 44: If-else if-else chain"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(2)),
            IfStmt(BinaryOp(Identifier('x'), '==', IntLiteral(1)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(1)
        ]))
        ]), BlockStmt([
            IfStmt(BinaryOp(Identifier('x'), '==', IntLiteral(2)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(2)
        ]))
        ]), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(3)
        ]))
        ]))
        ]))
        ]))
        ])
    expected = '2'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_045():
    """Test 45: Switch without default"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(5)),
            SwitchStmt(Identifier('x'), [
            CaseStmt(IntLiteral(1), [
            BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(1)
        ])),
            BreakStmt()
        ])
        ]),
            CaseStmt(IntLiteral(5), [
            BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(5)
        ])),
            BreakStmt()
        ])
        ])
        ], None)
        ]))
        ])
    expected = '5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_046():
    """Test 46: Modulo operation"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('printInt', [
            BinaryOp(IntLiteral(10), '%', IntLiteral(3))
        ])),
            ExprStmt(FuncCall('printInt', [
            BinaryOp(IntLiteral(20), '%', IntLiteral(7))
        ]))
        ]))
        ])
    expected = '16'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_047():
    """Test 47: Type promotion (int + float)"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(None, 'res', BinaryOp(FloatLiteral(5.0), '+', FloatLiteral(2.5))),
            ExprStmt(FuncCall('printFloat', [
            Identifier('res')
        ]))
        ]))
        ])
    expected = '7.5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_048():
    """Test 48: Nested switch cases"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'a', IntLiteral(1)),
            VarDecl(IntType(), 'b', IntLiteral(2)),
            SwitchStmt(Identifier('a'), [
            CaseStmt(IntLiteral(1), [
            BlockStmt([
            SwitchStmt(Identifier('b'), [
            CaseStmt(IntLiteral(2), [
            BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(12)
        ])),
            BreakStmt()
        ])
        ])
        ], None),
            BreakStmt()
        ])
        ])
        ], None)
        ]))
        ])
    expected = '12'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_049():
    """Test 49: Short-circuit like evaluation with &&"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(0)),
            IfStmt(BinaryOp(IntLiteral(1), '&&', AssignExpr(Identifier('x'), IntLiteral(2))), BlockStmt([
            
        ]), None),
            ExprStmt(FuncCall('printInt', [
            Identifier('x')
        ]))
        ]))
        ])
    expected = '2'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_050():
    """Test 50: Empty blocks and returns"""
    ast = Program([
            FuncDecl(VoidType(), 'doNothing', [
            
        ], BlockStmt([
            BlockStmt([
            
        ]),
            ReturnStmt(None)
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('doNothing', [
            
        ])),
            ExprStmt(FuncCall('printInt', [
            IntLiteral(1)
        ]))
        ]))
        ])
    expected = '1'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_051():
    """Test 51: Nested inline struct assignments"""
    ast = Program([
            StructDecl('S1', [
            MemberDecl(IntType(), 'x'),
            MemberDecl(FloatType(), 'y')
        ]),
            StructDecl('S2', [
            MemberDecl(FloatType(), 'x'),
            MemberDecl(IntType(), 'y')
        ]),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(StructType('S1'), 's1', StructLiteral([
            IntLiteral(1),
            FloatLiteral(2.0)
        ])),
            VarDecl(StructType('S2'), 's2', None),
            ExprStmt(AssignExpr(MemberAccess(Identifier('s1'), 'x'), MemberAccess(AssignExpr(Identifier('s2'), StructLiteral([
            FloatLiteral(1.0),
            IntLiteral(99)
        ])), 'y'))),
            ExprStmt(FuncCall('printInt', [
            MemberAccess(Identifier('s1'), 'x')
        ]))
        ]))
        ])
    expected = '99'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_052():
    """Test 52: Extremely complex operator precedences"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(5)),
            VarDecl(IntType(), 'y', IntLiteral(2)),
            VarDecl(IntType(), 'z', IntLiteral(10)),
            VarDecl(IntType(), 'res', BinaryOp(BinaryOp(BinaryOp(Identifier('x'), '+', BinaryOp(Identifier('y'), '*', Identifier('z'))), '-', BinaryOp(BinaryOp(Identifier('z'), '/', Identifier('y')), '%', IntLiteral(3))), '+', BinaryOp(BinaryOp(Identifier('x'), '<', Identifier('z')), '&&', BinaryOp(Identifier('y'), '>', IntLiteral(1))))),
            ExprStmt(FuncCall('printInt', [
            Identifier('res')
        ]))
        ]))
        ])
    expected = '24'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_053():
    """Test 53: Shadowing inside complex branches"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(10)),
            IfStmt(BinaryOp(Identifier('x'), '==', IntLiteral(10)), BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(20)),
            ExprStmt(FuncCall('printInt', [
            Identifier('x')
        ]))
        ]), None),
            SwitchStmt(Identifier('x'), [
            CaseStmt(IntLiteral(10), [
            BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(30)),
            ExprStmt(FuncCall('printInt', [
            Identifier('x')
        ])),
            BreakStmt()
        ])
        ])
        ], None),
            ExprStmt(FuncCall('printInt', [
            Identifier('x')
        ]))
        ]))
        ])
    expected = '203010'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_054():
    """Test 54: ForStmt with VarDecl initialization (per spec)"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'sum', IntLiteral(0)),
            ForStmt(VarDecl(IntType(), 'i', IntLiteral(1)), BinaryOp(Identifier('i'), '<=', IntLiteral(3)), PostfixOp('++', Identifier('i')), BlockStmt([
            ExprStmt(AssignExpr(Identifier('sum'), BinaryOp(Identifier('sum'), '+', Identifier('i'))))
        ])),
            ExprStmt(FuncCall('printInt', [
            Identifier('sum')
        ]))
        ]))
        ])
    expected = '6'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_055():
    """Test 55: Type promotion on variable assignment"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(FloatType(), 'f', BinaryOp(IntLiteral(5), '+', FloatLiteral(3.14))),
            ExprStmt(FuncCall('printFloat', [
            Identifier('f')
        ]))
        ]))
        ])
    expected = '8.14'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_056():
    """Test 56: Returning struct literal directly"""
    ast = Program([
            StructDecl('S', [
            MemberDecl(IntType(), 'x'),
            MemberDecl(IntType(), 'y')
        ]),
            FuncDecl(StructType('S'), 'makeS', [
            
        ], BlockStmt([
            ReturnStmt(StructLiteral([
            IntLiteral(10),
            IntLiteral(20)
        ]))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(StructType('S'), 's', FuncCall('makeS', [
            
        ])),
            ExprStmt(FuncCall('printInt', [
            BinaryOp(MemberAccess(Identifier('s'), 'x'), '+', MemberAccess(Identifier('s'), 'y'))
        ]))
        ]))
        ])
    expected = '30'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_057():
    """Test 57: Empty statements and blocks"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            BlockStmt([
            
        ]),
            VarDecl(IntType(), 'x', IntLiteral(1)),
            BlockStmt([
            BlockStmt([
            BlockStmt([
            ExprStmt(AssignExpr(Identifier('x'), IntLiteral(2)))
        ])
        ])
        ]),
            ExprStmt(FuncCall('printInt', [
            Identifier('x')
        ]))
        ]))
        ])
    expected = '2'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_058():
    """Test 58: Deep struct nesting"""
    ast = Program([
            StructDecl('C', [
            MemberDecl(IntType(), 'v')
        ]),
            StructDecl('B', [
            MemberDecl(StructType('C'), 'c')
        ]),
            StructDecl('A', [
            MemberDecl(StructType('B'), 'b')
        ]),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(StructType('A'), 'a', StructLiteral([
            StructLiteral([
            StructLiteral([
            IntLiteral(42)
        ])
        ])
        ])),
            ExprStmt(FuncCall('printInt', [
            MemberAccess(MemberAccess(MemberAccess(Identifier('a'), 'b'), 'c'), 'v')
        ]))
        ]))
        ])
    expected = '42'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_059():
    """Test 59: Nested switches"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(1)),
            VarDecl(IntType(), 'y', IntLiteral(2)),
            SwitchStmt(Identifier('x'), [
            CaseStmt(IntLiteral(1), [
            BlockStmt([
            SwitchStmt(Identifier('y'), [
            CaseStmt(IntLiteral(1), [
            BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(11)
        ])),
            BreakStmt()
        ])
        ]),
            CaseStmt(IntLiteral(2), [
            BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(12)
        ])),
            BreakStmt()
        ])
        ])
        ], None),
            ExprStmt(FuncCall('printInt', [
            IntLiteral(1)
        ])),
            BreakStmt()
        ])
        ])
        ], None)
        ]))
        ])
    expected = '121'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_060():
    """Test 60: Short-circuit logic evaluation verification"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'a', IntLiteral(0)),
            VarDecl(IntType(), 'b', IntLiteral(0)),
            IfStmt(BinaryOp(IntLiteral(1), '||', AssignExpr(Identifier('a'), IntLiteral(1))), BlockStmt([
            
        ]), None),
            IfStmt(BinaryOp(IntLiteral(0), '&&', AssignExpr(Identifier('b'), IntLiteral(1))), BlockStmt([
            
        ]), None),
            ExprStmt(FuncCall('printInt', [
            Identifier('a')
        ])),
            ExprStmt(FuncCall('printInt', [
            Identifier('b')
        ]))
        ]))
        ])
    expected = '00'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_061():
    """Test 61: Cascading assignments with expressions"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'a', None),
            VarDecl(IntType(), 'b', None),
            VarDecl(IntType(), 'c', None),
            ExprStmt(AssignExpr(Identifier('a'), BinaryOp(AssignExpr(Identifier('b'), IntLiteral(2)), '+', AssignExpr(Identifier('c'), IntLiteral(3))))),
            ExprStmt(FuncCall('printInt', [
            Identifier('a')
        ])),
            ExprStmt(FuncCall('printInt', [
            Identifier('b')
        ])),
            ExprStmt(FuncCall('printInt', [
            Identifier('c')
        ]))
        ]))
        ])
    expected = '523'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_062():
    """Test 62: Unary operators chained"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(1)),
            ExprStmt(FuncCall('printInt', [
            PrefixOp('!', PrefixOp('!', PrefixOp('!', Identifier('x'))))
        ])),
            ExprStmt(FuncCall('printInt', [
            PrefixOp('-', PrefixOp('-', PrefixOp('-', Identifier('x'))))
        ]))
        ]))
        ])
    expected = '0-1'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_063():
    """Test 63: Prefix and postfix on struct members"""
    ast = Program([
            StructDecl('S', [
            MemberDecl(IntType(), 'x')
        ]),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(StructType('S'), 's', StructLiteral([
            IntLiteral(5)
        ])),
            ExprStmt(FuncCall('printInt', [
            PostfixOp('++', MemberAccess(Identifier('s'), 'x'))
        ])),
            ExprStmt(FuncCall('printInt', [
            PrefixOp('++', MemberAccess(Identifier('s'), 'x'))
        ]))
        ]))
        ])
    expected = '57'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_064():
    """Test 64: Loops printing string values"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ForStmt(VarDecl(IntType(), 'i', IntLiteral(0)), BinaryOp(Identifier('i'), '<', IntLiteral(2)), PostfixOp('++', Identifier('i')), BlockStmt([
            ExprStmt(FuncCall('printString', [
            StringLiteral('hi')
        ]))
        ]))
        ]))
        ])
    expected = 'hihi'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_065():
    """Test 65: Unreachable code behavior"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(1)),
            IfStmt(BinaryOp(Identifier('x'), '==', IntLiteral(1)), BlockStmt([
            ReturnStmt(None),
            ExprStmt(FuncCall('printInt', [
            IntLiteral(99)
        ]))
        ]), None),
            ExprStmt(FuncCall('printInt', [
            IntLiteral(100)
        ]))
        ]))
        ])
    expected = ''
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_066():
    """Test 66: Modifying loop variable explicitly"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ForStmt(VarDecl(IntType(), 'i', IntLiteral(0)), BinaryOp(Identifier('i'), '<', IntLiteral(5)), PostfixOp('++', Identifier('i')), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            Identifier('i')
        ])),
            ExprStmt(PostfixOp('++', Identifier('i')))
        ]))
        ]))
        ])
    expected = '024'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_067():
    """Test 67: Parameter shadowing"""
    ast = Program([
            FuncDecl(IntType(), 'x', [
            Param(IntType(), 'x')
        ], BlockStmt([
            ReturnStmt(BinaryOp(Identifier('x'), '*', IntLiteral(2)))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('printInt', [
            FuncCall('x', [
            IntLiteral(5)
        ])
        ]))
        ]))
        ])
    expected = '10'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_068():
    """Test 68: Complex break condition in while(1)"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'i', IntLiteral(0)),
            WhileStmt(IntLiteral(1), BlockStmt([
            IfStmt(BinaryOp(PrefixOp('++', Identifier('i')), '>', IntLiteral(3)), BlockStmt([
            BreakStmt()
        ]), None),
            ExprStmt(FuncCall('printInt', [
            Identifier('i')
        ]))
        ]))
        ]))
        ])
    expected = '123'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_069():
    """Test 69: Assigning struct to auto type"""
    ast = Program([
            StructDecl('S', [
            MemberDecl(IntType(), 'v')
        ]),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(StructType('S'), 's1', StructLiteral([
            IntLiteral(100)
        ])),
            VarDecl(None, 's2', Identifier('s1')),
            ExprStmt(FuncCall('printInt', [
            MemberAccess(Identifier('s2'), 'v')
        ]))
        ]))
        ])
    expected = '100'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_070():
    """Test 70: Toggling boolean state"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'toggle', IntLiteral(1)),
            ForStmt(VarDecl(IntType(), 'i', IntLiteral(0)), BinaryOp(Identifier('i'), '<', IntLiteral(4)), PostfixOp('++', Identifier('i')), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            Identifier('toggle')
        ])),
            ExprStmt(AssignExpr(Identifier('toggle'), PrefixOp('!', Identifier('toggle'))))
        ]))
        ]))
        ])
    expected = '1010'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_071():
    """Test 71: Deeply nested function calls"""
    ast = Program([
            FuncDecl(IntType(), 'f', [
            Param(IntType(), 'x')
        ], BlockStmt([
            ReturnStmt(BinaryOp(Identifier('x'), '+', IntLiteral(1)))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('printInt', [
            FuncCall('f', [
            FuncCall('f', [
            FuncCall('f', [
            IntLiteral(0)
        ])
        ])
        ])
        ]))
        ]))
        ])
    expected = '3'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_072():
    """Test 72: Switch on relational expressions"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'a', IntLiteral(5)),
            VarDecl(IntType(), 'b', IntLiteral(3)),
            SwitchStmt(BinaryOp(Identifier('a'), '>', Identifier('b')), [
            CaseStmt(IntLiteral(1), [
            BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(1)
        ])),
            BreakStmt()
        ])
        ]),
            CaseStmt(IntLiteral(0), [
            BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(0)
        ])),
            BreakStmt()
        ])
        ])
        ], None)
        ]))
        ])
    expected = '1'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_073():
    """Test 73: Continue inside if inside switch inside loop"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ForStmt(VarDecl(IntType(), 'i', IntLiteral(0)), BinaryOp(Identifier('i'), '<', IntLiteral(3)), PostfixOp('++', Identifier('i')), BlockStmt([
            SwitchStmt(Identifier('i'), [
            CaseStmt(IntLiteral(1), [
            BlockStmt([
            IfStmt(IntLiteral(1), BlockStmt([
            ContinueStmt()
        ]), None)
        ])
        ])
        ], None),
            ExprStmt(FuncCall('printInt', [
            Identifier('i')
        ]))
        ]))
        ]))
        ])
    expected = '02'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_074():
    """Test 74: Assignment as truthy value"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(0)),
            IfStmt(AssignExpr(Identifier('x'), IntLiteral(2)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            Identifier('x')
        ]))
        ]), None)
        ]))
        ])
    expected = '2'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_075():
    """Test 75: Infinite loop structure with break"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'i', IntLiteral(0)),
            ForStmt(VarDecl(IntType(), 'j', IntLiteral(0)), IntLiteral(1), PostfixOp('++', Identifier('j')), BlockStmt([
            IfStmt(BinaryOp(Identifier('i'), '==', IntLiteral(2)), BlockStmt([
            BreakStmt()
        ]), None),
            ExprStmt(FuncCall('printInt', [
            PostfixOp('++', Identifier('i'))
        ]))
        ]))
        ]))
        ])
    expected = '01'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_076():
    """Test 76: Complex struct field mutations combined with loops"""
    ast = Program([
            StructDecl('S', [
            MemberDecl(IntType(), 'x')
        ]),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(StructType('S'), 's', StructLiteral([
            IntLiteral(3)
        ])),
            WhileStmt(BinaryOp(PrefixOp('--', MemberAccess(Identifier('s'), 'x')), '>', IntLiteral(0)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            MemberAccess(Identifier('s'), 'x')
        ]))
        ]))
        ]))
        ])
    expected = '21'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_077():
    """Test 77: For loop with missing optional fields"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'i', IntLiteral(0)),
            ForStmt(None, BinaryOp(Identifier('i'), '<', IntLiteral(3)), None, BlockStmt([
            ExprStmt(FuncCall('printInt', [
            Identifier('i')
        ])),
            ExprStmt(PostfixOp('++', Identifier('i')))
        ]))
        ]))
        ])
    expected = '012'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_078():
    """Test 78: Deeply nested block variable shadowing"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(1)),
            BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(2)),
            BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(3)),
            ExprStmt(FuncCall('printInt', [
            Identifier('x')
        ]))
        ]),
            ExprStmt(FuncCall('printInt', [
            Identifier('x')
        ]))
        ]),
            ExprStmt(FuncCall('printInt', [
            Identifier('x')
        ]))
        ]))
        ])
    expected = '321'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_079():
    """Test 79: Recursive function call (Factorial)"""
    ast = Program([
            FuncDecl(IntType(), 'fact', [
            Param(IntType(), 'n')
        ], BlockStmt([
            IfStmt(BinaryOp(Identifier('n'), '<=', IntLiteral(1)), ReturnStmt(IntLiteral(1)), None),
            ReturnStmt(BinaryOp(Identifier('n'), '*', FuncCall('fact', [
            BinaryOp(Identifier('n'), '-', IntLiteral(1))
        ])))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('printInt', [
            FuncCall('fact', [
            IntLiteral(5)
        ])
        ]))
        ]))
        ])
    expected = '120'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_080():
    """Test 80: Recursive function call (Fibonacci)"""
    ast = Program([
            FuncDecl(IntType(), 'fib', [
            Param(IntType(), 'n')
        ], BlockStmt([
            IfStmt(BinaryOp(Identifier('n'), '<=', IntLiteral(1)), ReturnStmt(Identifier('n')), None),
            ReturnStmt(BinaryOp(FuncCall('fib', [
            BinaryOp(Identifier('n'), '-', IntLiteral(1))
        ]), '+', FuncCall('fib', [
            BinaryOp(Identifier('n'), '-', IntLiteral(2))
        ])))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('printInt', [
            FuncCall('fib', [
            IntLiteral(6)
        ])
        ]))
        ]))
        ])
    expected = '8'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_081():
    """Test 81: Member access on returned struct"""
    ast = Program([
            StructDecl('S', [
            MemberDecl(IntType(), 'x')
        ]),
            FuncDecl(StructType('S'), 'getS', [
            
        ], BlockStmt([
            ReturnStmt(StructLiteral([
            IntLiteral(42)
        ]))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('printInt', [
            MemberAccess(FuncCall('getS', [
            
        ]), 'x')
        ]))
        ]))
        ])
    expected = '42'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_082():
    """Test 82: Array of structs equivalent (Struct containing struct)"""
    ast = Program([
            StructDecl('Inner', [
            MemberDecl(IntType(), 'val')
        ]),
            StructDecl('Outer', [
            MemberDecl(StructType('Inner'), 'in')
        ]),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(StructType('Outer'), 'o', StructLiteral([
            StructLiteral([
            IntLiteral(99)
        ])
        ])),
            ExprStmt(FuncCall('printInt', [
            MemberAccess(MemberAccess(Identifier('o'), 'in'), 'val')
        ]))
        ]))
        ])
    expected = '99'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_083():
    """Test 83: Mixed logic operators with arithmetic and relational"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'a', IntLiteral(1)),
            VarDecl(IntType(), 'b', IntLiteral(2)),
            VarDecl(IntType(), 'c', IntLiteral(3)),
            VarDecl(IntType(), 'd', IntLiteral(4)),
            IfStmt(BinaryOp(BinaryOp(BinaryOp(BinaryOp(Identifier('a'), '+', BinaryOp(Identifier('b'), '*', Identifier('c'))), '>', BinaryOp(Identifier('d'), '-', IntLiteral(1))), '&&', BinaryOp(Identifier('a'), '==', IntLiteral(1))), '||', BinaryOp(Identifier('c'), '!=', IntLiteral(3))), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(1)
        ]))
        ]), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(0)
        ]))
        ]))
        ]))
        ])
    expected = '1'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_084():
    """Test 84: Modulus and division precedence"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(20)),
            ExprStmt(FuncCall('printInt', [
            BinaryOp(BinaryOp(Identifier('x'), '/', IntLiteral(3)), '%', IntLiteral(4))
        ])),
            ExprStmt(FuncCall('printInt', [
            BinaryOp(BinaryOp(Identifier('x'), '%', IntLiteral(7)), '/', IntLiteral(2))
        ]))
        ]))
        ])
    expected = '23'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_085():
    """Test 85: Short-circuit logic inside for loop conditions"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'count', IntLiteral(0)),
            ForStmt(VarDecl(IntType(), 'i', IntLiteral(0)), BinaryOp(BinaryOp(Identifier('i'), '<', IntLiteral(5)), '&&', BinaryOp(Identifier('count'), '<', IntLiteral(2))), PostfixOp('++', Identifier('i')), BlockStmt([
            ExprStmt(PostfixOp('++', Identifier('count')))
        ])),
            ExprStmt(FuncCall('printInt', [
            Identifier('count')
        ]))
        ]))
        ])
    expected = '2'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_086():
    """Test 86: Evaluation order of arguments"""
    ast = Program([
            FuncDecl(IntType(), 'foo', [
            Param(IntType(), 'a'),
            Param(IntType(), 'b')
        ], BlockStmt([
            ReturnStmt(BinaryOp(BinaryOp(Identifier('a'), '*', IntLiteral(10)), '+', Identifier('b')))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(1)),
            ExprStmt(FuncCall('printInt', [
            FuncCall('foo', [
            PostfixOp('++', Identifier('x')),
            PrefixOp('++', Identifier('x'))
        ])
        ]))
        ]))
        ])
    expected = '13'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_087():
    """Test 87: Switch statement with no matching case and no default"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(5)),
            SwitchStmt(Identifier('x'), [
            CaseStmt(IntLiteral(1), [
            BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(1)
        ])),
            BreakStmt()
        ])
        ])
        ], None),
            ExprStmt(FuncCall('printInt', [
            IntLiteral(0)
        ]))
        ]))
        ])
    expected = '0'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_088():
    """Test 88: Switch statement with fall-through"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(1)),
            SwitchStmt(Identifier('x'), [
            CaseStmt(IntLiteral(1), [
            BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(1)
        ]))
        ])
        ]),
            CaseStmt(IntLiteral(2), [
            BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(2)
        ])),
            BreakStmt()
        ])
        ]),
            CaseStmt(IntLiteral(3), [
            BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(3)
        ]))
        ])
        ])
        ], None)
        ]))
        ])
    expected = '12'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_089():
    """Test 89: Returning from within a switch statement"""
    ast = Program([
            FuncDecl(IntType(), 'foo', [
            Param(IntType(), 'x')
        ], BlockStmt([
            SwitchStmt(Identifier('x'), [
            CaseStmt(IntLiteral(1), [
            BlockStmt([
            ReturnStmt(IntLiteral(100))
        ])
        ])
        ], DefaultStmt([
            BlockStmt([
            ReturnStmt(IntLiteral(200))
        ])
        ])),
            ReturnStmt(IntLiteral(300))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('printInt', [
            FuncCall('foo', [
            IntLiteral(1)
        ])
        ])),
            ExprStmt(FuncCall('printInt', [
            FuncCall('foo', [
            IntLiteral(2)
        ])
        ]))
        ]))
        ])
    expected = '100200'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_090():
    """Test 90: Struct assignment to itself"""
    ast = Program([
            StructDecl('S', [
            MemberDecl(IntType(), 'x')
        ]),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(StructType('S'), 's', StructLiteral([
            IntLiteral(5)
        ])),
            ExprStmt(AssignExpr(Identifier('s'), Identifier('s'))),
            ExprStmt(FuncCall('printInt', [
            MemberAccess(Identifier('s'), 'x')
        ]))
        ]))
        ])
    expected = '5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_091():
    """Test 91: Auto type inference for struct returned by function"""
    ast = Program([
            StructDecl('S', [
            MemberDecl(IntType(), 'x')
        ]),
            FuncDecl(StructType('S'), 'make', [
            
        ], BlockStmt([
            ReturnStmt(StructLiteral([
            IntLiteral(42)
        ]))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(None, 's', FuncCall('make', [
            
        ])),
            ExprStmt(FuncCall('printInt', [
            MemberAccess(Identifier('s'), 'x')
        ]))
        ]))
        ])
    expected = '42'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_092():
    """Test 92: Eager logic with side effects (nested)"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'a', IntLiteral(0)),
            VarDecl(IntType(), 'b', IntLiteral(0)),
            IfStmt(BinaryOp(AssignExpr(Identifier('a'), IntLiteral(1)), '&&', AssignExpr(Identifier('b'), IntLiteral(2))), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            BinaryOp(Identifier('a'), '+', Identifier('b'))
        ]))
        ]), None)
        ]))
        ])
    expected = '3'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_093():
    """Test 93: Multiple string prints"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('printString', [
            StringLiteral('A')
        ])),
            ExprStmt(FuncCall('printString', [
            StringLiteral('B')
        ])),
            ExprStmt(FuncCall('printString', [
            StringLiteral('C')
        ]))
        ]))
        ])
    expected = 'ABC'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_094():
    """Test 94: Returning early from a void function inside a loop"""
    ast = Program([
            FuncDecl(VoidType(), 'foo', [
            
        ], BlockStmt([
            ForStmt(VarDecl(IntType(), 'i', IntLiteral(0)), BinaryOp(Identifier('i'), '<', IntLiteral(5)), PostfixOp('++', Identifier('i')), BlockStmt([
            IfStmt(BinaryOp(Identifier('i'), '==', IntLiteral(2)), ReturnStmt(None), None),
            ExprStmt(FuncCall('printInt', [
            Identifier('i')
        ]))
        ]))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('foo', [
            
        ]))
        ]))
        ])
    expected = '01'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_095():
    """Test 95: Alternating logic inversions"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(1)),
            ExprStmt(FuncCall('printInt', [
            Identifier('x')
        ])),
            ExprStmt(FuncCall('printInt', [
            PrefixOp('!', Identifier('x'))
        ])),
            ExprStmt(FuncCall('printInt', [
            PrefixOp('!', PrefixOp('!', Identifier('x')))
        ])),
            ExprStmt(FuncCall('printInt', [
            PrefixOp('!', PrefixOp('!', PrefixOp('!', Identifier('x'))))
        ]))
        ]))
        ])
    expected = '1010'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_096():
    """Test 96: Dangling else problem test"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'x', IntLiteral(1)),
            VarDecl(IntType(), 'y', IntLiteral(2)),
            IfStmt(BinaryOp(Identifier('x'), '==', IntLiteral(1)), IfStmt(BinaryOp(Identifier('y'), '==', IntLiteral(3)), ExprStmt(FuncCall('printInt', [
            IntLiteral(3)
        ])), ExprStmt(FuncCall('printInt', [
            IntLiteral(4)
        ]))), None)
        ]))
        ])
    expected = '4'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_097():
    """Test 97: Float and Int comparison"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            IfStmt(BinaryOp(FloatLiteral(1.5), '>', IntLiteral(1)), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(1)
        ]))
        ]), BlockStmt([
            ExprStmt(FuncCall('printInt', [
            IntLiteral(0)
        ]))
        ]))
        ]))
        ])
    expected = '1'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_098():
    """Test 98: Modifying member of returned struct instance (ephemeral)"""
    ast = Program([
            StructDecl('S', [
            MemberDecl(IntType(), 'x')
        ]),
            FuncDecl(StructType('S'), 'get', [
            
        ], BlockStmt([
            ReturnStmt(StructLiteral([
            IntLiteral(10)
        ]))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            ExprStmt(FuncCall('printInt', [
            AssignExpr(MemberAccess(FuncCall('get', [
            
        ]), 'x'), IntLiteral(5))
        ]))
        ]))
        ])
    expected = '5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_099():
    """Test 99: Deep switch in while with break and continue interacting"""
    ast = Program([
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(IntType(), 'i', IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier('i'), '<', IntLiteral(5)), BlockStmt([
            ExprStmt(PostfixOp('++', Identifier('i'))),
            SwitchStmt(Identifier('i'), [
            CaseStmt(IntLiteral(2), [
            BlockStmt([
            ContinueStmt()
        ])
        ]),
            CaseStmt(IntLiteral(4), [
            BlockStmt([
            BreakStmt()
        ])
        ])
        ], None),
            ExprStmt(FuncCall('printInt', [
            Identifier('i')
        ]))
        ]))
        ]))
        ])
    expected = '1345'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_100():
    """Test 100: The massive combination test"""
    ast = Program([
            StructDecl('Point', [
            MemberDecl(IntType(), 'x'),
            MemberDecl(IntType(), 'y')
        ]),
            StructDecl('Rect', [
            MemberDecl(StructType('Point'), 'p1'),
            MemberDecl(StructType('Point'), 'p2')
        ]),
            FuncDecl(IntType(), 'area', [
            Param(StructType('Rect'), 'r')
        ], BlockStmt([
            VarDecl(IntType(), 'w', BinaryOp(MemberAccess(MemberAccess(Identifier('r'), 'p2'), 'x'), '-', MemberAccess(MemberAccess(Identifier('r'), 'p1'), 'x'))),
            VarDecl(IntType(), 'h', BinaryOp(MemberAccess(MemberAccess(Identifier('r'), 'p2'), 'y'), '-', MemberAccess(MemberAccess(Identifier('r'), 'p1'), 'y'))),
            ReturnStmt(BinaryOp(Identifier('w'), '*', Identifier('h')))
        ])),
            FuncDecl(VoidType(), 'main', [
            
        ], BlockStmt([
            VarDecl(StructType('Rect'), 'r', StructLiteral([
            StructLiteral([
            IntLiteral(0),
            IntLiteral(0)
        ]),
            StructLiteral([
            IntLiteral(5),
            IntLiteral(5)
        ])
        ])),
            VarDecl(IntType(), 'a', FuncCall('area', [
            Identifier('r')
        ])),
            IfStmt(BinaryOp(Identifier('a'), '==', IntLiteral(25)), BlockStmt([
            VarDecl(IntType(), 'count', IntLiteral(0)),
            ForStmt(VarDecl(IntType(), 'i', IntLiteral(0)), BinaryOp(Identifier('i'), '<', Identifier('a')), PostfixOp('++', Identifier('i')), BlockStmt([
            IfStmt(BinaryOp(BinaryOp(Identifier('i'), '%', IntLiteral(5)), '==', IntLiteral(0)), BlockStmt([
            ExprStmt(PostfixOp('++', Identifier('count')))
        ]), None)
        ])),
            ExprStmt(FuncCall('printInt', [
            Identifier('count')
        ]))
        ]), None)
        ]))
        ])
    expected = '5'
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_101():
    '''auto with implicit int return'''
    ast = Program([
        FuncDecl(None, "func", [], BlockStmt([
            ReturnStmt(IntLiteral(42))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(None, "a", FuncCall("func", [])),
            ExprStmt(FuncCall("printInt", [Identifier("a")]))
        ]))
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_102():
    '''chained assignment expression'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "a"),
            VarDecl(IntType(), "b"),
            VarDecl(IntType(), "c"),
            ExprStmt(AssignExpr(Identifier("a"), AssignExpr(Identifier("b"), AssignExpr(Identifier("c"), IntLiteral(10))))),
            ExprStmt(FuncCall("printInt", [Identifier("a")])),
            ExprStmt(FuncCall("printInt", [Identifier("b")])),
            ExprStmt(FuncCall("printInt", [Identifier("c")]))
        ]))
    ])
    expected = "101010"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_103():
    '''assignment expression in expression context'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "a"),
            VarDecl(IntType(), "b", BinaryOp(AssignExpr(Identifier("a"), IntLiteral(5)), "+", IntLiteral(7))),
            ExprStmt(FuncCall("printInt", [Identifier("a")])),
            ExprStmt(FuncCall("printInt", [Identifier("b")]))
        ]))
    ])
    expected = "512"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_104():
    '''auto infer struct member'''
    ast = Program([
        StructDecl("Point", [MemberDecl(IntType(), "x"), MemberDecl(IntType(), "y")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Point"), "p", StructLiteral([IntLiteral(10), IntLiteral(20)])),
            VarDecl(None, "x_coord", MemberAccess(Identifier("p"), "x")),
            ExprStmt(FuncCall("printInt", [Identifier("x_coord")]))
        ]))
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_105():
    '''nested scopes and shadowing'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(1)),
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(2)),
                ExprStmt(FuncCall("printInt", [Identifier("x")]))
            ]),
            ExprStmt(FuncCall("printInt", [Identifier("x")]))
        ]))
    ])
    expected = "21"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_106():
    '''assignment expression in return'''
    ast = Program([
        FuncDecl(IntType(), "foo", [], BlockStmt([
            VarDecl(IntType(), "x"),
            ReturnStmt(AssignExpr(Identifier("x"), IntLiteral(42)))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("foo", [])]))
        ]))
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_107():
    '''nested loops with break'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(VarDecl(IntType(), "i", IntLiteral(0)), BinaryOp(Identifier("i"), "<", IntLiteral(3)), PostfixOp("++", Identifier("i")), BlockStmt([
                ForStmt(VarDecl(IntType(), "j", IntLiteral(0)), BinaryOp(Identifier("j"), "<", IntLiteral(3)), PostfixOp("++", Identifier("j")), BlockStmt([
                    IfStmt(BinaryOp(Identifier("j"), "==", IntLiteral(1)), BlockStmt([BreakStmt()]), None),
                    ExprStmt(FuncCall("printInt", [Identifier("i")])),
                    ExprStmt(FuncCall("printInt", [Identifier("j")]))
                ]))
            ]))
        ]))
    ])
    expected = "001020"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_108():
    '''switch with default'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(5)),
            SwitchStmt(Identifier("x"), [
                CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printInt", [IntLiteral(1)])), BreakStmt()])
            ], DefaultStmt([ExprStmt(FuncCall("printInt", [IntLiteral(0)]))]))
        ]))
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_109():
    '''while loop with continue'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "j", IntLiteral(0)),
            WhileStmt(BinaryOp(Identifier("j"), "<", IntLiteral(4)), BlockStmt([
                ExprStmt(PostfixOp("++", Identifier("j"))),
                IfStmt(BinaryOp(Identifier("j"), "==", IntLiteral(2)), BlockStmt([ContinueStmt()]), None),
                ExprStmt(FuncCall("printInt", [Identifier("j")]))
            ]))
        ]))
    ])
    expected = "134"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_110():
    '''multiple struct levels auto infer'''
    ast = Program([
        StructDecl("Inner", [MemberDecl(IntType(), "val")]),
        StructDecl("Outer", [MemberDecl(StructType("Inner"), "inner")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Outer"), "o", StructLiteral([StructLiteral([IntLiteral(99)])])),
            VarDecl(None, "v", MemberAccess(MemberAccess(Identifier("o"), "inner"), "val")),
            ExprStmt(FuncCall("printInt", [Identifier("v")]))
        ]))
    ])
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_111():
    '''auto infer with arithmetic operation float'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(None, "res", BinaryOp(FloatLiteral(3.14), "*", IntLiteral(2))),
            ExprStmt(FuncCall("printFloat", [Identifier("res")]))
        ]))
    ])
    expected = "6.28"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_112():
    '''boolean logical operations with ints'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(1), "&&", IntLiteral(0))])),
            ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(1), "||", IntLiteral(0))]))
        ]))
    ])
    expected = "01"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_113():
    '''prefix and postfix decrement'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(10)),
            ExprStmt(FuncCall("printInt", [PrefixOp("--", Identifier("x"))])),
            ExprStmt(FuncCall("printInt", [PostfixOp("--", Identifier("x"))])),
            ExprStmt(FuncCall("printInt", [Identifier("x")]))
        ]))
    ])
    expected = "998"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_114():
    '''function taking struct and returning primitive'''
    ast = Program([
        StructDecl("Data", [MemberDecl(IntType(), "x")]),
        FuncDecl(IntType(), "process", [Param(StructType("Data"), "d")], BlockStmt([
            ReturnStmt(BinaryOp(MemberAccess(Identifier("d"), "x"), "*", IntLiteral(2)))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Data"), "d", StructLiteral([IntLiteral(5)])),
            ExprStmt(FuncCall("printInt", [FuncCall("process", [Identifier("d")])]))
        ]))
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_115():
    '''assignment expression in struct member'''
    ast = Program([
        StructDecl("Data", [MemberDecl(IntType(), "x")]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Data"), "d", StructLiteral([IntLiteral(0)])),
            VarDecl(IntType(), "y", AssignExpr(MemberAccess(Identifier("d"), "x"), IntLiteral(15))),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("d"), "x")])),
            ExprStmt(FuncCall("printInt", [Identifier("y")]))
        ]))
    ])
    expected = "1515"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_116():
    '''logical short circuiting assignment'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(0)),
            ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(0), "&&", AssignExpr(Identifier("x"), IntLiteral(1)))])),
            ExprStmt(FuncCall("printInt", [Identifier("x")]))
        ]))
    ])
    expected = "00"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_117():
    '''implicit void return'''
    ast = Program([
        FuncDecl(None, "proc", [], BlockStmt([
            ExprStmt(FuncCall("printString", [StringLiteral("Hello")]))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("proc", []))
        ]))
    ])
    expected = "Hello"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_118():
    '''switch case fallthrough'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(1)),
            SwitchStmt(Identifier("x"), [
                CaseStmt(IntLiteral(1), [ExprStmt(FuncCall("printInt", [IntLiteral(1)]))]),
                CaseStmt(IntLiteral(2), [ExprStmt(FuncCall("printInt", [IntLiteral(2)])), BreakStmt()])
            ], None)
        ]))
    ])
    expected = "12"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_119():
    '''modulus operation'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(10), "%", IntLiteral(3))])),
            ExprStmt(FuncCall("printInt", [BinaryOp(IntLiteral(15), "%", IntLiteral(4))]))
        ]))
    ])
    expected = "13"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_120():
    '''complex expression with all ops'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(1)),
            VarDecl(IntType(), "y", IntLiteral(2)),
            VarDecl(IntType(), "res", BinaryOp(BinaryOp(Identifier("x"), "+", Identifier("y")), "*", IntLiteral(3))),
            ExprStmt(FuncCall("printInt", [Identifier("res")]))
        ]))
    ])
    expected = "9"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_121():
    '''readInt and printInt with space separation'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", FuncCall("readInt", [])),
            VarDecl(IntType(), "y", FuncCall("readInt", [])),
            ExprStmt(FuncCall("printInt", [Identifier("x")])),
            ExprStmt(FuncCall("printInt", [Identifier("y")]))
        ]))
    ])
    expected = "42100"
    result = CodeGenerator().generate_and_run(ast, input_data="42 100")
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_122():
    '''readFloat and printFloat with newline separation'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(FloatType(), "x", FuncCall("readFloat", [])),
            VarDecl(FloatType(), "y", FuncCall("readFloat", [])),
            ExprStmt(FuncCall("printFloat", [Identifier("x")])),
            ExprStmt(FuncCall("printFloat", [Identifier("y")]))
        ]))
    ])
    expected = "3.142.71"
    result = CodeGenerator().generate_and_run(ast, input_data="3.14\n2.71")
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_123():
    '''readString with space and newline'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StringType(), "s1", FuncCall("readString", [])),
            VarDecl(StringType(), "s2", FuncCall("readString", [])),
            ExprStmt(FuncCall("printString", [Identifier("s1")])),
            ExprStmt(FuncCall("printString", [Identifier("s2")]))
        ]))
    ])
    expected = "HelloWorld"
    result = CodeGenerator().generate_and_run(ast, input_data="Hello\nWorld")
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_124():
    '''Mutual recursion: is_even and is_odd'''
    ast = Program([
        FuncDecl(IntType(), "is_odd", [Param(IntType(), "n")], BlockStmt([
            IfStmt(BinaryOp(Identifier("n"), "==", IntLiteral(0)), ReturnStmt(IntLiteral(0)), None),
            ReturnStmt(FuncCall("is_even", [BinaryOp(Identifier("n"), "-", IntLiteral(1))]))
        ])),
        FuncDecl(IntType(), "is_even", [Param(IntType(), "n")], BlockStmt([
            IfStmt(BinaryOp(Identifier("n"), "==", IntLiteral(0)), ReturnStmt(IntLiteral(1)), None),
            ReturnStmt(FuncCall("is_odd", [BinaryOp(Identifier("n"), "-", IntLiteral(1))]))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("is_even", [IntLiteral(4)])])),
            ExprStmt(FuncCall("printInt", [FuncCall("is_odd", [IntLiteral(4)])]))
        ]))
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_125():
    '''Read number and compute factorial recursively'''
    ast = Program([
        FuncDecl(IntType(), "fact", [Param(IntType(), "n")], BlockStmt([
            IfStmt(BinaryOp(Identifier("n"), "<=", IntLiteral(1)), ReturnStmt(IntLiteral(1)), None),
            ReturnStmt(BinaryOp(Identifier("n"), "*", FuncCall("fact", [BinaryOp(Identifier("n"), "-", IntLiteral(1))])))
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "n", FuncCall("readInt", [])),
            ExprStmt(FuncCall("printInt", [FuncCall("fact", [Identifier("n")])]))
        ]))
    ])
    expected = "120"
    result = CodeGenerator().generate_and_run(ast, input_data="5")
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_126():
    '''Switch fall-through with variable usage'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(0)),
            SwitchStmt(IntLiteral(1), [
                CaseStmt(IntLiteral(1), [
                    ExprStmt(AssignExpr(Identifier("x"), IntLiteral(10)))
                ]),
                CaseStmt(IntLiteral(2), [
                    ExprStmt(AssignExpr(Identifier("x"), BinaryOp(Identifier("x"), "+", IntLiteral(5))))
                ]),
                CaseStmt(IntLiteral(3), [
                    ExprStmt(FuncCall("printInt", [Identifier("x")]))
                ])
            ], None)
        ]))
    ])
    expected = "15"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_127():
    '''Switch fall-through starting from middle case to default'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "out", IntLiteral(0)),
            SwitchStmt(IntLiteral(2), [
                CaseStmt(IntLiteral(1), [
                    ExprStmt(AssignExpr(Identifier("out"), BinaryOp(Identifier("out"), "+", IntLiteral(10))))
                ]),
                CaseStmt(IntLiteral(2), [
                    ExprStmt(AssignExpr(Identifier("out"), BinaryOp(Identifier("out"), "+", IntLiteral(20))))
                ]),
                CaseStmt(IntLiteral(3), [
                    ExprStmt(AssignExpr(Identifier("out"), BinaryOp(Identifier("out"), "+", IntLiteral(30))))
                ])
            ], DefaultStmt([
                ExprStmt(AssignExpr(Identifier("out"), BinaryOp(Identifier("out"), "+", IntLiteral(40))))
            ])),
            ExprStmt(FuncCall("printInt", [Identifier("out")]))
        ]))
    ])
    expected = "90"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_128():
    '''Switch fall-through printing multiple times sequentially'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            SwitchStmt(IntLiteral(1), [
                CaseStmt(IntLiteral(1), [
                    ExprStmt(FuncCall("printString", [StringLiteral("A")]))
                ]),
                CaseStmt(IntLiteral(2), [
                    ExprStmt(FuncCall("printString", [StringLiteral("B")]))
                ]),
                CaseStmt(IntLiteral(3), [
                    ExprStmt(FuncCall("printString", [StringLiteral("C")]))
                ])
            ], DefaultStmt([
                ExprStmt(FuncCall("printString", [StringLiteral("D")]))
            ]))
        ]))
    ])
    expected = "ABCD"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_129():
    '''Switch inside loop, break from switch doesn't break loop'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ForStmt(VarDecl(IntType(), "i", IntLiteral(1)), BinaryOp(Identifier("i"), "<=", IntLiteral(3)), PostfixOp("++", Identifier("i")), BlockStmt([
                SwitchStmt(Identifier("i"), [
                    CaseStmt(IntLiteral(1), [
                        ExprStmt(FuncCall("printString", [StringLiteral("O")]))
                    ]),
                    CaseStmt(IntLiteral(2), [
                        ExprStmt(FuncCall("printString", [StringLiteral("T")])),
                        BreakStmt()
                    ]),
                    CaseStmt(IntLiteral(3), [
                        ExprStmt(FuncCall("printString", [StringLiteral("H")]))
                    ])
                ], None)
            ]))
        ]))
    ])
    expected = "OTTH"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_130():
    '''Switch fall-through with nested block shadowing'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(IntType(), "x", IntLiteral(0)),
            SwitchStmt(IntLiteral(1), [
                CaseStmt(IntLiteral(1), [
                    BlockStmt([
                        VarDecl(IntType(), "x", IntLiteral(10)),
                        ExprStmt(FuncCall("printInt", [Identifier("x")]))
                    ])
                ]),
                CaseStmt(IntLiteral(2), [
                    ExprStmt(FuncCall("printInt", [Identifier("x")]))
                ])
            ], None)
        ]))
    ])
    expected = "100"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_131():
    '''Switch fall-through with variable declaration in case and usage in later case'''
    ast = Program([
        FuncDecl(VoidType(), "main", [], BlockStmt([
            SwitchStmt(IntLiteral(1), [
                CaseStmt(IntLiteral(1), [
                    VarDecl(IntType(), "x", IntLiteral(0))
                ]),
                CaseStmt(IntLiteral(2), [
                    ExprStmt(AssignExpr(Identifier("x"), IntLiteral(5)))
                ]),
                CaseStmt(IntLiteral(3), [
                    ExprStmt(FuncCall("printInt", [Identifier("x")]))
                ])
            ], None)
        ]))
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_132():
    '''Switch with returns in cases'''
    ast = Program([
        FuncDecl(IntType(), "f", [], BlockStmt([
            SwitchStmt(IntLiteral(1), [
                CaseStmt(IntLiteral(0), [ReturnStmt(IntLiteral(0))]),
                CaseStmt(IntLiteral(1), [ReturnStmt(IntLiteral(1))]),
                CaseStmt(IntLiteral(2), [ReturnStmt(IntLiteral(2))])
            ], None)
        ])),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            ExprStmt(FuncCall("printInt", [FuncCall("f", [])]))
        ]))
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"

def test_133():
    '''Prefix vs postfix decrement in while loops'''
    ast = Program([
        FuncDecl(
            VoidType(),
            "main",
            [],
            BlockStmt([
                VarDecl(IntType(), "x", IntLiteral(5)),
                WhileStmt(
                    PrefixOp("--", Identifier("x")),
                    ExprStmt(FuncCall("printInt", [Identifier("x")]))
                ),
                ExprStmt(AssignExpr(Identifier("x"), IntLiteral(5))),
                WhileStmt(
                    PostfixOp("--", Identifier("x")),
                    ExprStmt(FuncCall("printInt", [Identifier("x")]))
                ),
            ])
        )
    ])
    expected = "432143210"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_134():
    '''Bubble sort on 7-element array using struct fields'''
    ast = Program([
        StructDecl("Array7", [
            MemberDecl(IntType(), "v0"),
            MemberDecl(IntType(), "v1"),
            MemberDecl(IntType(), "v2"),
            MemberDecl(IntType(), "v3"),
            MemberDecl(IntType(), "v4"),
            MemberDecl(IntType(), "v5"),
            MemberDecl(IntType(), "v6"),
        ]),
        FuncDecl(VoidType(), "main", [], BlockStmt([
            VarDecl(StructType("Array7"), "arr", StructLiteral([
                IntLiteral(3), IntLiteral(1), IntLiteral(4), IntLiteral(1),
                IntLiteral(5), IntLiteral(9), IntLiteral(2),
            ])),
            VarDecl(IntType(), "t", None),
            ForStmt(
                VarDecl(IntType(), "i", IntLiteral(0)),
                BinaryOp(Identifier("i"), "<", IntLiteral(6)),
                PostfixOp("++", Identifier("i")),
                BlockStmt([
                    ForStmt(
                        VarDecl(IntType(), "j", IntLiteral(0)),
                        BinaryOp(Identifier("j"), "<", BinaryOp(IntLiteral(6), "-", Identifier("i"))),
                        PostfixOp("++", Identifier("j")),
                        BlockStmt([
                            IfStmt(
                                BinaryOp(
                                    BinaryOp(Identifier("j"), "==", IntLiteral(0)),
                                    "&&",
                                    BinaryOp(MemberAccess(Identifier("arr"), "v0"), ">", MemberAccess(Identifier("arr"), "v1"))
                                ),
                                BlockStmt([
                                    ExprStmt(AssignExpr(Identifier("t"), MemberAccess(Identifier("arr"), "v0"))),
                                    ExprStmt(AssignExpr(MemberAccess(Identifier("arr"), "v0"), MemberAccess(Identifier("arr"), "v1"))),
                                    ExprStmt(AssignExpr(MemberAccess(Identifier("arr"), "v1"), Identifier("t"))),
                                ]),
                                None
                            ),
                            IfStmt(
                                BinaryOp(
                                    BinaryOp(Identifier("j"), "==", IntLiteral(1)),
                                    "&&",
                                    BinaryOp(MemberAccess(Identifier("arr"), "v1"), ">", MemberAccess(Identifier("arr"), "v2"))
                                ),
                                BlockStmt([
                                    ExprStmt(AssignExpr(Identifier("t"), MemberAccess(Identifier("arr"), "v1"))),
                                    ExprStmt(AssignExpr(MemberAccess(Identifier("arr"), "v1"), MemberAccess(Identifier("arr"), "v2"))),
                                    ExprStmt(AssignExpr(MemberAccess(Identifier("arr"), "v2"), Identifier("t"))),
                                ]),
                                None
                            ),
                            IfStmt(
                                BinaryOp(
                                    BinaryOp(Identifier("j"), "==", IntLiteral(2)),
                                    "&&",
                                    BinaryOp(MemberAccess(Identifier("arr"), "v2"), ">", MemberAccess(Identifier("arr"), "v3"))
                                ),
                                BlockStmt([
                                    ExprStmt(AssignExpr(Identifier("t"), MemberAccess(Identifier("arr"), "v2"))),
                                    ExprStmt(AssignExpr(MemberAccess(Identifier("arr"), "v2"), MemberAccess(Identifier("arr"), "v3"))),
                                    ExprStmt(AssignExpr(MemberAccess(Identifier("arr"), "v3"), Identifier("t"))),
                                ]),
                                None
                            ),
                            IfStmt(
                                BinaryOp(
                                    BinaryOp(Identifier("j"), "==", IntLiteral(3)),
                                    "&&",
                                    BinaryOp(MemberAccess(Identifier("arr"), "v3"), ">", MemberAccess(Identifier("arr"), "v4"))
                                ),
                                BlockStmt([
                                    ExprStmt(AssignExpr(Identifier("t"), MemberAccess(Identifier("arr"), "v3"))),
                                    ExprStmt(AssignExpr(MemberAccess(Identifier("arr"), "v3"), MemberAccess(Identifier("arr"), "v4"))),
                                    ExprStmt(AssignExpr(MemberAccess(Identifier("arr"), "v4"), Identifier("t"))),
                                ]),
                                None
                            ),
                            IfStmt(
                                BinaryOp(
                                    BinaryOp(Identifier("j"), "==", IntLiteral(4)),
                                    "&&",
                                    BinaryOp(MemberAccess(Identifier("arr"), "v4"), ">", MemberAccess(Identifier("arr"), "v5"))
                                ),
                                BlockStmt([
                                    ExprStmt(AssignExpr(Identifier("t"), MemberAccess(Identifier("arr"), "v4"))),
                                    ExprStmt(AssignExpr(MemberAccess(Identifier("arr"), "v4"), MemberAccess(Identifier("arr"), "v5"))),
                                    ExprStmt(AssignExpr(MemberAccess(Identifier("arr"), "v5"), Identifier("t"))),
                                ]),
                                None
                            ),
                            IfStmt(
                                BinaryOp(
                                    BinaryOp(Identifier("j"), "==", IntLiteral(5)),
                                    "&&",
                                    BinaryOp(MemberAccess(Identifier("arr"), "v5"), ">", MemberAccess(Identifier("arr"), "v6"))
                                ),
                                BlockStmt([
                                    ExprStmt(AssignExpr(Identifier("t"), MemberAccess(Identifier("arr"), "v5"))),
                                    ExprStmt(AssignExpr(MemberAccess(Identifier("arr"), "v5"), MemberAccess(Identifier("arr"), "v6"))),
                                    ExprStmt(AssignExpr(MemberAccess(Identifier("arr"), "v6"), Identifier("t"))),
                                ]),
                                None
                            ),
                        ])
                    )
                ])
            ),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("arr"), "v0")])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("arr"), "v1")])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("arr"), "v2")])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("arr"), "v3")])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("arr"), "v4")])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("arr"), "v5")])),
            ExprStmt(FuncCall("printInt", [MemberAccess(Identifier("arr"), "v6")])),
        ]))
    ])
    expected = "1123459"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


from tests.utils import ASTGenerator

def test_135():
    '''Prime number sieve for first 20 numbers'''
    source = """
    void main() {
        for (int n = 2; n <= 20; n++) {
            int is_prime = 1;
            for (int d = 2; d < n; d++) {
                if (n % d == 0) {
                    is_prime = 0;
                    break;
                }
            }
            if (is_prime) printInt(n);
        }
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "235711131719"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_136():
    '''Floor sqrt function using integer arithmetic'''
    source = """
    int sqrt(int n) {
        int i = 0;
        while (i * i <= n) {
            i++;
        }
        return i - 1;
    }

    void main() {
        printInt(sqrt(0));
        printInt(sqrt(1));
        printInt(sqrt(2));
        printInt(sqrt(5));
        printInt(sqrt(8));
        printInt(sqrt(16));
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "011224"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_137():
    '''Float sqrt using binary search'''
    source = """
    float sqrt(float n) {
        float low = 0.0;
        float high = n;
        if (high < 1.0) high = 1.0;
        float mid = 0.0;
        while (high - low > 0.0001) {
            mid = (low + high) / 2.0;
            if (mid * mid > n) {
                high = mid;
            } else {
                low = mid;
            }
        }
        return (low + high) / 2.0;
    }
    void main() {
        printFloat(sqrt(2.0));
        printFloat(sqrt(5.0));
        printFloat(sqrt(9.0));
        printFloat(sqrt(25.0));
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "1.41421512.2360612.99998864.9999714"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_138():
    '''Factorial, double factorial, and quick exponent'''
    source = """
    int fact(int n) {
        int result = 1;
        for (int i = 1; i <= n; i++) {
            result = result * i;
        }
        return result;
    }

    int dfact(int n) {
        int result = 1;
        for (int i = n; i > 0; i = i - 2) {
            result = result * i;
        }
        return result;
    }

    int qexp(int base, int exp) {
        int result = 1;
        while (exp > 0) {
            if (exp % 2 == 1) {
                result = result * base;
            }
            base = base * base;
            exp = exp / 2;
        }
        return result;
    }

    void main() {
        printInt(fact(5));
        printInt(dfact(5));
        printInt(qexp(2, 10));
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "120151024"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_139():
    '''Approximate pi using series with binary search sqrt'''
    source = """
    float sqrt(float n) {
        float low = 0.0;
        float high = n;
        if (high < 1.0) high = 1.0;
        float mid = 0.0;
        while (high - low > 0.0001) {
            mid = (low + high) / 2.0;
            if (mid * mid > n) {
                high = mid;
            } else {
                low = mid;
            }
        }
        return (low + high) / 2.0;
    }

    void main() {
        float sum = 0.0;
        int p3 = 1;
        for (int k = 0; k <= 10; k++) {
            int denom = p3 * (2 * k + 1);
            if (k % 2 == 0) {
                sum = sum + 1.0 / denom;
            } else {
                sum = sum - 1.0 / denom;
            }
            p3 = p3 * 3;
        }
        float pi = 2.0 * sqrt(3.0) * sum;
        printFloat(pi);
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "3.1415744"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_140():
    '''Codeforces 1989A'''
    source = """
    void solve() {
        int x = readInt();
        int y = readInt();
        if (y < -1) {
            printString("NO ");
            return;
        }
        printString("YES ");
    }

    void main() {
        int test = readInt();
        while (test--) {
            solve();
        }
    }
    """
    ast = ASTGenerator(source).generate()
    input_data = "5\n24 42\n-2 -1\n-1 -2\n0 -50\n15 0"
    expected = "YES YES NO NO YES"
    result = CodeGenerator().generate_and_run(ast, input_data)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_141():
    '''Type inference patterns combined'''
    source = """
    int calc() {
        auto x;
        float y = (x = 5) + 2.0;
        int z = y >= x++;
        return z;
    }

    void main() {
        auto a1 = 10;
        auto b1 = 3.14;
        auto c1 = a1 + b1;
        printFloat(c1);

        int flag = !!!1;
        float invert = - - -1.5;
        printInt(flag);
        printFloat(invert);

        int math = 10 % (-2.0 != 3.14);
        printInt(math);

        auto a2 = 5;
        float b2 = a2 + 1.5;
        printFloat(b2);

        auto counter = 0;
        counter++;
        ++counter;
        printInt(counter);

        printInt(calc());
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "13.140-1.506.521"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_142():
    '''Return type inference patterns combined'''
    source = """
    pick(int x) {
        if (x) { return 10; }
        return 20;
    }

    add(int a, float b) {
        return a + b;
    }

    fact(int n) {
        if (n <= 1) { return 1.0; }
        return n * fact(n - 1);
    }

    void main() {
        printInt(pick(0));
        printInt(pick(1));
        printFloat(add(1, 2.0));
        printFloat(fact(5));
    }
    """
    ast = ASTGenerator(source).generate()
    expected = "20103.0120.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected '{expected}', got '{result}'"


def test_143():
    source = '''
    void main() {
        int x = 10;
        while (x--) int x = 5;
        printInt(x);

        for (; x < 5; ++x) {
            int x = 3;
        }
        printInt(x);
    }
    '''
    expected = "-15"
    ast = ASTGenerator(source).generate()
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected