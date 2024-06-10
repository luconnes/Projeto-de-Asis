import lexer
import parser
from parser import symbol_table

if __name__ == "__main__":
    # Abrir o arquivo de entrada e ler o código-fonte
    with open("input.txt", "r") as file:
        source_code = file.read()

    # Realizar análise léxica
    lexer.lexer.input(source_code)

    # Iterar sobre os tokens resultantes da análise léxica
    for token in lexer.lexer:
        print(token)

    # Tentar realizar análise sintática e semântica
    try:
        result = parser.parser.parse(source_code, lexer=lexer.lexer)
        print("Análise sintática e semântica completa.")

        # Exibir a árvore de análise
        print("Árvore de Análise:")
        print(result)

        # Exibir a tabela de símbolos
        print("Tabela de Símbolos:")
        for name, type in symbol_table.items():
            print(f"{name} : {type}")
    except Exception as e:
        print(f"Erro: {e}")

