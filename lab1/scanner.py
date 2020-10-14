# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

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
    '<',  # Less than
    '>',  # Greater than
    ':',  # Colon
    ',',  # Coma
    ';',  # Semicolon
    '(', ')',  # Parentheses
    '[', ']',  # Square Brackets
    '{', '}',  # Curly  Brackets
]


# Todo
# Make sure that strings are correctly defined!

# -------------------------------------------------------------
# Tokens
# -------------------------------------------------------------

matrixBinaryOperations = (
    'DOTADD',       # .+
    'DOTSUB',       # .-
    'DOTMUL',       # .*
    'DOTDIV'        # ./
)

assignmentOperations = (
    'ASSIGN',  # =
    'SUBASSIGN',  # -=
    'ADDASSGIN',  # +=
    'DIVASSIGN',  # /=
    'MULTASSIGN'  # \ *=
)


# List of token names.   This is always required
tokens = (
    'INTNUM',       # int
    'FLOATNUM',     # float
)

# -------------------------------------------------------------
# Reserved Tokens
# -------------------------------------------------------------

matrixReservedKeywords = {
    'eye':      'EYE',
    'zeros':    'ZEROS',
    'ones':     'ONES'
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
    'print':    'PRINT'
} + matrixReservedKeywords


# A regular expression rule with some action code

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
