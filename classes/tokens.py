from enum import Enum


class Token(Enum):
    T_PROGRAM = 1,

    # END OF EXPRESSION
    T_DOT = 2,

    # OPERATORS
    T_ASSIGN = 4,
    T_PLUS = 5,
    T_MINUS = 6,
    T_DIVISION = 7,
    T_MULTIPLICATION = 8,
    T_LESS = 9,
    T_LESS_EQUAL = 10,
    T_GREATER = 11,
    T_GREATER_EQUAL = 12,
    T_EQUAL = 13,
    T_NOT_EQUAL = 14,

    # TYPES
    T_INTEGER = 15,
    T_FLOAT = 16,
    T_STRING = 17,
    T_BOOLEAN = 18,
    T_NULL = 19,
    T_EOF = 20,

    # RESERVED WORDS
    T_IDENTIFIER = 21,
    T_FUNCTION = 22,
    T_NEGATE = 23,
    T_IF = 24,
    T_ELSE = 25,

    # OTHERS
    T_LEFT_P = 26,
    T_RIGHT_P = 27,
    T_LEFT_CURLY_P = 28,
    T_RIGHT_CURLY_P = 29,

    # Errors
    T_ERROR = 30,

    # INITIALIZATION
    T_EMPTY = 31
