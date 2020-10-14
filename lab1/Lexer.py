import ply.lex as lex

# -------------------------------------------------------------
# Module contains implementation of a Lexer aka Scanner.
# -------------------------------------------------------------


class Lexer:
    def __init__(self, **kwargs):
        self.lexer = lex.lex()

    def input(self, text):
        self.text = text
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()

    def printTokens(self):
        while True:
            tok = self.token()
            if not tok:
                break    # No more input
            print(formatToken(tok, tokenColumnNo=findColumn(self.text, tok)))


def formatToken(tok, tokenColumnNo=None):
    linenoStr = f'({tok.lineno}):'.ljust(8)
    if tokenColumnNo is not None:
        linenoStr = f'({tok.lineno}, {tokenColumnNo}):'.ljust(10)
    return linenoStr + ' ' + f'{tok.type}( {tok.value} )'


def findColumn(text, token):
    lineStart = text.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - lineStart) + 1

# -------------------------------------------------------------
# Literals
# -------------------------------------------------------------


# Todo: move them to tokens since I don't like the output..
binaryOperators = [
    '+',  # Plus
    '-',  # Minus
    '*',  # Times
    '/',  # Divde
]

literals = binaryOperators + [
    ':',  # Colon
    ',',  # Coma
    ';',  # Semicolon
    '(', ')',  # Parentheses
    '[', ']',  # Square Brackets
    '{', '}',  # Curly  Brackets
]

# -------------------------------------------------------------
# Reserved Tokens
# -------------------------------------------------------------

specialFunctons = {
    'eye':      'EYE',
    'zeros':    'ZEROS',
    'ones':     'ONES',
    'print':    'PRINT'
}

typicalLanguageKeywords = {
    'if':       'IF',
    'then':     'THEN',
    'else':     'ELSE',
    'for':      'FOR',
    'while':    'WHILE',
    'break':    'BREAK',
    'continue': 'CONTINUE',
    'return':   'RETURN',
}

reserved = {}
reserved.update(specialFunctons)
reserved.update(typicalLanguageKeywords)


# -------------------------------------------------------------
# Tokens
# -------------------------------------------------------------

matrixBinaryOperations = [
    'DOTADD',       # .+
    'DOTSUB',       # .-
    'DOTMUL',       # .*
    'DOTDIV'        # ./
]

matrixOperations = [
    'TRANSPOSE',  # '
    'SLICE'   # :
]

assignmentOperations = [
    'ASSIGN',  # =
    'SUBASSIGN',  # -=
    'ADDASSGIN',  # +=
    'DIVASSIGN',  # /=
    'MULTASSIGN'  # \ *=
]

relationalOperators = [
    'LT',  # <
    'GT',  # >
    'LTE',  # <=
    'GTE',  # >=
    'EQL',  # ==
    'NEQ',  # \ !=
]

primitives = [
    'INTNUM',       # int
    'FLOATNUM',     # float
    'STR'
]


identifier = ['ID']

# List of token names.   This is always required
tokens = \
    matrixBinaryOperations +\
    matrixOperations +\
    assignmentOperations +\
    relationalOperators +\
    primitives +\
    identifier +\
    list(reserved.values())

# -------------------------------------------------------------
# Matching Rules
# -------------------------------------------------------------
# Note:
# - maximal is match is chosen (pattern which consumes the most characters)
# - patterns appearing closer take precedence:
#   - functions defined higher in this file,
#   - strings are sorted based on pattern length.


# Make sure that variables such as ___ are okay.
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


t_DOTADD = r'\.\+'       # .+
t_DOTSUB = r'\.-'       # .-
t_DOTMUL = r'\.\*'       # .*
t_DOTDIV = r'\./'       # ./

t_TRANSPOSE = r'\''
t_SLICE = r':'

t_ASSIGN = r'='
t_SUBASSIGN = r'-='
t_ADDASSGIN = r'\+='
t_DIVASSIGN = r'/='
t_MULTASSIGN = r'\*='

t_LT = r'<'
t_GT = r'>'
t_LTE = r'<='
t_GTE = r'>='
t_EQL = r'=='
t_NEQ = r'!='


def t_STR(t):
    # Todo
    # Make sure that strings are correctly defined!
    # This one might cause problems
    r'".*"'
    t.value = str(t.value[1: len(t.value) - 1])
    return t


def t_FLOATNUM(t):
    # It also allows for leading zeros and for scientific notation.
    r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'[-+]?(\d+)'  # It allows for leading zeros.
    t.value = int(t.value)
    return t


def t_newline(t):
    # Define a rule so we can track line numbers
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_COMMENT(t):
    # This one needs to be placed at the bottom so that it does not interfere with others!
    r'\#.*'
    pass


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_eof(t):
    return None


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'
