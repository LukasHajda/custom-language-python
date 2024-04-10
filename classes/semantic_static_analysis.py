from classes.nodes import *
from classes.node_visitor import VisitorSemanticAnalyzer
from classes.scope import Scope
from classes.errors import NameErrorException, TypeErrorException, DuplicateParameterException


class SemanticAnalyzer(VisitorSemanticAnalyzer):
    def __init__(self, root: Program):
        self.root: Program = root
        self.scope_level = 0
        self.scope_stack: deque = deque()
        self.current_scope: Optional[Scope] = None

    def __create_scope(self) -> Scope:
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

    def __check_variable_in_scopes(self, variable: str) -> Optional[Variable]:
        for index in range(len(self.scope_stack) - 1, -1, -1):
            scope = self.scope_stack[index]

            checked_variable = scope.lookup_variable(variable)
            if checked_variable:
                return checked_variable
        return None

    def __check_functions_in_scopes(self, function: str) -> Optional[FunctionDeclaration]:
        for index in range(len(self.scope_stack) - 1, -1, -1):
            scope = self.scope_stack[index]

            checked_function = scope.lookup_function(function)
            if checked_function:
                return checked_function
        return None

    def visit_program(self, node: Program) -> None:
        self.visit(node.block)

    def visit_print_statement(self, node: PrintStatement) -> None:
        self.visit(node.value)

    def visit_function_declaration(self, node: FunctionDeclaration) -> None:
        parameters_name = list(map(lambda param: param.value, node.parameter_list.parameters))

        if len(parameters_name) != len(set(parameters_name)):
            raise DuplicateParameterException(
                message = "Duplikovaný názov parametra vo funkcií ({function_name})".format(
                    function_name = node.name
                )
            )

        self.current_scope.add_function(node)
        self.visit(node.block)

    def visit_parameter_list(self, node: ParameterList) -> None:
        for parameter in node.parameters:
            if not self.__check_variable_in_scopes(parameter.value):
                self.current_scope.add_variable(parameter)

    def visit_function_call(self, node: FunctionCall) -> None:
        defined_function = self.__check_functions_in_scopes(node.name)

        if not defined_function:
            raise NameErrorException(
                message = "Názov: '{function_name}' nie je definovaná".format(
                    function_name = node.name,
                )
            )

        if len(defined_function.parameter_list.parameters) != len(node.argument_list.arguments):
            raise TypeErrorException(
                message = "{function_name}() prijíma {parameters} parametrov ale {actual} bolo predaných".format(
                    function_name = defined_function.name,
                    parameters = len(defined_function.parameter_list.parameters),
                    actual = len(node.argument_list.arguments)
                )
            )

        for argument in node.argument_list.arguments:
            self.visit(argument)

        node.block = defined_function.block
        node.parameter_list = defined_function.parameter_list

    def visit_argument(self, node: Argument) -> None:
        self.visit(node.value)

    def visit_assignment_statement(self, node: AssignmentStatement) -> None:
        if not self.__check_variable_in_scopes(node.name.value):
            self.current_scope.add_variable(node.name)
        self.visit(node.value)

    def visit_variable(self, node: Variable) -> bool:
        if self.__check_variable_in_scopes(node.value):
            return True
        raise NameErrorException(
            message = "Nedeklarovaná premenná: '{variable}' v riadku {row} a stĺpci {column}".format(
                variable = node.value,
                row = node.row,
                column = node.column
            )
        )

    def visit_literal(self, node: Literal) -> None:
        pass

    def visit_if_statement(self, node: IfStatement) -> None:
        self.visit(node.condition)
        self.visit(node.block)

        if node.else_block:
            self.visit(node.else_block)

    def visit_else_statement(self, node: ElseStatement) -> None:
        self.visit(node.block)

    def visit_binary_operation(self, node: BinaryOperation) -> None:
        self.visit(node.left_operand)
        self.visit(node.right_operand)

    def visit_unary_operation(self, node: UnaryOperation) -> None:
        self.visit(node.operand)

    def visit_while_statement(self, node: WhileStatement) -> None:
        self.visit(node.condition)
        self.visit(node.block)

    def visit_condition(self, node: Condition) -> None:
        self.visit(node.value)

    def visit_return_statement(self, node: ReturnStatement) -> None:
        self.visit(node.value)

    def visit_block(self, node: Block) -> None:
        scope = self.__create_scope()
        self.__add_new_scope(scope)
        for statement in node.statements:
            self.visit(statement)
        self.__exit_scope()

    def check(self) -> None:
        try:
            self.visit(self.root)
        except (NameErrorException, TypeErrorException) as exception:
            print(exception)
            exit(0)
