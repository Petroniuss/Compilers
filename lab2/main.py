import sys
import ply.lex as lex

from Lexer import Lexer
from Parser import LRParser


def printFormatted(xs):
    for x in xs:
        print(x.formatted())


def lexme(text):
    errors, tokens = Lexer() \
        .input(text) \
        .parseInput() \

    # For now we're just printing parsed tokens and lexems
    if len(errors) > 0:
        print('Invalid input!')
        printFormatted(errors)
    else:
        printFormatted(tokens)


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
    parser.parse(text)
