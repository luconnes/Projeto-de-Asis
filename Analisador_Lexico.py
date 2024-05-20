import re

def analisador_lexico(codigo):
    padrao_palavras_chave = r'\b(int|float|double|char|boolean|void|def|input|if|else|while|for|switch|case|default|break|continue|return|struct|println|main)\b'
    padrao_operadores = r'(\+\+|--|<=|>=|==|!=|&&|\|\||=|<|>|\+|-|\*|/|%)'
    padrao_simbolos_especiais = r'[\(\)\[\]\{\},;.]'
    padrao_numero_inteiro = r'\b\d+\b'
    padrao_numero_decimal = r'\b\d+\.\d+\b'
    padrao_identificador = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
    padrao_string = r'"([^"\\]*(\\.[^"\\]*)*)"'
    padrao_comentario = r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
    
    tokens = []
    IDs = []
    linhas = codigo.split('\n')
    
    padrao_lexemas = re.compile(r'(\b\w+\b|==|!=|<=|>=|\+\+|--|&&|\|\||[+\-/%=(){}\[\],;.]|"(?:\\.|[^"\\])*"|\'.*?\')')

    for num_linha, linha in enumerate(linhas, start=1):
        lexemas = padrao_lexemas.findall(linha)
        
        for token in lexemas:
            if(re.match(padrao_palavras_chave, token)):
                print("Palavra chave:",token)
            elif(re.match(padrao_operadores,token)):
                print("Operador:",token)
            elif(re.match(padrao_comentario, token)):
                print("Comentário:", token)
                
            elif(re.match(padrao_simbolos_especiais,token)):
                print("Simbolo especial:",token)
                
            elif(re.match(padrao_identificador,token)):
                if token not in IDs:
                    IDs.append(token)
                    print("Identificador:",token)
                elif token in IDs:
                    print("ID", IDs.index(token))
                
            elif(re.match(padrao_numero_decimal,token)):
                print("Numero decimal", token)
            elif(re.match(padrao_numero_inteiro,token)):
                print("Numero inteiro:",token)
            elif(re.match(padrao_string,token)):
                print("String:",token)
            else:
                print("Error")
                break
    
    return tokens

# Exemplo de uso do analisador léxico
with open("input.txt") as file:
    codigo_fonte = file.read()

tokens = analisador_lexico(codigo_fonte)
for token in tokens:
    print(token)
