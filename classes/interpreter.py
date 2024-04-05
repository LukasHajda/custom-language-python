from classes.node_visitor import VisitorInterpreter
from classes.nodes import *
from classes.evaluation_record import EvaluationRecord
from classes.errors import Return


class Interpreter(VisitorInterpreter):
    def __init__(self, root: Program):
        self.root: Program = root
        self.evaluation_stack: deque[EvaluationRecord] = deque()
        self.current_evaluation: Optional[EvaluationRecord] = None

    def __check_variable_in_stack(self, variable: str) -> Optional[Variable]:
        for index in range(len(self.evaluation_stack) - 1, -1, -1):
            evaluation_record = self.evaluation_stack[index]

            checked_variable = evaluation_record.get_variable(variable)
            if checked_variable:
                return checked_variable
        return None

    def __check_function_in_stack(self, function: str) -> Optional[Any]:
        for index in range(len(self.evaluation_stack) - 1, -1, -1):
            evaluation_record = self.evaluation_stack[index]

            checked_function = evaluation_record.get_function(function)
            if checked_function:
                return checked_function
        return None

    def evaluate_program(self, node: Program) -> None:
        evaluation_record = EvaluationRecord('PROGRAM')
        self.evaluation_stack.append(evaluation_record)
        self.current_evaluation = evaluation_record
        self.evaluate(node.block)

        self.evaluation_stack.pop()

    def evaluate_assignment_statement(self, node: AssignmentStatement) -> None:
        self.current_evaluation.set_variable(node.name.value, self.evaluate(node.value))

    def evaluate_variable(self, node: Variable) -> Variable:
        return self.__check_variable_in_stack(node.value)

    def evaluate_literal(self, node: Literal) -> Any:
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

    def evaluate_condition(self, node: Condition) -> Any:
        return self.evaluate(node.value)

    def evaluate_parameter_list(self, node: ParameterList) -> None:
        pass

    def evaluate_return_statement(self, node: ReturnStatement) -> None:
        value = self.evaluate(node.value)
        raise Return(value)

    def evaluate_block(self, node: Block) -> None:
        for statement in node.statements:
            self.evaluate(statement)

    def evaluate_function_declaration(self, node: FunctionDeclaration) -> None:
        pass

    def evaluate_argument(self, node: Argument) -> Any:
        return self.evaluate(node.value)

    def evaluate_function_call(self, node: FunctionCall) -> None:
        parameters = node.parameter_list.parameters
        arguments = node.argument_list.arguments

        evaluation_record = EvaluationRecord(f"FUNKCIA {node.name}")

        for parameter, argument in zip(parameters, arguments):
            value = self.evaluate(argument)
            evaluation_record.set_variable(parameter.value, value)

        self.evaluation_stack.append(evaluation_record)
        self.current_evaluation = evaluation_record

        try:
            value = self.evaluate(node.block)
        except (Return, ) as exception:
            value = exception.value

        self.evaluation_stack.pop()
        self.current_evaluation = self.evaluation_stack[-1]

        return value

    def start_evaluation(self) -> None:
        self.evaluate(self.root)
