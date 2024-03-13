from classes.nodes import Variable


class Scope:
    def __init__(self, level: int, global_scope: bool = False):
        self.variables: dict[str, None] = {}
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

        self.variables.update({variable.value: None})

    def lookup(self, variable: str) -> bool:
        return variable in self.variables

