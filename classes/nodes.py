from classes.token import TokenVariant
from typing import Any

class ASTnode:
    ...


# TODO: Skus potom pred alokovat pamata na SIZE a urob testy
class Program(ASTnode):
    def __init__(self):
        self.statements: list = []


class AssignmentStatement(ASTnode):
    def __init__(self):
        self.name: str
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
    def __init__(self):
        self.operand: ASTnode
        self.operator: str

class Literal(ASTnode):
    def __init__(self):
        self.type: TokenVariant
        self.value: Any