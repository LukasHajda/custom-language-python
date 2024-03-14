from classes.nodes import *
from classes.node_visitor import VisitorSemanticAnalyzer
from classes.scope import Scope
from classes.errors import UndeclaredVariable


class SemanticAnalyzer(VisitorSemanticAnalyzer):
    def __init__(self, root: Program):
        self.root: Program = root
        self.scope_level = 0
        self.scope_stack: deque = deque()
        self.current_scope: Optional[Scope] = None

    def __create_program_scope(self) -> Scope:
        self.scope_level += 1
        return Scope(
            level = self.scope_level,
            global_scope = self.scope_level == 1
        )

    def __add_new_scope(self, scope: Scope) -> None:
        self.scope_stack.append(scope)
        self.current_scope = scope

    def __exit_scope(self) -> None:
        if self.current_scope.global_scope:
            return
        self.scope_stack.pop()
        self.current_scope = self.scope_stack[-1]

    def __check_variable_in_scopes(self, variable: str) -> bool:
        for index in range(len(self.scope_stack) - 1, -1, -1):
            scope = self.scope_stack[index]

            if scope.lookup(variable):
                return True
        return False

    def visit_program(self, node: Program):
        self.visit(node.block)

    def visit_assignment_statement(self, node: AssignmentStatement):
        if not self.__check_variable_in_scopes(node.name.value):
            self.current_scope.add_variable(node.name)
        self.visit(node.value)

    def visit_variable(self, node: Variable) -> bool:
        if self.__check_variable_in_scopes(node.value):
            return True
        raise UndeclaredVariable(
            message = "Undeclared variable: '{variable}' at line {row} and column {column}".format(
                variable = node.value,
                row = node.row,
                column = node.column
            )
        )

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
        scope = self.__create_program_scope()
        self.__add_new_scope(scope)
        for statement in node.statements:
            self.visit(statement)
        self.__exit_scope()

    def check(self):
        try:
            self.visit(self.root)
        except UndeclaredVariable as exception:
            print(exception)
