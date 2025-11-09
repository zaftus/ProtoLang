from protolang.lexer import Lexer
from protolang.parser import Parser

def test_parses_program():
    src = 'let a = 5;'
    l = Lexer(src)
    p = Parser(l)
    program = p.parse_program()
    assert len(program.statements) == 1
