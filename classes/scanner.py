import functools
from typing import Optional, Callable, Iterator, Any
from classes.token import Token, TokenVariant
from ply.lex import LexToken
from ply import lex

SOURCE = 'source_code.txt'
NEWLINE = '\n'

TOKENS = {
    'plus': TokenVariant.T_PLUS, 'minus': TokenVariant.T_MINUS,
    'division': TokenVariant.T_DIVISION, 'multiplication': TokenVariant.T_MULTIPLICATION,
    'assign': TokenVariant.T_ASSIGN,
    'less': TokenVariant.T_LESS, 'less_equal': TokenVariant.T_LESS_EQUAL,
    'greater': TokenVariant.T_GREATER, 'greater_equal': TokenVariant.T_GREATER_EQUAL,
    'equal': TokenVariant.T_EQUAL, 'not_equal': TokenVariant.T_NOT_EQUAL,

    'integer': TokenVariant.T_INTEGER, 'float': TokenVariant.T_FLOAT,
    'boolean': TokenVariant.T_BOOLEAN, 'null': TokenVariant.T_NULL,
    'eof': TokenVariant.T_EOF,

    'identifier': TokenVariant.T_IDENTIFIER, 'if': TokenVariant.T_IF,
    'else': TokenVariant.T_ELSE, 'while': TokenVariant.T_WHILE,
    'left_p': TokenVariant.T_LEFT_P, 'right_p': TokenVariant.T_RIGHT_P,
    'left_curly_p': TokenVariant.T_LEFT_CURLY_P, 'right_curly_p': TokenVariant.T_RIGHT_CURLY_P,

    'ignore_whitespace': TokenVariant.T_WHITESPACE, 'ignore_comments': TokenVariant.T_COMMENT,
    'ignore_newline': TokenVariant.T_NEWLINE
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

        if 'ignore' not in token.type:
            return token
    return wrapper


class Scanner:
    tokens = (
        *(list(TOKENS.keys())),
    )

    def __init__(self):
        self.scanner = lex.lex(module = self)
        self.row = 0
        self.column = 1
        self.total = 0
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
    def t_assign(self, token: LexToken) -> LexToken:
        r"""[iI][sS]"""
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
    def t_integer(self, token: LexToken) -> LexToken:
        r"""[0-9]+"""
        return token

    @update_position
    def t_null(self, token: LexToken) -> LexToken:
        r"""[Nn][Uu][Ll][Ll]"""
        return token

    @update_position
    def t_boolean(self, token: LexToken) -> LexToken:
        r"""([Ff][Aa][Ll][Ss][Ee]]|[Tt][Rr][Uu][Ee])"""
        return token

    @update_position
    def t_if(self, token: LexToken) -> LexToken:
        r"""[Ii][Ff]"""
        return token

    @update_position
    def t_else(self, token: LexToken) -> LexToken:
        r"""[Ee][Ll][Ss][Ee]"""
        return token

    @update_position
    def t_identifier(self, token: LexToken) -> LexToken:
        r"""[a-zA-Z_][a-z]+"""
        return token

    def __set_text(self) -> None:
        with open(SOURCE, 'r') as file:
            self.scanner.input(file.read())
        file.close()

    def get_token(self):
        lex_token = self.scanner.token()
        return Token(
            token_variant = TOKENS.get(lex_token.type),
            value = lex_token.value,
            row = self.row,
            column = self.column
        )
