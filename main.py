from classes.parser import Parser, Scanner, TokenVariant, Program
from classes.semantic import SemanticAnalyzer
from classes.visualizer import Visualizer


if __name__ == '__main__':
    scanner: Scanner = Scanner()

    # token = scanner.next_token()
    # while token.token_variant != TokenVariant.T_EOF:
    #     print(token)
    #     token = scanner.next_token()

    parser: Parser = Parser(scanner)
    root: Program = parser.parse()

    visualizer = Visualizer(root)
    visualizer.visualize_tree()

    semantic_analyzer = SemanticAnalyzer(root)
    semantic_analyzer.check()


