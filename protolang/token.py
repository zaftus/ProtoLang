# token.py — token types and helpers
from dataclasses import dataclass

@dataclass(frozen=True)
class Token:
    type: str
    literal: str
    line: int
    col: int

# token constants
EOF = 'EOF'
IDENT = 'IDENT'
INT = 'INT'
STRING = 'STRING'
ASSIGN = '='
PLUS = '+'
MINUS = '-'
BANG = '!'
ASTERISK = '*'
SLASH = '/'
LT = '<'
GT = '>'
COMMA = ','
SEMICOLON = ';'
LPAREN = '('
RPAREN = ')'
LBRACE = '{'
RBRACE = '}'
FUNCTION = 'FUNCTION'
LET = 'LET'
RETURN = 'RETURN'
TRUE = 'TRUE'
FALSE = 'FALSE'
IF = 'IF'
ELSE = 'ELSE'

keywords = {
    'fn': FUNCTION,
    'let': LET,
    'return': RETURN,
    'true': TRUE,
    'false': FALSE,
    'if': IF,
    'else': ELSE,
}

def lookup_ident(ident: str):
    return keywords.get(ident, IDENT)
