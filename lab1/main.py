import sys
import ply.lex as lex

from scanner import Scanner

if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()

    # Give the lexer some input
    lexer.input(text)

    # Tokenize
    lexer.test()
