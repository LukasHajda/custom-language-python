import graphviz
from classes.nodes import *


class Visualizer(graphviz.Digraph):
    def __init__(self, root: Program):
        super().__init__()
        self.root: Program = root
        self.stack: deque = deque([root])
        self.parents: deque = deque([None])
        self.nodes: dict = {
            Program.__name__: 0,
            AssignmentStatement.__name__: 0,
            IfStatement.__name__: 0,
            ElseStatement.__name__: 0,
            WhileStatement.__name__: 0,
            BinaryOperation.__name__: 0,
            UnaryOperation.__name__: 0,
            Variable.__name__: 0,
            Literal.__name__: 0,
            Condition.__name__: 0,
            Block.__name__: 0
        }

    def __increase_queues(self, stack_value: Any, parent_value: Any) -> None:
        self.stack.append(stack_value)
        self.parents.append(parent_value)

    def __add_program(self, node: Program) -> None:
        current_node_name = self.__add_node(node)
        self.__increase_queues(stack_value = node.block, parent_value = current_node_name)

    def __add_assignment_statement(self, node: AssignmentStatement, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)

        self.__increase_queues(stack_value = node.name, parent_value = current_node_name)
        self.__increase_queues(stack_value = node.value, parent_value = current_node_name)

    def __add_variable(self, node: Variable, parent: str) -> None:
        current_node_name = self.__add_node(
            node = node,
            extra_info = f"name: {node.value}"
        )
        self.edge(parent, current_node_name)

    def __add_literal(self, node: Literal, parent: str) -> None:
        current_node_name = self.__add_node(
            node = node,
            extra_info = f"type: {node.token_type.value} | value: {node.value}"
        )
        self.edge(parent, current_node_name)

    def __add_binary_operation(self, node: BinaryOperation, parent: str) -> None:
        current_node_name = self.__add_node(
            node = node,
            extra_info = f"operator: {node.operator.value}"
        )
        self.edge(parent, current_node_name)
        self.__increase_queues(stack_value = node.left_operand, parent_value = current_node_name)
        self.__increase_queues(stack_value = node.right_operand, parent_value = current_node_name)

    def __add_unary_operation(self, node: UnaryOperation, parent: str) -> None:
        current_node_name = self.__add_node(
            node = node,
            extra_info = f"operator: {node.operator.value}"
        )
        self.edge(parent, current_node_name)
        self.__increase_queues(stack_value = node.operand, parent_value = current_node_name)

    def __add_if_statement(self, node: IfStatement, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)
        self.__increase_queues(stack_value = node.condition, parent_value = current_node_name)
        self.__increase_queues(stack_value = node.block, parent_value = current_node_name)

        if node.else_block:
            self.stack.append(node.else_block)
            self.parents.append(current_node_name)

    def __add_else_statement(self, node: ElseStatement, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)
        self.__increase_queues(stack_value = node.block, parent_value = current_node_name)

    def __add_while_statement(self, node: WhileStatement, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)
        self.__increase_queues(stack_value = node.condition, parent_value = current_node_name)
        self.__increase_queues(stack_value = node.block, parent_value = current_node_name)

    def __add_condition(self, node: Condition, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)
        self.__increase_queues(stack_value = node.value, parent_value = current_node_name)

    def __add_block(self, node: Block, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)

        for statement in node.statements:
            self.__increase_queues(stack_value = statement, parent_value = current_node_name)


    # Nevedeli by sme aplikovat Node visitor design ?
    def __traverse_ast(self) -> None:
        while self.stack:
            current_node = self.stack.popleft()
            parent = self.parents.popleft()

            match current_node.type:
                case NodeVariant.N_PROGRAM:
                    self.__add_program(current_node)
                case NodeVariant.N_ASSIGNMENT_STATEMENT:
                    self.__add_assignment_statement(current_node, parent)
                case NodeVariant.N_VARIABLE:
                    self.__add_variable(current_node, parent)
                case NodeVariant.N_LITERAL:
                    self.__add_literal(current_node, parent)
                case NodeVariant.N_IF_STATEMENT:
                    self.__add_if_statement(current_node, parent)
                case NodeVariant.N_ELSE_STATEMENT:
                    self.__add_else_statement(current_node, parent)
                case NodeVariant.N_BINARY_OPERATION:
                    self.__add_binary_operation(current_node, parent)
                case NodeVariant.N_UNARY_OPERATION:
                    self.__add_unary_operation(current_node, parent)
                case NodeVariant.N_WHILE_STATEMENT:
                    self.__add_while_statement(current_node, parent)
                case NodeVariant.N_CONDITION:
                    self.__add_condition(current_node, parent)
                case NodeVariant.N_BLOCK:
                    self.__add_block(current_node, parent)

    def __generate_node_name(self, node: ASTnode, extra_info: str = '') -> (str, str):
        node_group_count: int = self.nodes.get(str(node))
        id_name = f"{node}_{str(node_group_count + 1) }"
        label_name = f"{node} {extra_info}"
        self.nodes[str(node)] += 1

        return id_name, label_name

    def __add_node(self, node: ASTnode, extra_info: str = '') -> str:
        id_name, label_name = self.__generate_node_name(
            node = node,
            extra_info = extra_info
        )
        self.node(id_name, label_name)
        return id_name

    def visualize_tree(self) -> None:
        self.__traverse_ast()
        self.render('graph', view = True)
