from classes.token import TokenVariant
from typing import Any, Optional


class ASTnode:
    ...

# TODO: Urobit enum na AST nodes a nemusis pouzit isinstance alebo dat TokenVariant ( asi skor nie )
# TODO: Skus potom pred alokovat pamata na SIZE a urob testy
class Program(ASTnode):
    def __init__(self):
        self.statements: list = []


class AssignmentStatement(ASTnode):
    def __init__(self):
        self.name: ASTnode
        self.value: ASTnode


class IfStatement(ASTnode):
    def __init__(self):
        self.condition: Optional[ASTnode] = None
        self.statements: list = []
        self.else_statements: list = []


class WhileStatement(ASTnode):
    def __init__(self):
        self.condition: ASTnode
        self.statements: list = []


class BinaryOperation(ASTnode):
    def __init__(self, left_operand: ASTnode, right_operand: ASTnode, operator: TokenVariant):
        self.left_operand: ASTnode = left_operand
        self.operator: TokenVariant = operator
        self.right_operand: ASTnode = right_operand


class UnaryOperation(ASTnode):
    def __init__(self, operator: TokenVariant, operand: ASTnode):
        self.operator: TokenVariant = operator
        self.operand: ASTnode = operand


class Literal(ASTnode):
    def __init__(self, token_variant: TokenVariant, value: Any):
        self.type: TokenVariant = token_variant
        self.value: Any = value


class Variable(ASTnode):
    def __init__(self, value: str):
        self.value: str = value

