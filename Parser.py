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
    ('left', '+', '-'),
    ('left', '/', '*'),
    ('right', 'UMINUS'),
    ("nonassoc", 'IFx'),
    ("nonassoc", 'ELSE'),
    ('left', 'TRANSPOSE'),
    ('nonassoc', 'EQL', 'NEQ', 'GT', 'GTE',
        'LT', 'LTE'),
)


def p_start(p):
    """
        start : statements
    """
    p[0] = Ast('Root', [p[1]])


def p_statements(p):
    """
        statements : statements_list
    """
    p[0] = CodeBlock(p[1])


def p_statements_list(p):
    """
        statements_list : statements_list statement
    """
    p[1].append(p[2])
    p[0] = p[1]


def p_statements_list_single(p):
    """
        statements_list : statement
    """
    p[0] = [p[1]]


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
                  | nested_statements
    """
    p[0] = p[1]


def p_for(p):
    """
        for : FOR ID ASSIGN expression ':' expression nested
    """
    p[0] = For(Identifier(p[2]), p[4], p[6], p[7])


def p_while(p):
    """
        while : WHILE condition nested
    """
    p[0] = While(p[2], p[3])


def p_break(p):
    """
        break : BREAK
    """
    p[0] = Break()


def p_return(p):
    """
        return : RETURN expression
    """
    p[0] = Return(p[2])


def p_continue(p):
    """
        continue : CONTINUE
    """
    p[0] = Continue()


def p_print(p):
    """
        print : PRINT coma_separated
    """
    p[0] = FunctionCall(p[1], p[2])


def p_coma_separated(p):
    """
        coma_separated : coma_separated ',' expression
    """
    p[1].append(p[3])
    p[0] = p[1]


def p_coma_separated_single(p):
    """
        coma_separated : expression
    """
    p[0] = [p[1]]


def p_assignment(p):
    """
        assignment : ID assign_symbol expression
    """
    p[0] = Bind(Identifier(p[1]), p[2], p[3])


def p_slice_assignment(p):
    """
        assignment : ID slice assign_symbol expression
    """
    p[0] = BindWithSlice(Identifier(p[1]), p[2], p[3], p[4])


def p_assign(p):
    """
        assign_symbol : ASSIGN
                      | SUBASSIGN
                      | ADDASSIGN
                      | DIVASSIGN
                      | MULTASSIGN
    """
    p[0] = p[1]


def p_expression_function_call(p):
    """
        expression : built_in_function '(' expression_list ')'
    """
    p[0] = FunctionCall(p[1], p[3])


def p_expression_list(p):
    """
        expression_list : expression_list ',' expression
    """
    p[0] = p[1].append(p[3])


def p_expression_list_single(p):
    """
        expression_list : expression
    """
    p[0] = [p[1]]


def p_expression_term(p):
    """
        expression : term
    """
    p[0] = p[1]


def p_expression_binary_ops(p):
    """
        expression : expression '+' term
                   | expression '-' term
                   | expression '/' term
                   | expression '*' term
    """
    p[0] = BinaryOp(p[2], p[1], p[3])


def p_expression_relational_ops(p):
    """
        expression : expression EQL term
                   | expression NEQ term
                   | expression GT term
                   | expression GTE term
                   | expression LT term
                   | expression LTE term 
    """
    p[0] = RelationalExp(p[2], p[1], p[3])


def p_expression_unary(p):
    """
        expression : '-' term %prec UMINUS
    """
    p[0] = FunctionCall('negative', p[2])


def p_vector_transpose(p):
    """
        expression : expression TRANSPOSE
    """
    p[0] = FunctionCall('transpose', [p[1]])


def p_expression_id_func_call(p):
    """
        expression : ID dot_operation term
    """
    id = Identifier(p[1])
    p[0] = ObjectFunctionCall(id, p[2], [p[3]])


def p_expression_vector_func_call(p):
    """
        expression : vector dot_operation term
    """
    p[0] = ObjectFunctionCall(p[1], p[2], [p[3]])


def p_dot_operation(p):
    """
         dot_operation : DOTADD
                       | DOTSUB
                       | DOTMUL
                       | DOTDIV
    """
    p[0] = p[1]


def p_vector(p):
    """
        vector : '[' vector_contents ']'
    """
    p[0] = Vector(p[2])


def p_vector_empty(p):
    """
        vector : '[' ']'
    """
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


def p_vector_element(p):
    """
        vector_element : term
    """
    p[0] = p[1]


def p_slice(p):
    """
        slice : '[' slice_contents ']'
    """
    p[0] = Slice(p[2])


def p_slice_contents(p):
    """
        slice_contents : slice_contents ',' range
    """
    p[1].append(p[3])
    p[0] = p[1]


def p_slice_contents_single(p):
    """
        slice_contents : range
    """
    p[0] = p[1]


def p_range(p):
    """
        range : expression ':' expression
    """
    p[0] = Range(p[1], p[3])


def p_range_startless(p):
    """
        range : expression ':'
    """
    p[0] = EndlessRange(p[2])


def p_range_endless(p):
    """
        range : ':' expression
    """
    p[0] = StartlessRange(p[2])


def p_range_simple(p):
    """
        range : expression
    """
    p[0] = SimpleRange(p[1])


def p_if(p):
    """
        if : IF condition nested %prec IFx
    """
    p[0] = If(p[2], p[3])


def p_if_else(p):
    """
        if : IF condition nested ELSE nested
    """
    p[0] = IfElse(p[2], p[3], p[5])


def p_condition(p):
    """
        condition : '(' expression ')'
    """
    p[0] = Condition(p[2])


def p_nested(p):
    """
        nested : statement
    """
    xs = [p[1]]
    p[0] = CodeBlock(xs)


def p_nested_statements(p):
    """
        nested_statements : nested_empty
                          | nested_statements_list
    """
    p[0] = CodeBlock(p[1])


def p_nested_statements_list(p):
    """
        nested_statements_list : '{' statements_list '}'
    """
    p[0] = p[2]


def p_nested_statements_empty(p):
    """
        nested_empty : '{' '}'
    """
    p[0] = []


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
