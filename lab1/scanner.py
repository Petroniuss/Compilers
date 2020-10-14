import ply.lex as lex

# -------------------------------------------------------------
# Module contains implementation of a tokenizer.
# -------------------------------------------------------------

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

reserved = {
    'if':       'IF',
    'then':     'THEN',
    'else':     'ELSE',
    'for':      'FOR',
    'while':    'WHILE',
    'break':    'BREAK',
    'continue': 'CONTINUE',
    'return':   'RETURN',
} + specialFunctons


# -------------------------------------------------------------
# Tokens
# -------------------------------------------------------------

matrixBinaryOperations = (
    'DOTADD',       # .+
    'DOTSUB',       # .-
    'DOTMUL',       # .*
    'DOTDIV'        # ./
)

matrixOperations = (
    'TRANSPOSE',  # '
    'SLICE',   # :
)

assignmentOperations = (
    'ASSIGN',  # =
    'SUBASSIGN',  # -=
    'ADDASSGIN',  # +=
    'DIVASSIGN',  # /=
    'MULTASSIGN'  # \ *=
)

relationalOperators = (
    'LT',  # <
    'GT',  # >
    'LTE',  # <=
    'GTE',  # >=
    'EQL',  # ==
    'NEQ',  # \ !=
)

numbers = (
    'INTNUM',       # int
    'FLOATNUM'     # float
)

strings = ('STR')

identifier = ('ID')

# List of token names.   This is always required
tokens = \
    matrixBinaryOperations +\
    matrixOperations +\
    assignmentOperations +\
    relationalOperators +\
    numbers +\
    strings +\
    identifier

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


t_TRANSPOSE = r'\''
t_SLICE = r':',

t_ASSIGN = r'='
t_SUBASSIGN = r'-='
t_ADDASSGIN = r'+='
t_DIVASSIGN = r'/=',
t_MULTASSIGN = r'*='

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
    t.value = t.value[1: len(t.value) - 1]
    return t


def t_INTNUM(t):
    r'[-+]?(\d+)'  # It allows for leading zeros.
    t.value = int(t.value)
    return t


def t_FLOATNUM(t):
    # It also allows for leading zeros and for scientific notation.
    r'[-+]?(\d+(\.\d*)|\.\d+)([eE][-+]?\d+)?'
    t.value = float(t.value)
    return t


def t_newline(t):
    # Define a rule so we can track line numbers
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_COMMENT(t):
    # This one needs to be placed at the bottom so that it does not interfere with others!
    r'#.*'
    pass


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Build the lexer
lexer = lex.lex()
