from classes.nodes import ASTnode
from typing import Any


class NodeVisitor:
    def visit(self, node: ASTnode) -> Any:
        method = getattr(self, f"visit_{node.type.value}", self.__exception_visit)
        return method(node)

    def __exception_visit(self, node: ASTnode) -> Exception:
        raise Exception(f'No visit_{node.type.value} method')
