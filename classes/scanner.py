from typing import Optional, Callable, Iterator
from classes.tokens import Token
from ply import lex

SOURCE = 'source_code.txt'


class Scanner:
    def __init__(self):
        self.source: Optional[str] = None
        self.current_character: Optional[str] = None
        self.previous_character: Optional[str] = None
        self.row: int = 1
        self.column: int = 0
        self.tokens: Optional[list] = None

        self.__load_source_code()
        self.__read_character()

    def start_scanner(self) -> None:
        self.tokens = [_ for _ in self.get_token()]

    def get_tokens(self) -> list:
        return self.tokens

    def get_token(self) -> Iterator:
        pass

    def __read_character(self):
        for character in self.source:
            self.__increase_row_and_column()
            self.previous_character = self.current_character
            self.current_character = character

            print(self.current_character)

    def __load_source_code(self) -> None:
        with open(SOURCE, 'r') as file:
            self.source = file.read()

    def __increase_row_and_column(self) -> None:
        if self.current_character == '\n':
            self.row += 1
            self.column = 0
        else:
            self.column += 1

        print(f"ROW: {self.row}, COLUMN: {self.column}")
