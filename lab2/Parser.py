import ply.yacc as yacc
from ply.yacc import yaccdebug

from Lexer import tokens
from Lexer import literals

yaccdebug = True


def LRParser():
    return yacc.yacc(debug=yaccdebug, start='start', outputdir='./out')


# -------------------------------------------------------------------
# Parser
# -------------------------------------------------------------------


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
                  | if
                  | for
                  | while
    """
    pass


def p_for(p):
    """
        for : FOR ID ASSIGN expression ':' expression nested
    """
    debug(p[1])
    pass


def p_while(p):
    """
        while : WHILE condition nested
    """
    debug(p[1])
    pass


def p_break(p):
    """
        break : BREAK
    """
    debug(p[1])
    pass


def p_return(p):
    """
        return : RETURN expression
    """
    debug(p[1])
    pass


def p_continue(p):
    """
        continue : CONTINUE
    """
    debug(p[1])
    pass


def p_print(p):
    """
        print : PRINT coma_separated
    """
    debug(p[1])
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


def debug(o):
    print('DEBUG: ' + o.rjust(36))


precedence = (
    ('nonassoc', 'EQL', 'NEQ', 'GT', 'GTE',
        'LT', 'LTE'),
    ('left', '+', '-'),
    ('left', '/', '*'),
    ('left', 'TRANSPOSE'),
    ('right', 'UMINUS'),
    ("nonassoc", 'IFx'),
    ("nonassoc", 'ELSE')
)


def p_if(p):
    """
        if : IF condition nested %prec IFx
           | IF condition nested ELSE nested
    """
    debug('IF!')
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
