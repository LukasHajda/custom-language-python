from classes.parser import Parser, Scanner, TokenVariant, Program
from classes.semantic_static_analysis import SemanticAnalyzer
from classes.visualizer import Visualizer
from classes.interpreter import Interpreter


from classes.scope import Scope


if __name__ == '__main__':

    # Lexical analysis
    scanner: Scanner = Scanner()

    # Syntax analysis
    parser: Parser = Parser(scanner)
    root: Program = parser.parse()

    # Visualiser
    visualizer = Visualizer(root)
    visualizer.visualize_tree()

    # Semantic analysis
    semantic_analyzer = SemanticAnalyzer(root)
    semantic_analyzer.check()

    # Evaluation
    interpreter = Interpreter(root)
    interpreter.start_evaluation()






