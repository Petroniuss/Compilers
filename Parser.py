import ply.yacc as yacc
import ply.lex as lex

from ply.yacc import yaccdebug

from Lexer import tokens
from Lexer import literals

import Lexer

from Ast import *
from Failure import CompilationFailure, ParserError

yaccdebug = False
parseErrors = []


def LALRParser(sourceCode):
    lexer = lex.lex(module=Lexer)
    parser = yacc.yacc(debug=yaccdebug, start='start', outputdir='./out')

    ast = parser.parse(sourceCode, lexer=lexer, tracking=True)

    if len(parseErrors) > 0:
        raise CompilationFailure('Parsing failed', parseErrors)

    return ast


# -------------------------------------------------------------
# ------------- Syntax Analyzer -------------------------------
# -------------------------------------------------------------

precedence = (
    ("nonassoc", 'IFx'),
    ("nonassoc", 'ELSE'),
    ('nonassoc', 'EQL', 'NEQ', 'GT', 'GTE',
        'LT', 'LTE'),
    ('left', '+', '-'),
    ('left', '/', '*'),
    ('right', 'UMINUS'),
    ('left', 'TRANSPOSE'),
)


def p_start(p):
    """
        start : statements
    """
    p[0] = Ast('Root', [CodeBlock(p[1])], lineno=p.lineno(1))


def p_statements(p):
    """
        statements : statements statement
    """
    p[1].append(p[2])
    p[0] = p[1]


def p_statements_list_single(p):
    """
        statements : statement
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
        for : FOR ID ASSIGN range_closed statement
    """
    p[0] = For(Identifier(p[2], lineno=p.lineno(2)), p[4],
               CodeBlock([p[5]]), lineno=p.lineno(1))


def p_while(p):
    """
        while : WHILE condition statement
    """
    p[0] = While(p[2], CodeBlock([p[3]]), lineno=p.lineno(1))


def p_break(p):
    """
        break : BREAK
    """
    p[0] = Break(lineno=p.lineno(1))


def p_return(p):
    """
        return : RETURN expression
    """
    p[0] = Return(p[2], lineno=p.lineno(1))


def p_continue(p):
    """
        continue : CONTINUE
    """
    p[0] = Continue(lineno=p.lineno(1))


def p_print(p):
    """
        print : PRINT expression_list
    """
    p[0] = FunctionCall(p[1], p[2], lineno=p.lineno(1))


def p_assignment(p):
    """
        assignment : ID assign_symbol expression
    """
    idd = Identifier(p[1], lineno=p.lineno(1))
    exp = p[3]
    opp = p[2]
    # We break down '+=' into id = (id + exp)
    if p[2] != '=':
        opp = p[2][0]  # in order to get'+' out of '+='
        exp = BinaryOp(opp, idd, exp, lineno=p.lineno(2))

    p[0] = Bind(idd, '=', exp, lineno=p.lineno(1))


def p_slice_assignment(p):
    """
        assignment : ID slice assign_symbol expression
    """
    idd = Identifier(p[1], p.lineno(1))
    slicedVector = SlicedVector(idd, p[2], lineno=p.lineno(1))
    exp = p[4]

    opp = p[3]
    if p[3] != '=':
        opp = p[3][0]
        exp = BinaryOp(opp, slicedVector, exp)

    p[0] = BindWithSlice(slicedVector, '=', exp, lineno=p.lineno(1))


def p_assign(p):
    """
        assign_symbol : ASSIGN
                      | SUBASSIGN
                      | ADDASSIGN
                      | DIVASSIGN
                      | MULTASSIGN
    """
    p[0] = p[1]


def p_expression_list(p):
    """
        expression_list : expression_list ',' expression
    """
    p[1].append(p[3])
    p[0] = p[1]


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


def p_expression_function_call(p):
    """
        expression : built_in_function '(' expression_list ')'
    """
    p[0] = FunctionCall(p[1], p[3], lineno=p.lineno(1))


def p_expression_binary_ops(p):
    """
        expression : expression '+' term
                   | expression '-' term
                   | expression '/' term
                   | expression '*' term
    """
    p[0] = BinaryOp(p[2], p[1], p[3], lineno=p.lineno(2))


def p_expression_relational_ops(p):
    """
        expression : expression EQL term
                   | expression NEQ term
                   | expression GT term
                   | expression GTE term
                   | expression LT term
                   | expression LTE term 
    """
    p[0] = RelationalExp(p[2], p[1], p[3], lineno=p.lineno(2))


def p_expression_id_slice(p):
    """
        expression : ID slice
    """
    idd = Identifier(p[1], p.lineno(1))
    p[0] = SlicedVector(idd, p[2], lineno=p.lineno(1))


def p_expression_unary(p):
    """
        expression : '-' term %prec UMINUS
    """
    p[0] = FunctionCall('negative', [p[2]], lineno=p.lineno(1))


def p_vector_transpose(p):
    """
        expression : expression TRANSPOSE
    """
    p[0] = FunctionCall('transpose', [p[1]], lineno=p.lineno(1))


def p_expression_id_func_call(p):
    """
        expression : ID dot_operation term
    """
    id = Identifier(p[1])
    p[0] = FunctionCall(p[2], [id, p[3]], lineno=p.lineno(2))


def p_expression_vector_func_call(p):
    """
        expression : vector dot_operation term
    """
    p[0] = FunctionCall(p[2], [p[1], p[3]], lineno=p.lineno(2))


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
    p[0] = Vector(p[2], lineno=p.lineno(1))


def p_vector_empty(p):
    """
        vector : '[' ']'
    """
    p[0] = emptyVector(lineno=p.lineno(1))


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
    p[0] = p[2]


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
    p[0] = [p[1]]


def p_range(p):
    """
        range : range_closed
    """
    p[0] = p[1]


def p_range_closed(p):
    """
        range_closed : expression ':' expression
    """
    p[0] = Range(p[1], p[3], lineno=p.lineno(2))


def p_range_startless(p):
    """
        range : expression ':'
    """
    p[0] = EndlessRange(p[2], lineno=p.lineno(2))


def p_range_endless(p):
    """
        range : ':' expression
    """
    p[0] = FromStartRange(p[2], lineno=p.lineno(1))


def p_range_simple(p):
    """
        range : expression
    """
    p[0] = SimpleRange(p[1], lineno=p.lineno(1))


def p_if(p):
    """
        if : IF condition statement %prec IFx
    """
    p[0] = If(p[2], CodeBlock([p[3]]), lineno=p.lineno(1))


def p_if_else(p):
    """
        if : IF condition statement ELSE statement
    """
    p[0] = IfElse(p[2], CodeBlock([p[3]]),
                  CodeBlock([p[5]]), lineno=p.lineno(1))


def p_condition(p):
    """
        condition : '(' expression ')'
    """
    p[0] = p[2]


def p_nested_statements(p):
    """
        nested_statements : nested_empty
                          | nested_statements_list
    """
    p[0] = CodeBlock(p[1])


def p_nested_statements_list(p):
    """
        nested_statements_list : '{' statements '}'
    """
    p[0] = p[2]

# -------------------------------------
#      ----- Primitives -----
# -------------------------------------


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
    p[0] = Int(p[1], lineno=p.lineno(1))


def p_term_primitive_float(p):
    """
        term : FLOATNUM
    """
    p[0] = Float(p[1], lineno=p.lineno(1))


def p_term_primitive_str(p):
    """
        term : STR
    """
    p[0] = String(p[1], lineno=p.lineno(1))


def p_term_id(p):
    """
        term : ID
    """
    p[0] = Identifier(p[1], lineno=p.lineno(1))


def p_built_in_function(p):
    """
        built_in_function : EYE
                          | ONES
                          | ZEROS
    """
    p[0] = p[1]
    pass


def p_error(p):
    err = ParserError(p.value, p.lineno)
    parseErrors.append(err)
