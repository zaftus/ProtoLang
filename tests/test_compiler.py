from protolang.lexer import Lexer
from protolang.parser import Parser
from protolang.compiler import Compiler

def test_compile_const():
    src = '1;'
    l = Lexer(src)
    p = Parser(l)
    program = p.parse_program()
    c = Compiler()
    c.compile(program)
    instr, consts = c.bytecode()
    assert len(consts) == 1
