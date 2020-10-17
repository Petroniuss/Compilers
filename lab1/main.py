import sys
import ply.lex as lex

from Lexer import Lexer


def printFormatted(xs):
    for x in xs:
        print(x.formatted())


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()

    lexer = Lexer() \
        .input(text) \
        .parseInput() \

    tokens = lexer.tokens()
    errors = lexer.errors()

    # For now we're just printing parsed tokens and lexems
    if len(errors) > 0:
        print('Invalid input!')
        printFormatted(errors)
    else:
        printFormatted(tokens)
