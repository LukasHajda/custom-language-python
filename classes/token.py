from enum import Enum


class TokenVariant(Enum):
    T_PRINT = ('print', 'ukaz')
    T_FUNCTION = ('function', 'funkcia')
    T_RETURN = ('return', 'vrat')
    T_COLON = ('colon', ',')

    T_PROGRAM = ('program', 'program')
    T_DOT = ('dot', '.')
    T_ASSIGN = ('assign', 'prirad')
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
    T_NUMBER = ('number', 'number')
    T_INTEGER = ('integer', 'integer')
    T_FLOAT = ('float', 'float')
    T_STRING = ('string', 'string')
    T_BOOLEAN = ('boolean', 'boolean')
    T_NULL = ('null', 'null')
    T_EOF = ('eof', 'eof')

    # RESERVED WORDS
    T_IDENTIFIER = ('identifier', 'identifier')
    T_IF = ('ak', 'ak')
    T_ELSE = ('else', 'inak')
    T_WHILE = ('while', 'pokial')
    T_THEN = ('tak', 'tak')

    # OTHERS
    T_LEFT_P = ('left_p', '(')
    T_RIGHT_P = ('right_p', ')')
    T_LEFT_CURLY_P = ('left_curly_p', '{')
    T_RIGHT_CURLY_P = ('right_curly_p', '}')
    T_LEFT_SQUARE_P = ('left_square_p', '[')
    T_RIGHT_SQUARE_P = ('right_square_p', ']')
    T_TO = ('do', 'do')

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
