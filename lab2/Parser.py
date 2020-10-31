import ply.yacc as yacc
from ply.yacc import yaccdebug

from Lexer import tokens
from Lexer import literals

from Ast import *

yaccdebug = True


def LRParser():
    return yacc.yacc(debug=yaccdebug, start='start', outputdir='./out')


# -------------------------------------------------------------------
# Parser
# -------------------------------------------------------------------

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
        expression : built_in_function '(' term_list ')'
    """
    pass


def p_term_list(p):
    """
        term_list : term
                  | term_list ',' term
    """


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
               |  '[' ']'
    """
    if len(p) == 4:
        p[0] = Vector(p[2])
    else:
        p[0] = emptyVector()


def p_vector_contents_list(p):
    """
        vector_contents : vector_contents ',' vector_element
    """
    p[1].append(p[3])
    p[0] = p[1]


def p_vector_contents_single(p):
    """
        vector_contents : vector_element
    """
    p[0] = [p[1]]
    pass


def p_vector_element(p):
    """
        vector_element : term
    """
    p[0] = p[1]
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


def debug(header, info):
    print(header.ljust(36) + str(info))


def p_if(p):
    """
        if : IF condition nested %prec IFx
           | IF condition nested ELSE nested
    """
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
    """
    p[0] = p[2]


def p_term_vector(p):
    """
        term : vector
    """
    p[0] = p[1]


def p_term_primitive_int(p):
    """
        term : INTNUM
    """
    p[0] = Int(p[1])


def p_term_primitive_float(p):
    """
        term : FLOATNUM
    """
    p[0] = Float(p[1])


def p_term_primitive_str(p):
    """
        term : STR
    """
    p[0] = String(p[1])


def p_term_id(p):
    """
        term : ID
    """
    p[0] = Identifier(p[1])


def p_built_in_function(p):
    """
        built_in_function : EYE
                          | ONES
                          | ZEROS
    """
    p[0] = p[1]
    pass


def p_error(p):
    print('Error!')
    print(p.__dict__)
    pass
