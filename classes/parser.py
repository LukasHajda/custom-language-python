from classes.scanner import Scanner, TokenVariant
from classes.token import Token
from classes.errors import UnexpectedTokenException
from classes.nodes import *
from typing import Optional


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner: Scanner = scanner
        self.current_token: Optional[Token] = self.scanner.next_token()

    def __eat(self, expected_token: TokenVariant) -> None:

        if self.current_token.token_variant != expected_token:
            raise UnexpectedTokenException(
                message = "Parsing Error. Expected token: '{expected}' but '{given}' was given".format(
                    expected = expected_token.value[0],
                    given = self.current_token.token_variant.value[0],
                )
            )

        self.current_token = self.scanner.next_token()

    def __peek(self) -> Token:
        return self.scanner.peek()

    def __create_integer_literal_node(self) -> ASTnode:
        node = Literal(
            token_variant = TokenVariant.T_INTEGER,
            value = int(self.current_token.value)
        )
        self.__eat(TokenVariant.T_INTEGER)
        return node

    def __create_float_literal_node(self) -> ASTnode:
        node = Literal(
            token_variant = TokenVariant.T_FLOAT,
            value = float(self.current_token.value)
        )

        self.__eat(TokenVariant.T_FLOAT)
        return node

    def __create_boolean_literal_node(self) -> ASTnode:
        # TODO: Tu musi byt nejaky raise exception.
        node = Literal(
            token_variant = TokenVariant.T_BOOLEAN,
            value = 'true' == self.current_token.value
        )

        self.__eat(TokenVariant.T_BOOLEAN)
        return node

    def __create_unary_operation_node(self) -> ASTnode:
        operator = self.current_token.token_variant
        self.__eat(self.current_token.token_variant)

        node = UnaryOperation(
            operator = operator,
            operand = self.__parse_factor()
        )

        return node

    def __create_variable(self) -> ASTnode:
        node = Variable(
            value = self.current_token.value
        )

        self.__eat(self.current_token.token_variant)
        return node

    def __parse_factor(self) -> ASTnode:
        match self.current_token.token_variant:
            case TokenVariant.T_INTEGER:
                return self.__create_integer_literal_node()
            case TokenVariant.T_FLOAT:
                return self.__create_float_literal_node()
            case TokenVariant.T_BOOLEAN:
                return self.__create_boolean_literal_node()
            case TokenVariant.T_MINUS:
                return self.__create_unary_operation_node()
            case TokenVariant.T_PLUS:
                return self.__create_unary_operation_node()
            case TokenVariant.T_LEFT_P:
                self.__eat(TokenVariant.T_LEFT_P)
                node = self.__parse_expression()
                self.__eat(TokenVariant.T_RIGHT_P)
                return node
            case _:
                node = self.__create_variable()
                return node

    def __parse_term(self) -> ASTnode:
        node = self.__parse_factor()

        while self.current_token.token_variant in (
            TokenVariant.T_MULTIPLICATION,
            TokenVariant.T_DIVISION,
            TokenVariant.T_DIV,
            TokenVariant.T_MODULO
        ):
            current_token = self.current_token.token_variant

            match current_token:
                case TokenVariant.T_MULTIPLICATION:
                    self.__eat(TokenVariant.T_MULTIPLICATION)
                case TokenVariant.T_DIVISION:
                    self.__eat(TokenVariant.T_DIVISION)
                case TokenVariant.T_DIV:
                    self.__eat(TokenVariant.T_DIV)
                case TokenVariant.T_MODULO:
                    self.__eat(TokenVariant.T_MODULO)

            node = BinaryOperation(
                left_operand = node,
                right_operand = self.__parse_factor(),
                operator = current_token
            )

        return node

    def __parse_expression(self) -> ASTnode:
        node = self.__parse_term()

        # TODO: mozno by bolo fajn zrusit `match` a dat tam iba self.current_token.token_variant
        while self.current_token.token_variant in (TokenVariant.T_PLUS, TokenVariant.T_MINUS):
            current_token = self.current_token.token_variant
            match self.current_token.token_variant:
                case TokenVariant.T_PLUS:
                    self.__eat(TokenVariant.T_PLUS)
                case TokenVariant.T_MINUS:
                    self.__eat(TokenVariant.T_MINUS)

            node = BinaryOperation(
                left_operand = node,
                right_operand = self.__parse_term(),
                operator = current_token
            )
        return node

    def __parse_condition(self) -> ASTnode:
        node = self.__parse_expression()

        while self.current_token.token_variant in (
            TokenVariant.T_EQUAL,
            TokenVariant.T_NOT_EQUAL,
            TokenVariant.T_LESS,
            TokenVariant.T_LESS_EQUAL,
            TokenVariant.T_GREATER,
            TokenVariant.T_GREATER_EQUAL
        ):
            current_token = self.current_token.token_variant

            match self.current_token.token_variant:
                case TokenVariant.T_EQUAL:
                    self.__eat(TokenVariant.T_EQUAL)
                case TokenVariant.T_NOT_EQUAL:
                    self.__eat(TokenVariant.T_NOT_EQUAL)
                case TokenVariant.T_LESS:
                    self.__eat(TokenVariant.T_LESS)
                case TokenVariant.T_LESS_EQUAL:
                    self.__eat(TokenVariant.T_LESS_EQUAL)
                case TokenVariant.T_GREATER:
                    self.__eat(TokenVariant.T_GREATER)
                case TokenVariant.T_GREATER_EQUAL:
                    self.__eat(TokenVariant.T_GREATER_EQUAL)

            node = BinaryOperation(
                left_operand = node,
                right_operand = self.__parse_term(),
                operator = current_token
            )

        return node

    def __parse_program(self) -> Program:
        root = Program()

        self.__eat(TokenVariant.T_PROGRAM)
        root.block = self.__parse_statements()
        return root

    def __parse_assignment(self) -> ASTnode:
        node = AssignmentStatement()

        node.name = self.__create_variable()

        self.__eat(TokenVariant.T_ASSIGN)

        node.value = self.__parse_expression()
        return node

    def __parse_else(self) -> ASTnode:
        self.__eat(TokenVariant.T_ELSE)
        self.__eat(TokenVariant.T_LEFT_CURLY_P)

        node = ElseStatement()
        node.block = self.__parse_statements()
        self.__eat(TokenVariant.T_RIGHT_CURLY_P)
        return node

    def __parse_if(self) -> ASTnode:
        node = IfStatement()

        self.__eat(TokenVariant.T_IF)
        self.__eat(TokenVariant.T_LEFT_P)

        node.condition = Condition()
        node.condition.value = self.__parse_condition()
        self.__eat(TokenVariant.T_RIGHT_P)
        self.__eat(TokenVariant.T_LEFT_CURLY_P)
        node.block = self.__parse_statements()

        self.__eat(TokenVariant.T_RIGHT_CURLY_P)

        if self.current_token.token_variant == TokenVariant.T_ELSE:
            node.else_block = self.__parse_else()

        return node

    def __parse_while(self) -> ASTnode:
        node = WhileStatement()

        self.__eat(TokenVariant.T_WHILE)
        self.__eat(TokenVariant.T_LEFT_P)

        node.condition = Condition()
        node.condition.value = self.__parse_condition()
        self.__eat(TokenVariant.T_RIGHT_P)
        self.__eat(TokenVariant.T_LEFT_CURLY_P)

        node.block = self.__parse_statements()

        self.__eat(TokenVariant.T_RIGHT_CURLY_P)

        return node

    def __parse_statements(self) -> ASTnode:
        block = Block()
        while self.current_token.token_variant != TokenVariant.T_EOF:

            match self.current_token.token_variant:
                case TokenVariant.T_IDENTIFIER:
                    statement = self.__parse_assignment()
                    block.statements.append(statement)
                    self.__eat(TokenVariant.T_DOT)
                case TokenVariant.T_IF:
                    statement = self.__parse_if()
                    block.statements.append(statement)
                case TokenVariant.T_WHILE:
                    statement = self.__parse_while()
                    block.statements.append(statement)
                case _:
                    # print(self.current_token)
                    break

        return block

    def parse(self) -> Program:
        return self.__parse_program()


