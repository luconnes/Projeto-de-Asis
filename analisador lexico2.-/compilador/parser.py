import ply.yacc as yacc
from lexer import tokens

# Tabela de símbolos
symbol_table = {}

# Regras de precedência para resolver ambiguidades
precedence = (('left', 'OPERADOR'), )

# Definições de regras da gramática

def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : declaration
                 | expression_statement
                 | compound_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration : INT IDENTIFICADOR ASSIGN expression SIMBOLO
                   | FLOAT IDENTIFICADOR ASSIGN expression SIMBOLO
                   | CHAR IDENTIFICADOR ASSIGN expression SIMBOLO
                   | STRING IDENTIFICADOR ASSIGN expression SIMBOLO
                   | INT IDENTIFICADOR SIMBOLO
                   | FLOAT IDENTIFICADOR SIMBOLO
                   | CHAR IDENTIFICADOR SIMBOLO
                   | STRING IDENTIFICADOR SIMBOLO'''
    if p[2] in symbol_table:
        raise Exception(f"Erro semântico: Variável '{p[2]}' já declarada.")
    if len(p) == 6:  # Caso de declaração com atribuição
        symbol_table[p[2]] = p[1].lower()
        p[0] = ('declaration', p[1], p[2], p[4])
    else:  # Caso de declaração simples
        symbol_table[p[2]] = p[1].lower()
        p[0] = ('declaration', p[1], p[2])

def p_expression_statement(p):
    '''expression_statement : expression SIMBOLO '''
    p[0] = ('expression_statement', p[1])

def p_compound_statement(p):
    '''compound_statement : LBRACE statement_list RBRACE '''
    p[0] = ('compound_statement', p[2])

def p_selection_statement(p):
    '''selection_statement : IF SIMBOLO expression SIMBOLO statement ELSE statement
                           | IF SIMBOLO expression SIMBOLO statement'''
    if len(p) == 8:
        p[0] = ('if_else_statement', p[3], p[5], p[7])
    else:
        p[0] = ('if_statement', p[3], p[5])

def p_iteration_statement(p):
    '''iteration_statement : WHILE SIMBOLO expression SIMBOLO statement'''
    p[0] = ('while_statement', p[3], p[5])

def p_jump_statement(p):
    '''jump_statement : RETURN expression SIMBOLO'''
    p[0] = ('jump_statement', p[1], p[2])

def p_expression(p):
    '''expression : assignment_expression
                  | function_call
                  | term'''
    p[0] = p[1]

def p_assignment_expression(p):
    '''assignment_expression : IDENTIFICADOR ASSIGN expression'''
    if p[1] not in symbol_table:
        raise Exception(f"Erro semântico: Variável '{p[1]}' não declarada.")
    variable_type = symbol_table[p[1]]
    expression_type = p[3][1]
    if variable_type != expression_type:
        raise Exception(f"Erro semântico: Tipo de {p[1]} ({variable_type}) não corresponde ao tipo da expressão ({expression_type}).")
    p[0] = ('assignment', p[1], p[2], p[3])

def p_term(p):
    '''term : NUMERO_INTEIRO
            | NUMERO_DECIMAL
            | STRING
            | CHARACTER'''
    if isinstance(p[1], int):
        p[0] = ('term', 'int', p[1])
    elif isinstance(p[1], float):
        p[0] = ('term', 'float', p[1])
    elif isinstance(p[1], str) and len(p[1]) == 1:
        p[0] = ('term', 'char', p[1])
    else:
        p[0] = ('term', 'string', p[1])

def p_function_call(p):
    '''function_call : IDENTIFICADOR SIMBOLO SIMBOLO
                     | IDENTIFICADOR SIMBOLO expression_list SIMBOLO'''
    if len(p) == 4:
        p[0] = ('function_call', p[1], [])
    else:
        p[0] = ('function_call', p[1], p[3])

def p_expression_list(p):
    '''expression_list : expression
                       | expression_list SIMBOLO expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_error(p):
    if p:
        print(f"Erro de sintaxe no token '{p.value}', linha {p.lineno}")
    else:
        print("Erro de sintaxe no final do arquivo")

# Criar o parser
parser = yacc.yacc()
