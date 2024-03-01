# from typing import Optional, Callable, Iterator
# from classes.token_variant import TokenVariant
# from classes.token import Token
from ply.lex import LexToken
from ply import lex

SOURCE = 'source_code.txt'
NEWLINE = '\n'
OPERATORS = ['PLUS', 'MINUS', 'DIVISION', 'MULTIPLICATION',
             'ASSIGN', 'LESS', 'LESS_EQUAL', 'GREATER',
             'GREATER_EQUAL', 'EQUAL', 'NOT_EQUAL']

TYPES = ['INTEGER', 'FLOAT', 'boolean', 'NULL', 'EOF']
RESERVED_WORDS = ['IDENTIFIER', 'FUNCTION', 'NEGATE', 'IF', 'ELSE', 'WHILE']


class Scanner:
    tokens = (*TYPES, *RESERVED_WORDS, *OPERATORS)

    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_DIVISION = r'\/'
    t_MULTIPLICATION = r'\*'
    t_LESS = r'\<'
    t_LESS_EQUAL = r'\<\='
    t_GREATER = r'\>'
    t_GREATER_EQUAL = r'\>\='
    t_EQUAL = r'='
    t_NOT_EQUAL = r'!='

    t_INTEGER = r'[0-9]+'
    t_FLOAT = r'([0-9]*\.[0-9]+)'
    t_NULL = r'null'
    t_ignore_WHITESPACE = r'[ \t\r\n\s]'
    t_IDENTIFIER = r'[a-zA-Z_][a-z]+'

    def __init__(self):
        self.scanner = lex.lex(module = self)
        self.__set_text()

    def t_ASSIGN(self, token) -> LexToken:
        r"""[iI][sS]"""
        return token

    def t_boolean(self, token) -> LexToken:
        r"""(false|true)"""
        return token

    def __set_text(self) -> None:
        with open(SOURCE, 'r') as file:
            self.scanner.input(file.read())
        file.close()

    # TODO: Dokonci EOF,
    def get_token(self) -> ...:
        pass
