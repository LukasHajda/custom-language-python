from classes.nodes import *
from classes.node_visitor import NodeVisitor


class SemanticAnalyzer(NodeVisitor):
    def __init__(self, root: Program):
        self.root: Program = root

    def visit_program(self, node: Program):
        self.visit(node.block)

    def visit_assignment_statement(self, node: AssignmentStatement):
        self.visit(node.name)
        self.visit(node.value)

    def visit_variable(self, node: Variable):
        pass

    def visit_literal(self, node: Literal):
        pass

    def visit_if_statement(self, node: IfStatement):
        self.visit(node.condition)
        self.visit(node.block)

        if node.else_block:
            self.visit(node.else_block)

    def visit_else_statement(self, node: ElseStatement):
        self.visit(node.block)

    def visit_binary_operation(self, node: BinaryOperation):
        self.visit(node.left_operand)
        self.visit(node.right_operand)

    def visit_unary_operation(self, node: UnaryOperation):
        self.visit(node.operand)

    def visit_while_statement(self, node: WhileStatement):
        self.visit(node.condition)
        self.visit(node.block)

    def visit_condition(self, node: Condition):
        self.visit(node.value)

    def visit_block(self, node: Block):
        for statement in node.statements:
            self.visit(statement)

    # postorder traversal
    def __traverse_ast(self):
        self.visit(self.root)


    def check(self):
        self.__traverse_ast()
