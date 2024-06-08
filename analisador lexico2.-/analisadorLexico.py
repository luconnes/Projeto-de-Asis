from ply.lex import lex

# Lista de tokens
tokens = (
    'PALAVRA_CHAVE',
    'OPERADOR',
    'SIMBOLO_ESPECIAL',
    'NUMERO_INTEIRO',
    'NUMERO_DECIMAL',
    'IDENTIFICADOR',
    'STRING',
    'COMENTARIO',
)

# Expressões regulares para os tokens
t_COMENTARIO = r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
t_OPERADOR = r'\+\+|--|<=|>=|==|!=|&&|\|\||=|<|>|\+|-|\*|/|%'
t_SIMBOLO_ESPECIAL = r'[\(\)\[\]\{\},;.]'
t_NUMERO_DECIMAL = r'\b\d+\.\d+\b'
t_NUMERO_INTEIRO = r'\b\d+\b'
t_STRING = r'"([^"\\]*(\\.[^"\\]*)*)"'
t_IDENTIFICADOR = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'

# Ignorar espaços em branco e tabs
t_ignore = ' \t'

# Contador de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratar erro de caracteres não reconhecidos
def t_error(t):
    print(f"Caractere não reconhecido: '{t.value[0]}'", f"na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir o analisador léxico
analise_lexica = lex()

# Função para analisar o código
def analisador_lexico(codigo):
    analise_lexica.input(codigo)
    while True:
        token = analise_lexica.token()
        if not token:
            break
        print(token)

# Exemplo de uso do analisador léxico
with open("input.txt") as file:
    codigo_fonte = file.read()

analisador_lexico(codigo_fonte)
