from classes.token import TokenVariant
from typing import Any, Optional
from enum import Enum
from collections import deque


class NodeVariant(Enum):
    N_PROGRAM = 'program',
    N_ASSIGNMENT_STATEMENT = 'assignment',
    N_IF_STATEMENT = 'if',
    N_ELSE_STATEMENT = 'else',
    N_WHILE_STATEMENT = 'while',
    N_BINARY_OPERATION = 'binary_operation',
    N_UNARY_OPERATION = 'unary_operation',
    N_LITERAL = 'literal',
    N_VARIABLE = 'variable',
    N_CONDITION = 'condition'


class ASTnode:
    ...

# TODO: Skus potom pred alokovat pamata na SIZE a urob testy
class Program(ASTnode):
    def __init__(self):
        self.type: NodeVariant = NodeVariant.N_PROGRAM
        self.statements: deque = deque()


class AssignmentStatement(ASTnode):
    def __init__(self):
        self.type: NodeVariant = NodeVariant.N_ASSIGNMENT_STATEMENT
        self.name: Optional[Variable] = None
        self.value: Optional[ASTnode] = None


class IfStatement(ASTnode):
    def __init__(self):
        self.type: NodeVariant = NodeVariant.N_IF_STATEMENT
        self.condition: Optional[Condition] = None
        self.statements: deque = deque()
        self.else_statement: Optional[ElseStatement] = None


class ElseStatement(ASTnode):
    def __init__(self):
        self.type: NodeVariant = NodeVariant.N_ELSE_STATEMENT
        self.statements: deque = deque()


class WhileStatement(ASTnode):
    def __init__(self):
        self.type: NodeVariant = NodeVariant.N_WHILE_STATEMENT
        self.condition: Optional[Condition] = None
        self.statements: deque = deque()


class BinaryOperation(ASTnode):
    def __init__(self, left_operand: ASTnode, right_operand: ASTnode, operator: TokenVariant):
        self.type: NodeVariant = NodeVariant.N_BINARY_OPERATION
        self.left_operand: ASTnode = left_operand
        self.operator: TokenVariant = operator
        self.right_operand: ASTnode = right_operand


class UnaryOperation(ASTnode):
    def __init__(self, operator: TokenVariant, operand: ASTnode):
        self.type: NodeVariant = NodeVariant.N_UNARY_OPERATION
        self.operator: TokenVariant = operator
        self.operand: ASTnode = operand


class Literal(ASTnode):
    def __init__(self, token_variant: TokenVariant, value: Any):
        self.type: NodeVariant = NodeVariant.N_LITERAL
        self.token_type: TokenVariant = token_variant
        self.value: [int | str | float | bool] = value


class Variable(ASTnode):
    def __init__(self, value: str):
        self.type: NodeVariant = NodeVariant.N_VARIABLE
        self.value: str = value


class Condition(ASTnode):
    def __init__(self):
        self.type: NodeVariant = NodeVariant.N_CONDITION
        self.value: Optional[ASTnode] = None
