import ply.lex as lex

# Lista de tokens
tokens = [
    'OPERADOR',
    'IDENTIFICADOR',
    'SIMBOLO',
    'NUMERO_DECIMAL',
    'NUMERO_INTEIRO',
    'STRING',
    'CHARACTER',
    'ASSIGN',
    'LBRACE',  # Adicionando delimitadores específicos '{'
    'RBRACE', #adicionado delimitdaores especificos '}'
    'INT',
    'BOOLEAN',
    'VOID',
    'IF',
    'ELSE',
    'WHILE',
    'FOR',
    'RETURN',
    'PRINTF',
    'MAIN',
    'DOUBLE',
    'FLOAT',
    'CHAR',
]

# Expressões regulares para tokens simples
t_ignore = ' \t'

t_OPERADOR = r'\+\+|--|<=|>=|==|!=|&&|\|\||<|>|\+|-|\*|/|%'

t_ASSIGN = r'='

# Delimitadores específicos
t_LBRACE = r'\{'
t_RBRACE = r'\}'

# Outros símbolos podem ser agrupados juntos
t_SIMBOLO = r'[\(\)\[\],;]'

# Funções para tokens complexos
def t_NUMERO_DECIMAL(t):
    r'\b\d+\.\d+\b'
    t.value = float(t.value)
    return t

def t_NUMERO_INTEIRO(t):
    r'\b\d+\b'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"([^"\\]*(\\.[^"\\]*)*)"'
    t.value = t.value[1:-1]  # Remove as aspas
    return t

def t_CHARACTER(t):
    r"'.'"
    t.value = t.value[1:-1]  # Remove as aspas
    return t

# Palavras-chave
palavras_chave = {
    'main': 'MAIN',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'boolean': 'BOOLEAN',
    'void': 'VOID',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'printf': 'PRINTF',
    'return': 'RETURN',
}

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = palavras_chave.get(t.value, 'IDENTIFICADOR')  # Verifica se é uma palavra-chave
    return t

def t_COMENTARIO(t):
    r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
    t.lexer.lineno += t.value.count('\n')
    pass  # Ignorar comentários de bloco

def t_COMENTARIO_LINHA(t):
    r'//.*'
    pass  # Ignorar comentários de linha

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

# Criar analisador léxico
lexer = lex.lex()