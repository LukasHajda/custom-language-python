from enum import Enum


class TokenVariant(Enum):
    T_PROGRAM = 'program',

    # END OF EXPRESSION
    T_DOT = 'dot',

    # OPERATORS
    T_ASSIGN = 'assign',
    T_PLUS = 'plus',
    T_MINUS = 'minus',
    T_DIVISION = 'division',
    T_MULTIPLICATION = 'multiplication',
    T_LESS = 'less',
    T_LESS_EQUAL = 'less_equal',
    T_GREATER = 'greater',
    T_GREATER_EQUAL = 'greater_equal',
    T_EQUAL = 'equal',
    T_NOT_EQUAL = 'not_equal',

    # TYPES
    T_INTEGER = 'integer',
    T_FLOAT = 'float',
    T_STRING = 'string',
    T_BOOLEAN = 'boolean',
    T_NULL = 'null',
    T_EOF = 'eof',

    # RESERVED WORDS
    T_IDENTIFIER = 'identifier',
    T_FUNCTION = 'function',
    T_NEGATE = 'negate',
    T_IF = 'if',
    T_ELSE = 'else',
    T_WHILE = 'while'

    # OTHERS
    T_LEFT_P = 'left_p',
    T_RIGHT_P = 'right_p',
    T_LEFT_CURLY_P = 'left_curly_p',
    T_RIGHT_CURLY_P = 'right_curly_p',

    # Errors
    T_ERROR = 'error',

    # INITIALIZATION
    T_EMPTY = 'empty',

    T_COMMENT = 'comment',
    T_WHITESPACE = 'whitespace'
    T_NEWLINE = 'newline'


class Token:
    def __init__(self, token_variant: TokenVariant, value: str, row: int, column: int):
        self.token_variant = token_variant
        self.value = value
        self.row = row
        self.column = column

    def __str__(self):
        return f"Token(type: {self.token_variant}, value:{self.value}, row:{self.row}, column:{self.column})"

    def __repr__(self):
        return self.__str__()
