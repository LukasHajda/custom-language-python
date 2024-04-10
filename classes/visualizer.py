import graphviz
from classes.nodes import *
from classes.node_visitor import VisitorVisualizer


class Visualizer(graphviz.Digraph, VisitorVisualizer):
    def __init__(self, root: Program):
        super().__init__()
        self.root: Program = root
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
            Block.__name__: 0,
            PrintStatement.__name__: 0,
            FunctionDeclaration.__name__: 0,
            FunctionCall.__name__: 0,
            Parameter.__name__: 0,
            ParameterList.__name__: 0,
            ArgumentList.__name__: 0,
            Argument.__name__: 0,
            ReturnStatement.__name__: 0
        }

    def __traverse_ast(self) -> None:
        self.add(self.root, parent = None)

    def __generate_node_name(self, node: ASTnode, extra_info: str = '') -> (str, str):
        node_group_count: int = self.nodes.get(str(node))
        id_name = f"{node}_{str(node_group_count + 1)}"
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

    def add_program(self, node: Program, _: str) -> None:
        current_node_name = self.__add_node(node)
        self.add(node.block, parent = current_node_name)

    def add_argument_list(self, node: ArgumentList, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)

        for argument in node.arguments:
            self.add(argument, parent = current_node_name)

    def add_parameter_list(self, node: ParameterList, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)

        for parameter in node.parameters:
            self.add(parameter, parent = current_node_name)

    def add_argument(self, node: Argument, parent: str) -> None:
        current_node_name = self.__add_node(node, extra_info = str(self.nodes.get(str(node)) + 1))
        self.edge(parent, current_node_name)
        self.add(node.value, parent = current_node_name)

    def add_parameter(self, node: Parameter, parent: str) -> None:
        current_node_name = self.__add_node(
            node = node,
            extra_info = f"name: {node.name}"
        )
        self.edge(parent, current_node_name)

    def add_function_call(self, node: FunctionCall, parent: str) -> None:
        current_node_name = self.__add_node(node, extra_info = node.name)
        self.edge(parent, current_node_name)

        self.add(node.argument_list, parent = current_node_name)

    def add_function_declaration(self, node: FunctionDeclaration, parent: str) -> None:
        current_node_name = self.__add_node(node, extra_info = node.name)
        self.edge(parent, current_node_name)

        self.add(node.block, parent = current_node_name)

    def add_return_statement(self, node: ReturnStatement, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)

        self.add(node.value, parent = current_node_name)

    def add_assignment_statement(self, node: AssignmentStatement, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)

        self.add(node.name, parent = current_node_name)
        self.add(node.value, parent = current_node_name)

    def add_variable(self, node: Variable, parent: str) -> None:
        current_node_name = self.__add_node(
            node = node,
            extra_info = f"name: {node.value}"
        )
        self.edge(parent, current_node_name)

    def add_literal(self, node: Literal, parent: str) -> None:
        current_node_name = self.__add_node(
            node = node,
            extra_info = f"type: {node.token_type.value[0]} | value: {node.value}"
        )
        self.edge(parent, current_node_name)

    def add_binary_operation(self, node: BinaryOperation, parent: str) -> None:
        current_node_name = self.__add_node(
            node = node,
            extra_info = f"operator: {node.operator.value[1]}"
        )
        self.edge(parent, current_node_name)
        self.add(node.left_operand, parent = current_node_name)
        self.add(node.right_operand, parent = current_node_name)

    def add_unary_operation(self, node: UnaryOperation, parent: str) -> None:
        current_node_name = self.__add_node(
            node = node,
            extra_info = f"operator: {node.operator.value}"
        )
        self.edge(parent, current_node_name)

        self.add(node.operand, parent = current_node_name)

    def add_if_statement(self, node: IfStatement, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)

        self.add(node.condition, parent = current_node_name)
        self.add(node.block, parent = current_node_name)

        if node.else_block:
            self.add(node.else_block, parent = current_node_name)

    def add_print_statement(self, node: PrintStatement, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)

        self.add(node.value, parent = current_node_name)

    def add_else_statement(self, node: ElseStatement, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)

        self.add(node.block, parent = current_node_name)

    def add_while_statement(self, node: WhileStatement, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)

        self.add(node.condition, parent = current_node_name)
        self.add(node.block, parent = current_node_name)

    def add_condition(self, node: Condition, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)

        self.add(node.value, parent = current_node_name)

    def add_block(self, node: Block, parent: str) -> None:
        current_node_name = self.__add_node(node)
        self.edge(parent, current_node_name)

        for statement in node.statements:
            self.add(statement, parent = current_node_name)

    def visualize_tree(self) -> None:
        self.__traverse_ast()
        self.render('AST', format = 'pdf', cleanup = True)
