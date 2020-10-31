import ply.yacc as yacc
from ply.yacc import yaccdebug

from Lexer import tokens
from Lexer import literals

parser = None
yaccdebug = True


def LRParser():
    global parser
    if parser is None:
        parser = yacc.yacc(debug=yaccdebug, start='start', outputdir='./out')

    return parser


# -------------------------------------------------------------------
# Parser
# -------------------------------------------------------------------
precedence = (
    # ('nonassoc', 'LESSTHAN', 'GREATERTHAN'),  # Nonassociative operators
    ('left', '+', '-'),
    ('left', '/', '*'),
    ('left', 'TRANSPOSE'),
    ('right', 'UMINUS'),            # Unary minus operator
    # this order is incorrect but for some reason it does parse input..
    ("nonassoc", 'IFx'),
    ("nonassoc", 'EIFx'),
    ("nonassoc", 'ELSE'),
)


def p_start(p):
    """
        start : statements
    """
    pass


def p_statements(p):
    """
        statements : statement
                   | statements statement
    """
    pass


def p_statement(p):
    """
        statement : assignment ';'
                  | print ';'
                  | continue ';'
                  | break ';'
                  | return ';'
                  | if_statement
                  | for
                  | while
    """
    pass


def p_block(p):
    """
        block : nested
    """
    pass


def p_for(p):
    """
        for : FOR ID ASSIGN expression ':' expression nested
    """
    pass


def p_while(p):
    """
        while : WHILE condition nested
    """
    pass


def p_break(p):
    """
        break : BREAK
    """
    pass


def p_return(p):
    """
        return : RETURN expression 
    """
    pass


def p_continue(p):
    """
        continue : CONTINUE
    """
    pass


def p_print(p):
    """
        print : PRINT coma_separated
    """
    pass


def p_coma_separated(p):
    """
        coma_separated : expression 
                       | coma_separated ',' expression
    """
    pass


def p_assignment(p):
    """
        assignment : ID assign_symbol expression
    """
    pass


def p_slice_assignment(p):
    """
        assignment : ID slice assign_symbol expression
    """
    pass


def p_assign(p):
    """
        assign_symbol : ASSIGN
                      | SUBASSIGN
                      | ADDASSIGN
                      | DIVASSIGN
                      | MULTASSIGN
    """
    pass


def p_expression_built_in_function(p):
    """
        expression : built_in_function '(' term ')'
    """
    pass


def p_expression_term(p):
    """
        expression : term
    """
    pass


def p_expression_binary_ops(p):
    """
        expression : expression '+' term
                   | expression '-' term
                   | expression '/' term
                   | expression '*' term
                   | expression EQL term
                   | expression NEQ term
                   | expression GT term
                   | expression GTE term
                   | expression LT term
                   | expression LTE term
    """
    pass


def p_expression_unary(p):
    """
        expression : '-' term %prec UMINUS
    """
    pass


def p_vector_transpose(p):
    """
        vector : ID TRANSPOSE
               | vector TRANSPOSE
    """
    pass


def p_expression_suffix_binary_ops(p):
    """
        expression : ID dot_operation term
                   | vector dot_operation term
    """
    pass


def p_dot_operation(p):
    """
         dot_operation : DOTADD       
                       | DOTSUB       
                       | DOTMUL
                       | DOTDIV
    """
    pass


def p_vector(p):
    """
        vector : '[' vector_contents ']'
    """
    pass


def p_vector_contents(p):
    """
        vector_contents : vector_element
                        | vector_contents ',' vector_element 
    """
    pass


def p_vector_element(p):
    """
        vector_element : term
    """
    pass


def p_slice(p):
    """
        slice : '[' slice_contents ']'
    """
    pass


def p_slice_contents(p):
    """
        slice_contents : range
                       | slice_contents ',' range
    """
    pass


def p_range(p):
    """
        range : term ':' term
              | term ':'
              | ':' term
              | term
    """
    pass


# This generates 2 reduce/shift conflicts but they're resoved by default in favour of shift
# So that way we avoid dangling else problem.
def p_if_statement(p):
    """
        if_statement : if optional_else_ifs optional_else 
    """
    pass


def p_if(p):
    """
        if : IF condition nested %prec IFx
    """
    print('IF!')
    pass


def p_optional_else_ifs(p):
    """
        optional_else_ifs : else_ifs %prec EIFx
                          | 
    """
    pass


def p_else_ifs(p):
    """
        else_ifs : else_if 
                 | else_ifs else_if
    """
    pass


def p_else_if(p):
    """
        else_if : ELSE IF condition nested 
    """
    print('Else IF!')
    pass


def p_optional_else(p):
    """
        optional_else : else
                      |
    """
    pass


def p_else(p):
    """
        else : ELSE nested 
    """
    print('ELSE ')
    pass


def p_condition(p):
    """
        condition : '(' expression ')'
    """


def p_nested(p):
    """
        nested : '{' statements '}'
               | statement
    """
    pass


def p_term(p):
    """
        term : '(' expression ')'
             | vector 
             | INTNUM
             | STR
             | FLOATNUM
             | ID
    """
    pass


def p_built_in_function(p):
    """
        built_in_function : EYE 
                          | ONES
                          | ZEROS
    """
    pass


def p_error(p):
    print('Error!')
    print(p.__dict__)
    pass
