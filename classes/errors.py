class UnexpectedCharacterException(Exception):
    def __init__(self, message: str = None):
        self.message = f'{self.__class__.__name__}: {message}'
        super().__init__(self.message)


class UnexpectedTokenException(Exception):
    def __init__(self, message: str = None):
        self.message = f'{self.__class__.__name__}: {message}'
        super().__init__(self.message)


# TODO: Mozno trosku prerobit tieto exceptiony
# TODO: Doplnit row a column aby sa vedelo kde sa errory nachadzaju

class InvalidOperandsForOperation(Exception):
    def __init__(self, message: str = None):
        self.message = f'{self.__class__.__name__}: {message}'
        super().__init__(self.message)


class UndeclaredVariable(Exception):
    def __init__(self, message: str = None):
        self.message = f'{self.__class__.__name__}: {message}'
        super().__init__(self.message)

    # TODO: Vytvor parent classu ktora bude dedit z Exception a dorob tam __str__
    def __str__(self):
        return self.message


class DuplicateVariableDeclaration(Exception):
    def __init__(self, message: str = None):
        self.message = f'{self.__class__.__name__}: {message}'
        super().__init__(self.message)

    def __str__(self):
        return self.message
