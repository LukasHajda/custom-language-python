from classes.token import TokenVariant
from typing import Any

SIZE = 128


class ASTnode:
    ...


# TODO: Skus potom pred alokovat pamata na SIZE a urob testy
class Program(ASTnode):
    def __init__(self):
        self.statements: list = [None] * SIZE
        self.position: int = 0

    def add_statement(self, statement: ASTnode) -> None:
        self.statements[self.position] = statement


class AssignmentStatement(ASTnode):
    def __init__(self):
        self.name: ASTnode
        self.value: ASTnode


class IfStatement(ASTnode):
    def __init__(self):
        self.condition: ASTnode
        self.statements: list = []
        self.else_statements: list = []


class WhileStatement(ASTnode):
    def __init__(self):
        self.condition: ASTnode
        self.statements: list = []


class BinaryOperation(ASTnode):
    def __init__(self):
        self.left_operand: ASTnode
        self.operator: str
        self.right_operand: ASTnode


class UnaryOperation(ASTnode):
    def __init__(self, operator: str, operand: ASTnode):
        self.operator: str = operator
        self.operand: ASTnode = operand


class Literal(ASTnode):
    def __init__(self, token_variant: TokenVariant, value: Any):
        self.type: TokenVariant = token_variant
        self.value: Any = value


class Variable(ASTnode):
    def __init__(self, value: str):
        self.value: str = value

