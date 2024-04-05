from classes.nodes import ASTnode


class GeneralException(Exception):
    def __init__(self, message: str = None):
        self.message: str = f'{self.__class__.__name__}: {message}'

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.__str__()


class UnexpectedCharacterException(GeneralException):
    def __init__(self, message: str = None):
        super().__init__(message)


class UnexpectedTokenException(GeneralException):
    def __init__(self, message: str = None):
        super().__init__(message)


class InvalidOperandsForOperation(GeneralException):
    def __init__(self, message: str = None):
        super().__init__(message)


class NameErrorException(GeneralException):
    def __init__(self, message: str = None):
        super().__init__(message)


class DuplicateVariableDeclaration(GeneralException):
    def __init__(self, message: str = None):
        super().__init__(message)


class TypeErrorException(GeneralException):
    def __init__(self, message: str = None):
        super().__init__(message)


class Return(Exception):
    def __init__(self, value: ASTnode):
        super().__init__()
        self.value = value
