from classes.node_visitor import VisitorInterpreter
from classes.nodes import *


class Interpreter(VisitorInterpreter):
    def __init__(self, root: Program):
        self.root: Program = root
        self.variables = {}

    def __str__(self):
        pass

    def evaluate_program(self, node: Program) -> None:
        self.evaluate(node.block)

    def evaluate_assignment_statement(self, node: AssignmentStatement) -> None:
        self.variables[node.name.value] = self.evaluate(node.value)

    def evaluate_variable(self, node: Variable) -> bool:
        return self.variables[node.value]

    def evaluate_literal(self, node: Literal) -> None:
        return node.value

    def evaluate_if_statement(self, node: IfStatement) -> None:
        condition = self.evaluate(node.condition)
        if condition:
            self.evaluate(node.block)
        else:
            if node.else_block:
                self.evaluate(node.else_block)

    def evaluate_else_statement(self, node: ElseStatement) -> None:
        self.evaluate(node.block)

    def evaluate_binary_operation(self, node: BinaryOperation):
        match node.operator:
            case TokenVariant.T_PLUS:
                return self.evaluate(node.left_operand) + self.evaluate(node.right_operand)
            case TokenVariant.T_MINUS:
                return self.evaluate(node.left_operand) - self.evaluate(node.right_operand)
            case TokenVariant.T_MULTIPLICATION:
                return self.evaluate(node.left_operand) * self.evaluate(node.right_operand)
            case TokenVariant.T_DIVISION:
                return self.evaluate(node.left_operand) / self.evaluate(node.right_operand)
            case TokenVariant.T_DIV:
                return self.evaluate(node.left_operand) // self.evaluate(node.right_operand)
            case TokenVariant.T_MODULO:
                return self.evaluate(node.left_operand) % self.evaluate(node.right_operand)
            case TokenVariant.T_LESS:
                return self.evaluate(node.left_operand) < self.evaluate(node.right_operand)
            case TokenVariant.T_LESS_EQUAL:
                return self.evaluate(node.left_operand) <= self.evaluate(node.right_operand)
            case TokenVariant.T_GREATER:
                return self.evaluate(node.left_operand) > self.evaluate(node.right_operand)
            case TokenVariant.T_GREATER_EQUAL:
                return self.evaluate(node.left_operand) >= self.evaluate(node.right_operand)
            case TokenVariant.T_EQUAL:
                return self.evaluate(node.left_operand) == self.evaluate(node.right_operand)
            case TokenVariant.T_NOT_EQUAL:
                return self.evaluate(node.left_operand) != self.evaluate(node.right_operand)

    def evaluate_unary_operation(self, node: UnaryOperation) -> None:
        match node.operator:
            case TokenVariant.T_PLUS:
                return +self.evaluate(node.operand)
            case TokenVariant.T_MINUS:
                return -self.evaluate(node.operand)

    def evaluate_while_statement(self, node: WhileStatement) -> None:
        condition = self.evaluate(node.condition)
        while condition:
            self.evaluate(node.block)
            condition = self.evaluate(node.condition)

    def evaluate_print_statement(self, node: PrintStatement) -> None:
        result = self.evaluate(node.value)
        print(result)

    def evaluate_condition(self, node: Condition) -> None:
        return self.evaluate(node.value)

    def evaluate_block(self, node: Block) -> None:
        for statement in node.statements:
            self.evaluate(statement)

    def start_evaluation(self) -> None:
        self.evaluate(self.root)
