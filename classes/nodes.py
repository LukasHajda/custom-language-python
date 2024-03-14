from classes.token import TokenVariant
from typing import Any, Optional
from enum import Enum
from collections import deque


class NodeVariant(Enum):
    N_PROGRAM = 'program'
    N_ASSIGNMENT_STATEMENT = 'assignment_statement'
    N_IF_STATEMENT = 'if_statement'
    N_ELSE_STATEMENT = 'else_statement'
    N_WHILE_STATEMENT = 'while_statement'
    N_BINARY_OPERATION = 'binary_operation'
    N_UNARY_OPERATION = 'unary_operation'
    N_LITERAL = 'literal'
    N_VARIABLE = 'variable'
    N_CONDITION = 'condition'
    N_BLOCK = 'block'


class ASTnode:
    def __init__(self, node_variant: NodeVariant):
        self.type: NodeVariant = node_variant

    def __str__(self):
        return self.__class__.__name__


class Program(ASTnode):
    def __init__(self):
        super().__init__(NodeVariant.N_PROGRAM)
        self.block: Optional[Block] = None


class AssignmentStatement(ASTnode):
    def __init__(self):
        super().__init__(NodeVariant.N_ASSIGNMENT_STATEMENT)
        self.name: Optional[Variable] = None
        self.value: Optional[ASTnode] = None


class IfStatement(ASTnode):
    def __init__(self):
        super().__init__(NodeVariant.N_IF_STATEMENT)
        self.condition: Optional[Condition] = None
        self.block: Optional[Block] = None
        self.else_block: Optional[ElseStatement] = None


class ElseStatement(ASTnode):
    def __init__(self):
        super().__init__(NodeVariant.N_ELSE_STATEMENT)
        self.block: Optional[Block] = None


class WhileStatement(ASTnode):
    def __init__(self):
        super().__init__(NodeVariant.N_WHILE_STATEMENT)
        self.condition: Optional[Condition] = None
        self.block: Optional[Block] = None


class BinaryOperation(ASTnode):
    def __init__(self, left_operand: ASTnode, right_operand: ASTnode, operator: TokenVariant):
        super().__init__(NodeVariant.N_BINARY_OPERATION)
        self.left_operand: ASTnode = left_operand
        self.operator: TokenVariant = operator
        self.right_operand: ASTnode = right_operand


class UnaryOperation(ASTnode):
    def __init__(self, operator: TokenVariant, operand: ASTnode):
        super().__init__(NodeVariant.N_UNARY_OPERATION)
        self.operator: TokenVariant = operator
        self.operand: ASTnode = operand


class Literal(ASTnode):
    def __init__(self, token_variant: TokenVariant, value: Any):
        super().__init__(NodeVariant.N_LITERAL)
        self.token_type: TokenVariant = token_variant
        self.value: [int | str | float | bool] = value


class Variable(ASTnode):
    def __init__(self, value: str, row: int, column: int):
        super().__init__(NodeVariant.N_VARIABLE)
        self.value: str = value
        self.row: int = row
        self.column: int = column


class Condition(ASTnode):
    def __init__(self):
        super().__init__(NodeVariant.N_CONDITION)
        self.value: Optional[ASTnode] = None


class Block(ASTnode):
    def __init__(self):
        super().__init__(NodeVariant.N_BLOCK)
        self.statements: deque = deque()
