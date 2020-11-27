import sys
import ply.lex as lex

from Lexer import Lexer
from Parser import LRParser
from TreePrinter import TreePrinter

import Parser


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "./tests/example.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    lexer = Lexer()
    parser = LRParser()

    text = file.read()
    ast = parser.parse(text, lexer=lexer.lex())
    if Parser.parseError is True:
        print('Error during creating ast..')
    else:
        # We can print tree in two formats
        ast.printTree()
        ast.printFancyTree()
