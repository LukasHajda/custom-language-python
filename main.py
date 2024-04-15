import os
os.environ["PATH"] += os.pathsep + '<cesta ku graphviz bin prečinku>'
# Príklad: os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz/bin/'

from classes.parser import Parser, Scanner, TokenVariant, Program
from classes.semantic_static_analysis import SemanticAnalyzer
from classes.visualizer import Visualizer
from classes.interpreter import Interpreter



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






