# lexer.py — a small, robust lexer
from protolang.token import Token, EOF, IDENT, INT, STRING, lookup_ident

class Lexer:
    def __init__(self, input_text: str):
        self.input = input_text
        self.pos = 0
        self.read_pos = 0
        self.ch = ''
        self.line = 1
        self.col = 0
        self._read_char()

    def _read_char(self):
        if self.read_pos >= len(self.input):
            self.ch = ''
        else:
            self.ch = self.input[self.read_pos]
        self.pos = self.read_pos
        self.read_pos += 1
        if self.ch == '\n':
            self.line += 1
            self.col = 0
        else:
            self.col += 1

    def _peek_char(self):
        if self.read_pos >= len(self.input):
            return ''
        return self.input[self.read_pos]

    def next_token(self):
        self._skip_whitespace()
        if self.ch == '':
            tok = Token(EOF, '', self.line, self.col)
        elif self.ch == '"':
            literal = self._read_string()
            tok = Token(STRING, literal, self.line, self.col)
        elif self.ch.isalpha() or self.ch == '_':
            ident = self._read_identifier()
            tok_type = lookup_ident(ident)
            tok = Token(tok_type, ident, self.line, self.col)
            return tok
        elif self.ch.isdigit():
            num = self._read_number()
            tok = Token(INT, num, self.line, self.col)
            return tok
        else:
            ch = self.ch
            tok = Token(ch, ch, self.line, self.col)
        self._read_char()
        return tok

    def _skip_whitespace(self):
        while self.ch in (' ', '\t', '\n', '\r'):
            self._read_char()

    def _read_identifier(self):
        start = self.pos
        while self.ch.isalpha() or self.ch == '_' or self.ch.isdigit():
            self._read_char()
        return self.input[start:self.pos]

    def _read_number(self):
        start = self.pos
        while self.ch.isdigit():
            self._read_char()
        return self.input[start:self.pos]

    def _read_string(self):
        # consume opening quote
        self._read_char()
        start = self.pos
        while self.ch != '"' and self.ch != '':
            if self.ch == '\\':
                self._read_char()  # skip escape char
            self._read_char()
        s = self.input[start:self.pos]
        return s
