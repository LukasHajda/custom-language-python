class ASTnode:
    ...


# TODO: Skus potom pred alokovat pamata na SIZE a urob testy
class Program(ASTnode):
    def __init__(self):
        self.statements: list = []


class AssignmentStatement(ASTnode):
    def __init__(self, name: str, value: ASTnode):
        self.name: str = name
        self.value: ASTnode = value


class IfStatement(ASTnode):
    def __init__(self, condition: ASTnode):
        self.condition: ASTnode = condition
        self.statements: list = []
        self.else_statements: list = []


class WhileStatement(ASTnode):
    def __init__(self, condition: ASTnode):
        self.condition: ASTnode = condition
        self.statements: list = []


class BinaryOperation(ASTnode):
    def __init__(self, left_operand: ASTnode, operator: str, right_operand: ASTnode):
        self.left_operand: ASTnode = left_operand
        self.operator: str = operator
        self.right_operand: ASTnode = right_operand


class UnaryOperation(ASTnode):
    def __init__(self, operand: ASTnode, operator: str):
        self.operand: ASTnode = operand
        self.operator: str = operator