import graphviz
from classes.nodes import *


class Visualizer(graphviz.Digraph):
    def __init__(self, root: ASTnode):
        super().__init__()
        self.root: ASTnode = root
        self.stack = [root]
        self.parents = [None]
        self.nodes = []

    def __increase_queues(self, stack_value: Any, parent_value: Any) -> None:
        self.stack.append(stack_value)
        self.parents.append(parent_value)

    def __traverse_ast(self) -> None:
        # TODO: pozri collectiosn: deque
        while self.stack:
            current_node = self.stack.pop(0)
            parent = self.parents.pop(0)

            current_node_name = self.__add_node(current_node)

            if isinstance(current_node, Program):
                for statement in current_node.statements:
                    self.__increase_queues(stack_value = statement, parent_value = current_node_name)

            if isinstance(current_node, AssignmentStatement):
                self.__add_edge(parent, current_node_name)
                self.__increase_queues(stack_value = current_node.name, parent_value = current_node_name)
                self.__increase_queues(stack_value = current_node.value, parent_value = current_node_name)

            if isinstance(current_node, Variable) or isinstance(current_node, Literal):
                self.__add_edge(parent, current_node_name)

            if isinstance(current_node, BinaryOperation):
                self.__add_edge(parent, current_node_name)
                self.__increase_queues(stack_value = current_node.left_operand, parent_value = current_node_name)
                self.__increase_queues(stack_value = current_node.right_operand, parent_value = current_node_name)

            if isinstance(current_node, UnaryOperation):
                self.__add_edge(parent, current_node_name)
                self.__increase_queues(stack_value = current_node.operand, parent_value = current_node_name)


    def __generate_node_name(self, node: ASTnode) -> (str, str):
        # TODO: toto nejako uprav, class bude mat svoj __str__ alebo daco take
        index = 1
        label_name = type(node).__name__
        extra_info = ''
        if isinstance(node, Variable):
            extra_info = f' name: {node.value}'
        if isinstance(node, Literal):
            extra_info = f' value: {node.value}'
        if isinstance(node, BinaryOperation):
            extra_info = f' operator: {node.operator.value[0]}'
        if isinstance(node, UnaryOperation):
            extra_info = f' operator: {node.operator.value[0]}'
        while 1:
            id_name = f"{label_name}_{index}"
            if id_name not in self.nodes:
                self.nodes.append(id_name)
                return id_name, (label_name + extra_info)
            index += 1

    def __add_node(self, node: ASTnode) -> str:
        id_name, label_name = self.__generate_node_name(node)
        self.node(id_name, label_name)
        return id_name

    def __add_edge(self, parent: str, node: str):
        self.edge(parent, node)

    def visualize_tree(self):
        self.__traverse_ast()
        self.render('graph', view = True)
