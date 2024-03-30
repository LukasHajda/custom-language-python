from classes.scanner import Scanner
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
                message = "Expected token: '{expected}' but '{given}' was given at row {row} and column {column}".format(
                    expected = expected_token.value[1],
                    given = self.current_token.token_variant.value[1],
                    row = self.current_token.row,
                    column = self.current_token.column
                )
            )

        self.current_token = self.scanner.next_token()

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
        node = Literal(
            token_variant = TokenVariant.T_BOOLEAN,
            value = 'pravda' == self.current_token.value
        )

        self.__eat(TokenVariant.T_BOOLEAN)
        return node

    def __create_string_literal(self) -> ASTnode:
        node = Literal(
            token_variant = TokenVariant.T_STRING,
            value = self.current_token.value
        )

        self.__eat(TokenVariant.T_STRING)
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
            value = self.current_token.value,
            row = self.current_token.row,
            column = self.current_token.column
        )

        self.__eat(TokenVariant.T_IDENTIFIER)
        return node

    def __parse_factor(self) -> ASTnode:
        match self.current_token.token_variant:
            case TokenVariant.T_INTEGER:
                return self.__create_integer_literal_node()
            case TokenVariant.T_FLOAT:
                return self.__create_float_literal_node()
            case TokenVariant.T_STRING:
                return self.__create_string_literal()
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

            self.__eat(current_token)

            node = BinaryOperation(
                left_operand = node,
                right_operand = self.__parse_factor(),
                operator = current_token
            )

        return node

    def __parse_expression(self) -> ASTnode:
        node = self.__parse_term()

        while self.current_token.token_variant in (TokenVariant.T_PLUS, TokenVariant.T_MINUS):
            current_token = self.current_token.token_variant

            self.__eat(current_token)

            node = BinaryOperation(
                left_operand = node,
                right_operand = self.__parse_term(),
                operator = current_token
            )
        return node

    def __parse_condition(self) -> ASTnode:
        node = self.__parse_expression()

        if self.current_token.token_variant in (
            TokenVariant.T_EQUAL,
            TokenVariant.T_NOT_EQUAL,
            TokenVariant.T_LESS,
            TokenVariant.T_LESS_EQUAL,
            TokenVariant.T_GREATER,
            TokenVariant.T_GREATER_EQUAL
        ):
            current_token = self.current_token.token_variant

            self.__eat(current_token)

            node = BinaryOperation(
                left_operand = node,
                right_operand = self.__parse_expression(),
                operator = current_token
            )

        return node

    def __parse_program(self) -> Program:
        root = Program()

        self.__eat(TokenVariant.T_PROGRAM)
        root.block = self.__parse_statements()
        return root

    def __parse_assignment(self) -> ASTnode:
        self.__eat(TokenVariant.T_TO)
        node = AssignmentStatement()

        node.name = self.__create_variable()

        self.__eat(TokenVariant.T_ASSIGN)

        node.value = self.__parse_expression()
        return node

    def __parse_else(self) -> ASTnode:
        self.__eat(TokenVariant.T_ELSE)
        self.__eat(TokenVariant.T_LEFT_CURLY_P)

        node = ElseStatement()
        node.block = self.__parse_statements(until_curly_p = True)
        self.__eat(TokenVariant.T_RIGHT_CURLY_P)
        return node

    def __parse_if(self) -> ASTnode:
        node = IfStatement()

        self.__eat(TokenVariant.T_IF)
        self.__eat(TokenVariant.T_LEFT_P)

        node.condition = Condition()
        node.condition.value = self.__parse_condition()
        self.__eat(TokenVariant.T_RIGHT_P)
        self.__eat(TokenVariant.T_THEN)
        self.__eat(TokenVariant.T_LEFT_CURLY_P)
        node.block = self.__parse_statements(until_curly_p = True)

        self.__eat(TokenVariant.T_RIGHT_CURLY_P)

        if self.current_token.token_variant == TokenVariant.T_ELSE:
            node.else_block = self.__parse_else()

        return node

    def __parse_print(self) -> ASTnode:
        node = PrintStatement()
        self.__eat(TokenVariant.T_PRINT)
        self.__eat(TokenVariant.T_LEFT_P)

        node.value = self.__parse_expression()

        self.__eat(TokenVariant.T_RIGHT_P)
        self.__eat(TokenVariant.T_DOT)

        return node

    def __parse_while(self) -> ASTnode:
        node = WhileStatement()

        self.__eat(TokenVariant.T_WHILE)
        self.__eat(TokenVariant.T_LEFT_P)

        node.condition = Condition()
        node.condition.value = self.__parse_condition()
        self.__eat(TokenVariant.T_RIGHT_P)
        self.__eat(TokenVariant.T_THEN)
        self.__eat(TokenVariant.T_LEFT_CURLY_P)

        node.block = self.__parse_statements(until_curly_p = True)

        self.__eat(TokenVariant.T_RIGHT_CURLY_P)

        return node

    def __parse_arguments(self) -> ASTnode:
        argument_list = ArgumentList()

        while self.current_token.token_variant != TokenVariant.T_RIGHT_P:
            argument = Argument()
            argument.value = self.__parse_expression()

            argument_list.arguments.append(argument)

        return argument_list

    def __parse_parameters(self) -> ASTnode:
        parameter_list = ParameterList()
        first_parameter = True

        while self.current_token.token_variant != TokenVariant.T_RIGHT_P:
            if not first_parameter:
                self.__eat(TokenVariant.T_COLON)

            parameter = Parameter(
                name = self.current_token.value
            )
            parameter_list.parameters.append(parameter)
            self.__eat(TokenVariant.T_IDENTIFIER)
            first_parameter = False

        self.__eat(TokenVariant.T_RIGHT_P)

        return parameter_list

    def __parse_function_declaration(self) -> ASTnode:
        self.__eat(TokenVariant.T_FUNCTION)

        function = FunctionDeclaration()
        function.name = self.current_token.value

        self.__eat(TokenVariant.T_IDENTIFIER)
        self.__eat(TokenVariant.T_LEFT_P)
        parameter_list = self.__parse_parameters()

        self.__eat(TokenVariant.T_LEFT_CURLY_P)
        function.block = self.__parse_statements(until_curly_p = True)
        function.block.statements.appendleft(parameter_list)

        self.__eat(TokenVariant.T_RIGHT_CURLY_P)

        return function

    def __parser_return_statement(self) -> ASTnode:
        self.__eat(TokenVariant.T_RETURN)

        return_statement = ReturnStatement()
        return_statement.value = self.__parse_expression()

        self.__eat(TokenVariant.T_DOT)

        return return_statement

    def __parser_function_call(self) -> ASTnode:
        function_call = FunctionCall()
        function_call.name = self.current_token.value

        self.__eat(TokenVariant.T_IDENTIFIER)
        self.__eat(TokenVariant.T_LEFT_P)

        function_call.argument_list = self.__parse_arguments()

        self.__eat(TokenVariant.T_RIGHT_P)
        self.__eat(TokenVariant.T_DOT)

        return function_call


    # TODO: Mozno skusit potom urobit samostatny block.
    def __parse_statements(self, until_curly_p: bool = False) -> ASTnode:
        block = Block()
        while self.current_token.token_variant not in (
                TokenVariant.T_EOF,
                TokenVariant.T_RIGHT_CURLY_P if until_curly_p else ...
        ):

            match self.current_token.token_variant:
                case TokenVariant.T_TO:
                    statement = self.__parse_assignment()
                    block.statements.append(statement)
                    self.__eat(TokenVariant.T_DOT)
                case TokenVariant.T_IF:
                    statement = self.__parse_if()
                    block.statements.append(statement)
                case TokenVariant.T_WHILE:
                    statement = self.__parse_while()
                    block.statements.append(statement)
                # Function call
                case TokenVariant.T_IDENTIFIER:
                    function_call = self.__parser_function_call()
                    block.statements.append(function_call)
                case TokenVariant.T_PRINT:
                    statement = self.__parse_print()
                    block.statements.append(statement)
                case TokenVariant.T_FUNCTION:
                    function_declaration = self.__parse_function_declaration()
                    block.statements.append(function_declaration)
                case TokenVariant.T_RETURN:
                    statement = self.__parser_return_statement()
                    block.statements.append(statement)
                case _:
                    raise UnexpectedTokenException(
                        message = f"Unexpected Token: {self.current_token}"
                    )

        return block

    def parse(self) -> Program:
        try:
            return self.__parse_program()
        except (UnexpectedTokenException, ) as exception:
            print(exception)
            exit(0)


