import functools
from typing import Callable, Any
from classes.token import Token, TokenVariant
from ply.lex import LexToken, Lexer
from ply import lex
from classes.errors import UnexpectedCharacterException

SOURCE: str = 'source_code.txt'
NEWLINE: str = '\n'

RESERVED_WORDS: dict = {
    'if': TokenVariant.T_IF,
    'while': TokenVariant.T_WHILE,
    'else': TokenVariant.T_ELSE,
    'null': TokenVariant.T_NULL,
    'false': TokenVariant.T_BOOLEAN,
    'true': TokenVariant.T_BOOLEAN,
    'is': TokenVariant.T_ASSIGN
}

TOKENS: dict = {
    'plus': TokenVariant.T_PLUS, 'minus': TokenVariant.T_MINUS,
    'division': TokenVariant.T_DIVISION, 'multiplication': TokenVariant.T_MULTIPLICATION,
    'modulo': TokenVariant.T_MODULO, 'div': TokenVariant.T_DIV,

    'less': TokenVariant.T_LESS, 'less_equal': TokenVariant.T_LESS_EQUAL,
    'greater': TokenVariant.T_GREATER, 'greater_equal': TokenVariant.T_GREATER_EQUAL,
    'equal': TokenVariant.T_EQUAL, 'not_equal': TokenVariant.T_NOT_EQUAL,

    'integer': TokenVariant.T_INTEGER, 'float': TokenVariant.T_FLOAT,
    'eof': TokenVariant.T_EOF,

    'identifier': TokenVariant.T_IDENTIFIER,

    'left_p': TokenVariant.T_LEFT_P, 'right_p': TokenVariant.T_RIGHT_P,
    'left_curly_p': TokenVariant.T_LEFT_CURLY_P, 'right_curly_p': TokenVariant.T_RIGHT_CURLY_P,
    'dot': TokenVariant.T_DOT,

    'ignore_whitespace': TokenVariant.T_WHITESPACE, 'ignore_comments': TokenVariant.T_COMMENT,
    'ignore_newline': TokenVariant.T_NEWLINE,

}


def update_position(function) -> Callable:

    @functools.wraps(function)
    def wrapper(self: Any, token: LexToken) -> LexToken:
        if token.value == NEWLINE:
            self.column = 1
            self.total = 0
            self.row += 1
        else:
            self.total += len(token.value)
            self.column = self.total - len(token.value) + 1

        return function(self, token)
    return wrapper


class Scanner:
    tokens: list = (
        *(list(TOKENS.keys())),
        *(list(set(RESERVED_WORDS.keys())))
    )

    def __init__(self):
        self.scanner: Lexer = lex.lex(module = self)
        self.is_beginning: bool = True
        self.row: int = 1
        self.column: int = 1
        self.total: int = 0
        self.__set_text()

    @update_position
    def t_ignore_newline(self, token: LexToken) -> None:
        r"""[\n]"""
        pass

    @update_position
    def t_ignore_whitespace(self, token: LexToken) -> None:
        r"""[\t\r\s]"""
        pass

    @update_position
    def t_ignore_comments(self, token: LexToken) -> LexToken:
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
        r"""\="""
        return token

    @update_position
    def t_not_equal(self, token: LexToken) -> LexToken:
        r"""\!\="""
        return token

    @update_position
    def t_float(self, token: LexToken) -> LexToken:
        r"""([0-9]*\.[0-9]+)"""
        return token

    @update_position
    def t_dot(self, token: LexToken) -> LexToken:
        r"""\."""
        return token

    @update_position
    def t_integer(self, token: LexToken) -> LexToken:
        r"""[0-9]+"""
        return token

    @update_position
    def t_identifier(self, token: LexToken) -> LexToken:
        r"""[a-zA-Z_][a-z]+"""
        token.type = token.value if token.value in RESERVED_WORDS else TokenVariant.T_IDENTIFIER.value[0]
        return token

    def t_error(self, token: LexToken) -> None:
        token.lexer.skip(1)
        raise UnexpectedCharacterException(
            message = "Unexpected character: '{token}' at line {row} and column {column}".format(
                token = token.value,
                row = self.row,
                column = self.column
            )
        )

    def __set_text(self) -> None:
        with open(SOURCE, 'r') as file:
            self.scanner.input(file.read())
        file.close()

    def get_token(self) -> Token:
        lex_token: Token = self.scanner.token()
        if self.is_beginning:
            self.is_beginning = False
            return Token(TokenVariant.T_PROGRAM)
        return Token(
            token_variant = TOKENS.get(lex_token.type, RESERVED_WORDS.get(lex_token.type)),
            value = lex_token.value,
            row = self.row,
            column = self.column
        )
