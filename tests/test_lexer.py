from protolang.lexer import Lexer
from protolang.token import INT, IDENT, EOF

def test_simple_tokens():
    src = 'let five = 5;'
    l = Lexer(src)
    toks = []
    while True:
        t = l.next_token()
        toks.append(t.type)
        if t.type == EOF: break
    assert IDENT in toks
    assert INT in toks
