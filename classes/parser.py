from classes.scanner import Scanner, TokenVariant
from classes.token import Token
from classes.errors import UnexpectedTokenException
from classes.nodes import *
from typing import Optional


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner: Scanner = scanner
        self.current_token: Optional[Token] = None
        self.next_token: Optional[Token] = self.scanner.get_token()

    def eat(self, expected_token: TokenVariant) -> None:
        self.current_token = self.next_token

        if self.current_token.token_variant != expected_token:
            raise UnexpectedTokenException(
                message = "Expected token: '{expected}' but '{given}' was given".format(
                    expected = expected_token.value[0],
                    given = self.current_token.token_variant.value[0],
                )
            )

        self.next_token = self.scanner.get_token()

    def peek(self) -> Token:
        return self.next_token

    def create_integer_literal_node(self) -> ASTnode:
        return Literal(
            token_variant = TokenVariant.T_INTEGER,
            value = int(self.current_token.value)
        )

    def create_float_literal_node(self) -> ASTnode:
        return Literal(
            token_variant = TokenVariant.T_FLOAT,
            value = float(self.current_token.value)
        )

    def create_boolean_literal_node(self) -> ASTnode:
        return Literal(
            token_variant = TokenVariant.T_FLOAT,
            value = 'true' == self.current_token.value
        )

    def create_unary_operation_node(self) -> ASTnode:
        return UnaryOperation(
            operator = self.current_token.value,
            operand = self.parse_factor()
        )

    def create_variable(self) -> ASTnode:
        return Variable(
            value = self.current_token.value
        )

    def parse_factor(self) -> ASTnode:
        match self.next_token.token_variant:
            case TokenVariant.T_INTEGER:
                self.eat(TokenVariant.T_INTEGER)
                return self.create_integer_literal_node()
            case TokenVariant.T_FLOAT:
                self.eat(TokenVariant.T_FLOAT)
                return self.create_float_literal_node()
            case TokenVariant.T_BOOLEAN:
                self.eat(TokenVariant.T_BOOLEAN)
                return self.create_boolean_literal_node()
            case TokenVariant.T_MINUS:
                self.eat(TokenVariant.T_MINUS)
                return self.create_unary_operation_node()
            case TokenVariant.T_PLUS:
                self.eat(TokenVariant.T_PLUS)
                return self.create_unary_operation_node()
            case TokenVariant.T_LEFT_P:
                self.eat(TokenVariant.T_LEFT_P)
                node = self.parser_expression()
                self.eat(TokenVariant.T_RIGHT_P)
                return node
            case _:
                node = self.create_variable()
                return node

    def parse_term(self) -> ASTnode:
        return self.parse_factor()

    def parser_expression(self) -> ASTnode:
        return self.parse_term()

    def parse_program(self) -> ASTnode:
        self.eat(TokenVariant.T_PROGRAM)
        root = self.parse_statements()
        return root

    def parse_assignment(self) -> ASTnode:
        self.eat(TokenVariant.T_IDENTIFIER)
        node = AssignmentStatement()

        node.name = self.create_variable()
        self.eat(TokenVariant.T_ASSIGN)

        node.value = self.parser_expression()
        return node

    def parse_statements(self) -> ASTnode:
        root = Program()

        while self.current_token.token_variant != TokenVariant.T_EOF:
            token = self.peek()

            match token.token_variant:
                case TokenVariant.T_IDENTIFIER:
                    statement = self.parse_assignment()
                    root.statements.append()

        return root


