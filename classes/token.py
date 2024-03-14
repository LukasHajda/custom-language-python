from enum import Enum


class TokenVariant(Enum):
    T_PROGRAM = ('program', 'program')

    # END OF EXPRESSION
    T_DOT = ('dot', '.')

    # OPERATORS
    T_ASSIGN = ('assign', 'is')
    T_PLUS = ('plus', '+')
    T_MINUS = ('minus', '-')
    T_DIVISION = ('division', '/')
    T_MODULO = ('modulo', '%')
    T_DIV = ('div', '//')
    T_MULTIPLICATION = ('multiplication', '*')
    T_LESS = ('less', '<')
    T_LESS_EQUAL = ('less_equal', '<=')
    T_GREATER = ('greater', '>')
    T_GREATER_EQUAL = ('greater_equal', '>=')
    T_EQUAL = ('equal', '==')
    T_NOT_EQUAL = ('not_equal', '!=')

    # TYPES
    T_INTEGER = ('integer', 'integer')
    T_FLOAT = ('float', 'float')
    T_STRING = ('string', 'string')
    T_BOOLEAN = ('boolean', 'boolean')
    T_NULL = ('null', 'null')
    T_EOF = ('eof', 'eof')

    # RESERVED WORDS
    T_IDENTIFIER = ('identifier', 'identifier')
    # T_NEGATE = ('negate', '!')
    T_IF = ('if', 'if')
    T_ELSE = ('else', 'else')
    T_WHILE = ('while', 'while')

    # OTHERS
    T_LEFT_P = ('left_p', '(')
    T_RIGHT_P = ('right_p', ')')
    T_LEFT_CURLY_P = ('left_curly_p', '{')
    T_RIGHT_CURLY_P = ('right_curly_p', '}')

    # Errors
    T_ERROR = ('error', 'error')

    # INITIALIZATION
    T_EMPTY = ('empty', 'empty')

    T_COMMENT = ('comment', '#')
    T_WHITESPACE = ('whitespace', 'whitespace')
    T_NEWLINE = ('newline', 'newline')


class Token:
    def __init__(self, token_variant: TokenVariant, value: str = None, row: int = 0, column: int = 0):
        self.token_variant: TokenVariant = token_variant
        self.value: str = value
        self.row: int = row
        self.column: int = column

    def __str__(self):
        return f"Token(type: {self.token_variant}, value:{self.value}, row:{self.row}, column:{self.column})"

    def __repr__(self):
        return self.__str__()
