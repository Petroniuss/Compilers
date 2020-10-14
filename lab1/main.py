import sys
import ply.lex as lex

from Lexer import Lexer

if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()

    lexer = Lexer()
    lexer.input(text)  # Give the lexer some input
    lexer.printTokens()
