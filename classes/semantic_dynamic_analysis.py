from typing import Optional, Any
from classes.token import TokenVariant
from classes.errors import TypeErrorException


class DynamicSemanticAnalyzer:
    def check_and_evaluate_binary_operation(self,
                           operator: Any,
                           right: [str | bool | int | float | None],
                           left: Optional[str | bool | int | float] = None,
                           ):

        try:
            match operator:
                case TokenVariant.T_EQUAL:
                    return left == right
                case TokenVariant.T_NOT_EQUAL:
                    return left != right
                case TokenVariant.T_LESS:
                    return left < right
                case TokenVariant.T_GREATER:
                    return left > right
                case TokenVariant.T_LESS_EQUAL:
                    return left <= right
                case TokenVariant.T_GREATER_EQUAL:
                    return left >= right
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
        except (Exception, ) as _:
            raise TypeErrorException(
                message = "Nemôžete použiť operátor {operator} medzi typmi ({type_1}) a ({type_2})".format(
                    operator = operator.value[1],
                    type_1 = type(left).__name__ if left is not None else 'nic',
                    type_2 = type(right).__name__ if right is not None else 'nic'
                )
            )

    def check_and_evaluate_unary_operation(self, operand, operator):
        try:
            match operator:
                case TokenVariant.T_PLUS:
                    return +operand
                case TokenVariant.T_MINUS:
                    return -operand
        except (Exception, ) as _:
            raise TypeErrorException(
                message = "Nemôžete použiť unárny operator {operator} na typ ({type_1})".format(
                    operator = operator.value[1],
                    type_1 = type(operand).__name__ if operand is not None else 'nic',
                )
            )
