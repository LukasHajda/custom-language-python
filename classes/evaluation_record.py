from typing import Any


class EvaluationRecord:
    def __init__(self):
        self.variables: dict = {}
        self.functions: dict = {}

    def __str__(self):
        return f"{self.variables}"

    def get_function(self, function_name: str) -> Any:
        return self.functions[function_name]

    def get_variable(self, variable_name: str) -> Any:
        return self.variables.get(variable_name, None)

    def set_function(self, key: str, value: Any) -> None:
        self.functions[key] = value

    def set_variable(self, key: str, value: Any) -> None:
        self.variables[key] = value

