from classes.scanner import Scanner, TokenVariant
from classes.token import Token
from classes.errors import UnexpectedTokenException
from typing import Optional


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner: Scanner = scanner
        self.current_token: Optional[Token] = None

    def eat(self, expected_token: TokenVariant) -> None:
        token = self.scanner.get_token()

        if token.token_variant != expected_token:
            raise UnexpectedTokenException(
                message = "Expected token: '{expected}' but '{given}' was given".format(
                    expected = expected_token.value[0],
                    given = token.token_variant.value[0],
                )
            )

        self.current_token = token

