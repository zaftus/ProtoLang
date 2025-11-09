# compiler.py — compile AST to simple bytecode
from protolang.ast import *

class OpCode:
    CONST = 1
    ADD = 2
    SUB = 3
    MUL = 4
    DIV = 5
    POP = 6
    CALL = 7
    RETURN = 8

class Compiler:
    def __init__(self):
        self.instructions = bytearray()
        self.constants = []

    def _emit(self, opcode: int, operand: bytes = b''):
        self.instructions.append(opcode)
        if operand:
            self.instructions.extend(operand)

    def compile(self, node):
        if node is None:
            return
        if isinstance(node, Program):
            for s in node.statements:
                self.compile(s)
        elif isinstance(node, ExpressionStatement):
            self.compile(node.expression)
            self._emit(OpCode.POP)
        elif isinstance(node, IntegerLiteral):
            idx = len(self.constants)
            self.constants.append(node.value)
            # 2-byte index
            self._emit(OpCode.CONST, idx.to_bytes(2, 'big'))
        elif isinstance(node, ReturnStatement):
            self.compile(node.return_value)
            self._emit(OpCode.RETURN)
        elif isinstance(node, CallExpression):
            self.compile(node.function)
            for arg in node.arguments:
                self.compile(arg)
            self._emit(OpCode.CALL, len(node.arguments).to_bytes(1,'big'))
        else:
            # other nodes omitted for brevity
            pass

    def bytecode(self):
        return bytes(self.instructions), self.constants
