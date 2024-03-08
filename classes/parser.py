from classes.scanner import Scanner, TokenVariant
from classes.token import Token
from classes.errors import UnexpectedTokenException
from classes.nodes import *
from typing import Optional


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner: Scanner = scanner
        self.current_token: Optional[Token] = self.scanner.next_token()

    def eat(self, expected_token: TokenVariant) -> None:

        if self.current_token.token_variant != expected_token:
            raise UnexpectedTokenException(
                message = "Parsing Error. Expected token: '{expected}' but '{given}' was given".format(
                    expected = expected_token.value[0],
                    given = self.current_token.token_variant.value[0],
                )
            )

        self.current_token = self.scanner.next_token()

    def peek(self) -> Token:
        return self.scanner.peek()

    def create_integer_literal_node(self) -> ASTnode:
        node = Literal(
            token_variant = TokenVariant.T_INTEGER,
            value = int(self.current_token.value)
        )
        self.eat(TokenVariant.T_INTEGER)
        return node

    def create_float_literal_node(self) -> ASTnode:
        node = Literal(
            token_variant = TokenVariant.T_FLOAT,
            value = float(self.current_token.value)
        )

        self.eat(TokenVariant.T_FLOAT)
        return node

    def create_boolean_literal_node(self) -> ASTnode:
        # TODO: Tu musi byt nejaky raise exception.
        node = Literal(
            token_variant = TokenVariant.T_BOOLEAN,
            value = 'true' == self.current_token.value
        )

        self.eat(TokenVariant.T_BOOLEAN)
        return node

    def create_unary_operation_node(self) -> ASTnode:
        operator = self.current_token.token_variant
        self.eat(self.current_token.token_variant)

        node = UnaryOperation(
            operator = operator,
            operand = self.parse_factor()
        )

        return node

    def create_variable(self) -> ASTnode:
        node = Variable(
            value = self.current_token.value
        )

        self.eat(self.current_token.token_variant)
        return node

    def parse_factor(self) -> ASTnode:
        match self.current_token.token_variant:
            case TokenVariant.T_INTEGER:
                return self.create_integer_literal_node()
            case TokenVariant.T_FLOAT:
                return self.create_float_literal_node()
            case TokenVariant.T_BOOLEAN:
                return self.create_boolean_literal_node()
            case TokenVariant.T_MINUS:
                return self.create_unary_operation_node()
            case TokenVariant.T_PLUS:
                return self.create_unary_operation_node()
            case TokenVariant.T_LEFT_P:
                self.eat(TokenVariant.T_LEFT_P)
                node = self.parse_expression()
                self.eat(TokenVariant.T_RIGHT_P)
                return node
            case _:
                node = self.create_variable()
                return node

    def parse_term(self) -> ASTnode:
        node = self.parse_factor()

        while self.current_token.token_variant in (
            TokenVariant.T_MULTIPLICATION,
            TokenVariant.T_DIVISION,
            TokenVariant.T_DIV,
            TokenVariant.T_MODULO
        ):
            current_token = self.current_token.token_variant

            match current_token:
                case TokenVariant.T_MULTIPLICATION:
                    self.eat(TokenVariant.T_MULTIPLICATION)
                case TokenVariant.T_DIVISION:
                    self.eat(TokenVariant.T_DIVISION)
                case TokenVariant.T_DIV:
                    self.eat(TokenVariant.T_DIV)
                case TokenVariant.T_MODULO:
                    self.eat(TokenVariant.T_MODULO)

            node = BinaryOperation(
                left_operand = node,
                right_operand = self.parse_factor(),
                operator = current_token
            )

        return node

    def parse_expression(self) -> ASTnode:
        node = self.parse_term()

        # TODO: mozno by bolo fajn zrusit `match` a dat tam iba self.current_token.token_variant
        while self.current_token.token_variant in (TokenVariant.T_PLUS, TokenVariant.T_MINUS):
            current_token = self.current_token.token_variant
            match self.current_token.token_variant:
                case TokenVariant.T_PLUS:
                    self.eat(TokenVariant.T_PLUS)
                case TokenVariant.T_MINUS:
                    self.eat(TokenVariant.T_MINUS)

            node = BinaryOperation(
                left_operand = node,
                right_operand = self.parse_term(),
                operator = current_token
            )
        return node

    def parse_condition(self) -> ASTnode:
        node = self.parse_expression()

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
                    self.eat(TokenVariant.T_EQUAL)
                case TokenVariant.T_NOT_EQUAL:
                    self.eat(TokenVariant.T_NOT_EQUAL)
                case TokenVariant.T_LESS:
                    self.eat(TokenVariant.T_LESS)
                case TokenVariant.T_LESS_EQUAL:
                    self.eat(TokenVariant.T_LESS_EQUAL)
                case TokenVariant.T_GREATER:
                    self.eat(TokenVariant.T_GREATER)
                case TokenVariant.T_GREATER_EQUAL:
                    self.eat(TokenVariant.T_GREATER_EQUAL)

            node = BinaryOperation(
                left_operand = node,
                right_operand = self.parse_term(),
                operator = current_token
            )

        return node

    def parse_program(self) -> Program:
        root = Program()

        self.eat(TokenVariant.T_PROGRAM)
        root.statements = self.parse_statements()
        return root

    def parse_assignment(self) -> ASTnode:
        node = AssignmentStatement()

        node.name = self.create_variable()

        self.eat(TokenVariant.T_ASSIGN)

        node.value = self.parse_expression()
        return node

    def parse_else(self) -> ASTnode:
        self.eat(TokenVariant.T_ELSE)
        self.eat(TokenVariant.T_LEFT_CURLY_P)

        node = ElseStatement()
        node.statements = self.parse_statements()
        self.eat(TokenVariant.T_RIGHT_CURLY_P)
        return node

    def parse_if(self) -> ASTnode:
        node = IfStatement()

        self.eat(TokenVariant.T_IF)
        self.eat(TokenVariant.T_LEFT_P)

        node.condition = Condition()
        node.condition.value = self.parse_condition()
        self.eat(TokenVariant.T_RIGHT_P)
        self.eat(TokenVariant.T_LEFT_CURLY_P)
        node.statements = self.parse_statements()

        self.eat(TokenVariant.T_RIGHT_CURLY_P)

        if self.current_token.token_variant == TokenVariant.T_ELSE:
            node.else_statement = self.parse_else()

        # print("KONEC IF: ", node.statements)

        return node

    def parse_while(self) -> ASTnode:
        node = WhileStatement()

        self.eat(TokenVariant.T_WHILE)
        self.eat(TokenVariant.T_LEFT_P)

        node.condition = Condition()
        node.condition.value = self.parse_condition()
        self.eat(TokenVariant.T_RIGHT_P)
        self.eat(TokenVariant.T_LEFT_CURLY_P)

        node.statements = self.parse_statements()

        self.eat(TokenVariant.T_RIGHT_CURLY_P)

        return node

    def parse_statements(self) -> list:
        statements = []
        while self.current_token.token_variant != TokenVariant.T_EOF:

            match self.current_token.token_variant:
                case TokenVariant.T_IDENTIFIER:
                    # print(self.current_token)
                    statement = self.parse_assignment()
                    statements.append(statement)
                    self.eat(TokenVariant.T_DOT)
                case TokenVariant.T_IF:
                    statement = self.parse_if()
                    statements.append(statement)
                case TokenVariant.T_WHILE:
                    statement = self.parse_while()
                    statements.append(statement)
                case _:
                    # print(self.current_token)
                    break

        return statements

    def parse(self) -> Program:
        return self.parse_program()


