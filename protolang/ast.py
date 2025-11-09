# ast.py — AST node definitions
from dataclasses import dataclass
from typing import List, Optional

class Node:
    pass

@dataclass
class Program(Node):
    statements: List[Node]

@dataclass
class LetStatement(Node):
    name: 'Identifier'
    value: Node

@dataclass
class ReturnStatement(Node):
    return_value: Node

@dataclass
class ExpressionStatement(Node):
    expression: Node

@dataclass
class Identifier(Node):
    value: str

@dataclass
class IntegerLiteral(Node):
    value: int

@dataclass
class StringLiteral(Node):
    value: str

@dataclass
class FunctionLiteral(Node):
    params: List[Identifier]
    body: 'BlockStatement'

@dataclass
class CallExpression(Node):
    function: Node
    arguments: List[Node]

@dataclass
class BlockStatement(Node):
    statements: List[Node]

@dataclass
class IfExpression(Node):
    condition: Node
    consequence: BlockStatement
    alternative: Optional[BlockStatement]
