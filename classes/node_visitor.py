from classes.nodes import ASTnode
from typing import Callable


class VisitorSemanticAnalyzer:
    def visit(self, node: ASTnode) -> Callable | Exception:
        method = getattr(self, f"visit_{node.type.value}", self.__exception_visit)
        return method(node)

    def __exception_visit(self, node: ASTnode) -> Exception:
        raise Exception(f'No visit_{node.type.value} method')


class VisitorVisualizer:
    def add(self, node: ASTnode, **kwargs) -> Callable | Exception:
        method = getattr(self, f"add_{node.type.value}", self.__exception_add)
        return method(node, kwargs['parent'])

    def __exception_add(self, node: ASTnode, _) -> Exception:
        return Exception(f'No add_{node.type.value} method')
