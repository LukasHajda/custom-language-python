from typing import Optional, Any
from classes.token import TokenVariant
from classes.errors import TypeErrorException


class DynamicSemanticAnalyzer:
    def check_and_evaluate(self,
                           operator: Any,
                           right: [str | bool | int | float | None],
                           left: Optional[str | bool | int | float] = None,
                           ):
        if left and right:
            if operator in [
                TokenVariant.T_PLUS, TokenVariant.T_MINUS,
                TokenVariant.T_MULTIPLICATION, TokenVariant.T_DIVISION,
                TokenVariant.T_MODULO, TokenVariant.T_DIV
            ]:
                return self.__evaluate_basic_binary_operation(left = left, right = right, operator = operator)

            if operator in [
                TokenVariant.T_LESS, TokenVariant.T_GREATER,
                TokenVariant.T_LESS_EQUAL, TokenVariant.T_GREATER_EQUAL,
            ]:
                return self.__evaluate_basic_compare(left = left, right = right, operator = operator)

            else:
                match operator:
                    case TokenVariant.T_EQUAL:
                        return left == right
                    case TokenVariant.T_NOT_EQUAL:
                        return left != right

        else:
            if operator in [
                TokenVariant.T_MINUS, TokenVariant.T_PLUS
            ]:
                return self.__evaluate_unary_operation(operand = right, operator = operator)

    def __evaluate_unary_operation(self, operand, operator) -> Any:
        if type(operand) not in [int, float]:
            raise TypeErrorException(
                message = "Nemozte pouzit unarny operator {operator} na typ ({type_1})".format(
                    operator = operator.value[1],
                    type_1 = type(operand).__name__,
                )
            )
        match operator:
            case TokenVariant.T_PLUS:
                return +operand
            case TokenVariant.T_MINUS:
                return -operand

    def __evaluate_basic_compare(self, left, right, operator) -> Any:
        if type(left) not in [int, float] or type(left) not in [int, float]:
            raise TypeErrorException(
                message = "Nemozte pouzit operator {operator} medzi typmi ({type_1}) a ({type_2})".format(
                    operator = operator.value[1],
                    type_1 = type(left).__name__,
                    type_2 = type(right).__name__
                )
            )

        match operator:
            case TokenVariant.T_LESS:
                return left < right
            case TokenVariant.T_GREATER:
                return left > right
            case TokenVariant.T_LESS_EQUAL:
                return left <= right
            case TokenVariant.T_GREATER_EQUAL:
                return left >= right

    def __evaluate_basic_binary_operation(self, left, right, operator) -> Any:
        if type(left) is not type(right):
            raise TypeErrorException(
                message = "Nemozte pouzit operator {operator} medzi typmi ({type_1}) a ({type_2})".format(
                    operator = operator.value[1],
                    type_1 = type(left).__name__,
                    type_2 = type(right).__name__
                )
            )
        match operator:
            case TokenVariant.T_PLUS:
                return left + right
            case TokenVariant.T_MINUS:
                return left - right
            case TokenVariant.T_MULTIPLICATION:
                return left * right
            case TokenVariant.T_DIVISION:
                return left / right
            case TokenVariant.T_DIV:
                return left // right
            case TokenVariant.T_MODULO:
                return left % right
