from typing import Any


class EvaluationRecord:
    def __init__(self, name: str):
        self.variables: dict = {}
        self.functions: dict = {}
        self.name = name

    def get_function(self, function_name: str) -> Any:
        return self.functions[function_name]

    def get_variable(self, variable_name: str) -> Any:
        return self.variables[variable_name]

    def set_function(self, key: str, value: Any) -> None:
        self.functions[key] = value

    def set_variable(self, key: str, value: Any) -> None:
        self.variables[key] = value

