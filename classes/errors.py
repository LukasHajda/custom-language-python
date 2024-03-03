class UnexpectedCharacterException(Exception):
    def __init__(self, message: str = None):
        self.message = f'{self.__class__.__name__}: {message}'
        super().__init__(self.message)


class UnexpectedTokenException(Exception):
    def __init__(self, message: str = None):
        self.message = f'{self.__class__.__name__}: {message}'
        super().__init__(self.message)