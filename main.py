from classes.parser import Parser, Scanner, TokenVariant, ASTnode
from classes.visualizer import Visualizer


if __name__ == '__main__':
    scanner: Scanner = Scanner()

    # token = scanner.next_token()
    # while token.token_variant != TokenVariant.T_EOF:
    #     print(token)
    #     token = scanner.next_token()

    parser: Parser = Parser(scanner)
    root: ASTnode = parser.parse()

    visualizer = Visualizer(root)
    visualizer.visualize_tree()


