from classes.parser import Parser, Scanner, TokenVariant, ASTnode
from classes.visualizer import Visualizer


if __name__ == '__main__':
    scanner: Scanner = Scanner()

    parser: Parser = Parser(scanner)
    root: ASTnode = parser.parse()

    visualizer = Visualizer(root)
    visualizer.visualize_tree()


    # while token.token_variant != TokenVariant.T_EOF:
    #     print(f"TOKEN: {token}")
    #     token = scanner.get_token()


