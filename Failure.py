class AnsiColor:
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'

    WARNING = '\033[93m'
    FAIL = '\033[91m'

    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    END = '\033[0m'


def formatMessageBoldTitle(msg):
    dashes = 24 * '-'
    return f"{AnsiColor.BOLD}{AnsiColor.GREEN}{dashes} {msg}  {dashes}{AnsiColor.END}"


def formatFailure(msg):
    dashes = 24 * '-'
    return dashes + '\n' + f'{AnsiColor.RED}{msg}{AnsiColor.END}' + '\n'


class ParserError:
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

    def formatted(self):
        return f"{AnsiColor.RED}Syntax Analyzer Error{AnsiColor.END}: '{self.value}' at {self.lineno}"


class TypeError:
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

    def formatted(self):
        return f"{AnsiColor.RED}Type Error{AnsiColor.END}: '{self.value}' at {self.lineno}"


class CodegenError:
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno

    def formatted(self):
        return f"{AnsiColor.RED}Codegen Error{AnsiColor.END}: '{self.value}' at {self.lineno}"


class CompilationFailure(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        dashes = 24 * '-'

        self.message = f"{AnsiColor.BOLD}{dashes} {message}  {dashes}{AnsiColor.END}"
        self.endMessage = f"{AnsiColor.BOLD}{dashes} {len(message) * '-'}  {dashes}{AnsiColor.END}"
        self.errors = errors

    def printTrace(self):
        print(self.message)

        for error in self.errors:
            print(error.formatted())

        print(self.endMessage)
