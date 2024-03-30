from classes.nodes import ASTnode
from typing import Callable, Any


class VisitorSemanticAnalyzer:
    def visit(self, node: ASTnode) -> Callable | Exception:
        method = getattr(self, f"visit_{node.type.value}", self.__exception_visit)
        return method(node)

    def __exception_visit(self, node: ASTnode) -> Exception:
        raise Exception(f'No visit_{node.type.value} method')


class VisitorVisualizer:
    def add(self, node: ASTnode, **kwargs) -> Callable | Exception:
        print(node)
        method = getattr(self, f"add_{node.type.value}", self.__exception_add)
        return method(node, kwargs['parent'])

    def __exception_add(self, node: ASTnode, _) -> Exception:
        return Exception(f'No add_{node.type.value} method')


class VisitorInterpreter:
    def evaluate(self, node: ASTnode) -> Any:
        method = getattr(self, f"evaluate_{node.type.value}", self.__exception_evaluate)
        return method(node)

    def __exception_evaluate(self, node: ASTnode) -> Exception:
        raise Exception(f'No evaluate_{node.type.value} method')
