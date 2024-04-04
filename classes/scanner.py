import functools
from typing import Callable, Any
from classes.token import Token, TokenVariant
from ply.lex import LexToken, Lexer
from ply import lex
from classes.errors import UnexpectedCharacterException

RESERVED_WORDS: dict = {
    'ak': TokenVariant.T_IF, 'inak': TokenVariant.T_ELSE,
    'tak': TokenVariant.T_THEN, 'pokial': TokenVariant.T_WHILE,
    'nepravda': TokenVariant.T_BOOLEAN, 'pravda': TokenVariant.T_BOOLEAN,
    'prirad': TokenVariant.T_ASSIGN, 'do': TokenVariant.T_TO,
    'nic': TokenVariant.T_NULL,
    'ukaz': TokenVariant.T_PRINT,
    'funkcia': TokenVariant.T_FUNCTION,
    'vrat': TokenVariant.T_RETURN,
}

TOKENS: dict = {
    'plus': TokenVariant.T_PLUS, 'minus': TokenVariant.T_MINUS,
    'division': TokenVariant.T_DIVISION, 'multiplication': TokenVariant.T_MULTIPLICATION,
    'modulo': TokenVariant.T_MODULO, 'div': TokenVariant.T_DIV,

    'less': TokenVariant.T_LESS, 'less_equal': TokenVariant.T_LESS_EQUAL,
    'greater': TokenVariant.T_GREATER, 'greater_equal': TokenVariant.T_GREATER_EQUAL,
    'equal': TokenVariant.T_EQUAL, 'not_equal': TokenVariant.T_NOT_EQUAL,

    'integer': TokenVariant.T_INTEGER, 'float': TokenVariant.T_FLOAT,
    'string': TokenVariant.T_STRING,
    'eof': TokenVariant.T_EOF, 'number': TokenVariant.T_NUMBER,

    'identifier': TokenVariant.T_IDENTIFIER,

    'left_p': TokenVariant.T_LEFT_P, 'right_p': TokenVariant.T_RIGHT_P,
    'left_curly_p': TokenVariant.T_LEFT_CURLY_P, 'right_curly_p': TokenVariant.T_RIGHT_CURLY_P,
    'left_square_p': TokenVariant.T_LEFT_SQUARE_P, 'right_square_p': TokenVariant.T_RIGHT_SQUARE_P,
    'dot': TokenVariant.T_DOT, 'colon': TokenVariant.T_COLON,

    'ignore_whitespace': TokenVariant.T_WHITESPACE, 'ignore_comments': TokenVariant.T_COMMENT,
    'ignore_newline': TokenVariant.T_NEWLINE,

}


def update_position(function: Callable) -> Callable:
    @functools.wraps(function)
    def wrapper(self: Any, token: LexToken) -> LexToken:
        if token.value == '\n':
            self.column = 1
            self.row += 1
            self.total = 0
        else:
            self.total += len(token.value)
            self.column = self.total - len(token.value) + 1

        return function(self, token)
    return wrapper


class Scanner:
    tokens: list = (
        list((RESERVED_WORDS | TOKENS).keys())
    )

    def __init__(self):
        self.scanner: Lexer = lex.lex(module = self)
        self.source: str = 'source_code.txt'
        self.row: int = 1
        self.column: int = 1
        self.total: int = 0
        self.is_beginning: bool = True
        self.__set_text()

    def __set_text(self) -> None:
        with open(self.source, 'r') as file:
            self.scanner.input(file.read())
        file.close()

    def __create_token(self, lex_token: LexToken) -> Token:
        token_variant = TOKENS.get(lex_token.type, RESERVED_WORDS.get(lex_token.type))
        return Token(
            token_variant = token_variant,
            value = lex_token.value.lower() if token_variant == TokenVariant.T_BOOLEAN else lex_token.value,
            row = self.row,
            column = self.column
        )

    @update_position
    def t_ignore_newline(self, token: LexToken) -> None:
        r"""[\n]"""
        pass

    @update_position
    def t_ignore_whitespace(self, token: LexToken) -> None:
        r"""[\t\r\s]"""
        pass

    @update_position
    def t_ignore_comments(self, token: LexToken) -> None:
        r"""\#.*"""
        pass

    @update_position
    def t_eof(self, token: LexToken) -> LexToken:
        return token

    @update_position
    def t_modulo(self, token: LexToken) -> LexToken:
        r"""\%"""
        return token

    @update_position
    def t_div(self, token: LexToken) -> LexToken:
        r"""\/\/"""
        return token

    @update_position
    def t_plus(self, token: LexToken) -> LexToken:
        r"""\+"""
        return token

    @update_position
    def t_minus(self, token: LexToken) -> LexToken:
        r"""\-"""
        return token

    @update_position
    def t_division(self, token: LexToken) -> LexToken:
        r"""\/"""
        return token

    @update_position
    def t_multiplication(self, token: LexToken) -> LexToken:
        r"""\*"""
        return token

    @update_position
    def t_left_p(self, token: LexToken) -> LexToken:
        r"""\("""
        return token

    @update_position
    def t_right_p(self, token: LexToken) -> LexToken:
        r"""\)"""
        return token

    @update_position
    def t_right_curly_p(self, token: LexToken) -> LexToken:
        r"""\}"""
        return token

    @update_position
    def t_left_curly_p(self, token: LexToken) -> LexToken:
        r"""\{"""
        return token

    @update_position
    def t_colon(self, token: LexToken) -> LexToken:
        r"""\,"""
        return token

    @update_position
    def t_less_equal(self, token: LexToken) -> LexToken:
        r"""\<\="""
        return token

    @update_position
    def t_greater_equal(self, token: LexToken) -> LexToken:
        r"""\>\="""
        return token

    @update_position
    def t_less(self, token: LexToken) -> LexToken:
        r"""\<"""
        return token

    @update_position
    def t_greater(self, token: LexToken) -> LexToken:
        r"""\>"""
        return token

    @update_position
    def t_equal(self, token: LexToken) -> LexToken:
        r"""\=\="""
        return token

    @update_position
    def t_not_equal(self, token: LexToken) -> LexToken:
        r"""\!\="""
        return token

    @update_position
    def t_string(self, token: LexToken) -> LexToken:
        r"""\"[^"]*\""""
        return token

    @update_position
    def t_number(self, token: LexToken) -> LexToken:
        r"""(([0-9]*\.)?[0-9]+)"""
        token.type = TokenVariant.T_FLOAT.value[0] if '.' in token.value else TokenVariant.T_INTEGER.value[0]
        return token

    @update_position
    def t_dot(self, token: LexToken) -> LexToken:
        r"""\."""
        return token

    @update_position
    def t_identifier(self, token: LexToken) -> LexToken:
        r"""[a-zA-Z_][a-zA-Z0-9]+"""
        token.type = token.value.lower() if token.value in RESERVED_WORDS else TokenVariant.T_IDENTIFIER.value[0]
        return token

    def t_error(self, token: LexToken) -> None:
        token.lexer.skip(1)
        raise UnexpectedCharacterException(
            message = "Lexing Error. Unexpected character: '{token}' at line {row} and column {column}".format(
                token = token.value[1],
                row = self.row,
                column = self.column
            )
        )

    def next_token(self) -> Token:
        if self.is_beginning:
            self.is_beginning = False
            return Token(TokenVariant.T_PROGRAM)
        else:
            try:
                lex_token = self.scanner.token()
                return self.__create_token(lex_token)
            except UnexpectedCharacterException as exception:
                print(exception)
                exit(0)
