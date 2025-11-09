# parser.py — Pratt-style parser for core expressions
from protolang.token import *
from protolang.ast import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.cur_token = None
        self.peek_token = None
        # prime tokens
        self._next_token(); self._next_token()

    def _next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self):
        program = Program([])
        while self.peek_token and self.peek_token.type != EOF:
            self._next_token()
            stmt = self._parse_statement()
            if stmt:
                program.statements.append(stmt)
        return program

    def _parse_statement(self):
        if self.cur_token.type == LET:
            return self._parse_let_statement()
        if self.cur_token.type == RETURN:
            return self._parse_return_statement()
        return self._parse_expression_statement()

    def _parse_let_statement(self):
        # assume next token is identifier
        name = Identifier(self.peek_token.literal)
        self._next_token()
        if self.peek_token.type == ASSIGN:
            self._next_token(); self._next_token()
            expr = self._parse_expression()
            if self.peek_token.type == SEMICOLON:
                self._next_token()
            return LetStatement(name, expr)
        else:
            raise SyntaxError('expected = after let')

    def _parse_return_statement(self):
        self._next_token()
        expr = self._parse_expression()
        if self.peek_token.type == SEMICOLON:
            self._next_token()
        return ReturnStatement(expr)

    def _parse_expression_statement(self):
        expr = self._parse_expression()
        if self.peek_token.type == SEMICOLON:
            self._next_token()
        return ExpressionStatement(expr)

    def _parse_expression(self):
        # simplistic: integer, ident, function, call, string, if
        t = self.cur_token
        if t is None:
            return None
        if t.type == INT:
            return IntegerLiteral(int(t.literal))
        if t.type == STRING:
            return StringLiteral(t.literal)
        if t.type == IDENT:
            return Identifier(t.literal)
        if t.type == FUNCTION:
            return self._parse_function_literal()
        if t.type == IF:
            return self._parse_if_expression()
        # more cases would be here (prefix/infix ops)
        return None

    def _parse_function_literal(self):
        # expects current token is FUNCTION and next is LPAREN
        if self.peek_token.type != LPAREN:
            raise SyntaxError('expected ( after fn')
        self._next_token()
        # read params
        params = []
        while self.peek_token.type != RPAREN:
            self._next_token()
            if self.cur_token.type == IDENT:
                params.append(Identifier(self.cur_token.literal))
            if self.peek_token.type == COMMA:
                self._next_token()
        self._next_token()
        # now body
        if self.peek_token.type == LBRACE:
            self._next_token(); self._next_token()
            body = BlockStatement([])
            while self.cur_token.type != RBRACE:
                stmt = self._parse_statement()
                if stmt: body.statements.append(stmt)
                self._next_token()
            return FunctionLiteral(params, body)
        raise SyntaxError('expected { for fn body')

    def _parse_if_expression(self):
        # very small; expects: if (cond) { ... } else { ... }
        if self.peek_token.type != LPAREN:
            raise SyntaxError('expected ( after if')
        self._next_token(); self._next_token()
        condition = self._parse_expression()
        if self.peek_token.type != RPAREN:
            raise SyntaxError('expected ) after condition')
        self._next_token();
        if self.peek_token.type != LBRACE:
            raise SyntaxError('expected { after )')
        self._next_token(); self._next_token()
        consequence = BlockStatement([])
        while self.cur_token.type != RBRACE:
            stmt = self._parse_statement()
            if stmt: consequence.statements.append(stmt)
            self._next_token()
        alternative = None
        if self.peek_token.type == ELSE:
            self._next_token(); self._next_token()
            if self.cur_token.type != LBRACE:
                raise SyntaxError('expected { after else')
            alt_block = BlockStatement([])
            while self.cur_token.type != RBRACE:
                stmt = self._parse_statement()
                if stmt: alt_block.statements.append(stmt)
                self._next_token()
            alternative = alt_block
        return IfExpression(condition, consequence, alternative)
