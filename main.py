import sys

from Compiler import Compiler
from Failure import formatFailure


def readInput():
    defaultModule = 'slice.m'
    try:
        filename = sys.argv[1] if len(
            sys.argv) > 1 else "./tests/ir/" + defaultModule
        file = open(filename, "r")
    except IOError:
        print(formatFailure("Cannot open {0} file".format(filename)))
        sys.exit(0)

    return file.read(), filename


if __name__ == '__main__':
    sourceCode, filename = readInput()
    Compiler().run(sourceCode, filename)
