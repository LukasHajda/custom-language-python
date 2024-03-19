from classes.parser import Parser, Scanner, TokenVariant, Program
from classes.semantic_analysis import SemanticAnalyzer
from classes.visualizer import Visualizer


from classes.scope import Scope


if __name__ == '__main__':

    #TODO: Prepinace na vizualizaciu

    scanner: Scanner = Scanner()

    token = scanner.next_token()
    while token.token_variant != TokenVariant.T_EOF:
        print(token)
        token = scanner.next_token()

    # parser: Parser = Parser(scanner)
    # root: Program = parser.parse()
    # #
    # visualizer = Visualizer(root)
    # visualizer.visualize_tree()


    # TODO: 14.3.2024 si si uvedomil ze Visitor pattern robi postorder prechod.

    # semantic_analyzer = SemanticAnalyzer(root)
    # semantic_analyzer.check()




