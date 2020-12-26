import sys

from Compiler import Compiler


def readFile():
    defaultModule = 'foo.m'
    try:
        filename = sys.argv[1] if len(
            sys.argv) > 1 else "./tests/ir/" + defaultModule
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    return file.read()


if __name__ == '__main__':
    sourceCode = readFile()
    Compiler().run(sourceCode)
