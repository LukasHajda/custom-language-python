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

    def create_literal_node(self) -> ASTnode:


    def create_factor(self) -> ASTnode:
        match self.next_token.token_variant:
            case TokenVariant.T_INTEGER | TokenVariant.T_FLOAT | TokenVariant.T_BOOLEAN:
                self.eat(self.next_token.token_variant)
                return self.create_literal_node()

    def create_term(self) -> ASTnode:
        node = self.create_factor()
        return node

    def create_expression_node(self) -> ASTnode:
        node = self.create_term()
        return node

    def parse_program(self) -> ASTnode:
        self.eat(TokenVariant.T_PROGRAM)
        root = self.parse_statements()
        return root

    def parse_assignment(self) -> ASTnode:
        self.eat(TokenVariant.T_IDENTIFIER)
        node = AssignmentStatement()

        node.name = self.current_token.value
        self.eat(TokenVariant.T_ASSIGN)

        node.value = self.create_expression_node()
        return node

    def parse_statements(self) -> ASTnode:
        root = Program()

        while self.current_token.token_variant != TokenVariant.T_EOF:
            token = self.peek()

            match token.token_variant:
                case TokenVariant.T_IDENTIFIER:
                    self.parse_assignment()





