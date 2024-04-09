from classes.nodes import Variable, FunctionDeclaration
from typing import Optional


class Scope:
    def __init__(self, level: int, global_scope: bool = False):
        self.variables: dict[str, Variable] = {}
        self.functions: dict[str, FunctionDeclaration] = {}
        self.global_scope: bool = global_scope
        self.level = level

    def __str__(self):
        return "Scope| level: {level} global_scope: {global_scope} variables: {variables}".format(
            level = self.level,
            global_scope = self.global_scope,
            variables = ", ".join(name for name in self.variables.keys())
        )

    def add_variable(self, variable: Variable) -> None:
        if variable.value in self.variables:
            return

        self.variables.update({variable.value: variable})

    def add_function(self, function: FunctionDeclaration) -> None:
        self.functions.update({function.name: function})

    def lookup_variable(self, variable: str) -> Optional[Variable]:
        return self.variables[variable] if variable in self.variables else None

    def lookup_function(self, function: str) -> Optional[FunctionDeclaration]:
        return self.functions[function] if function in self.functions else None

