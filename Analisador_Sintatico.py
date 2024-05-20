import Analisador_Lexico
class Parser:
    def __init__(self, tokens):  # Corrigindo o nome do método
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        self.programa()

    def programa(self):
        while self.pos < len(self.tokens):
            self.declaracao()

    def declaracao(self):
        if self.match('PALAVRA_CHAVE', 'int', 'float', 'double', 'char', 'boolean'):
            self.declaracao_variavel()
        elif self.match('PALAVRA_CHAVE', 'void'):
            if self.match('PALAVRA_CHAVE', 'void', 'def'):
                self.declaracao_funcao()
            else:
                self.error("Esperado declaração de função ou variável após 'void'")
        elif self.match('IDENTIFICADOR'):
            self.declaracao_variavel()  # Permitir declaração de variável sem palavra-chave de tipo
        elif self.match('PALAVRA_CHAVE', 'struct'):
            self.declaracao_estrutura()
        elif self.match('COMENTARIO'):
            self.advance()
        else:
            self.error("Esperado declaração")


    def declaracao_variavel(self):
        self.tipo()
        self.consume('IDENTIFICADOR', mensagem="Esperado identificador")
        if self.match('OPERADOR', '='):
            self.advance()
            self.expressao()
        self.consume('SIMBOLO', ';', mensagem="Esperado ';' após a declaração de variável")


    def tipo(self):
        if self.match('PALAVRA_CHAVE', 'int', 'float', 'double', 'char', 'boolean', 'void'):
            self.advance()
        else:
            self.error("Esperado tipo")

    def declaracao_funcao(self):
        self.tipo()
        if not self.match('PALAVRA_CHAVE', 'void'):
            self.consume('IDENTIFICADOR', mensagem="Esperado identificador da função")
        self.consume('SIMBOLO', '(', mensagem="Esperado '('")
        self.parametros()
        self.consume('SIMBOLO', ')', mensagem="Esperado ')'")
        self.bloco()



    def parametros(self):
        if not self.check('SIMBOLO', ')'):
            self.parametro()
            while self.match('SIMBOLO', ','):
                self.advance()
                self.parametro()

    def parametro(self):
        self.tipo()
        self.consume('IDENTIFICADOR', mensagem="Esperado identificador")

    def bloco(self):
        self.consume('SIMBOLO', '{', mensagem="Esperado '{'")
        while not self.check('SIMBOLO', '}') and self.pos < len(self.tokens):
            self.declaracao()
        self.consume('SIMBOLO', '}', mensagem="Esperado '}'")

    def expressao(self):
        if self.match('IDENTIFICADOR') or self.match('NUMERO_INTEIRO') or self.match('NUMERO_DECIMAL'):
            self.advance()
        else:
            self.error("Esperado expressão")

    def declaracao_estrutura(self):
        self.consume('PALAVRA_CHAVE', 'struct', mensagem="Esperado 'struct'")
        self.consume('IDENTIFICADOR', mensagem="Esperado identificador")
        self.consume('SIMBOLO', '{', mensagem="Esperado '{'")
        while not self.check('SIMBOLO', '}') and self.pos < len(self.tokens):
            self.declaracao_variavel()
        self.consume('SIMBOLO', '}', mensagem="Esperado '}'")
        self.consume('SIMBOLO', ';', mensagem="Esperado ';'")

    def match(self, tipo, *valores):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token[0] == tipo and (not valores or token[1] in valores):
                return True
            elif tipo == 'IDENTIFICADOR' and token[0] == 'IDENTIFICADOR':
                return True
        return False

    def consume(self, tipo, valor=None, mensagem=None):
        if self.match(tipo, valor):
            self.advance()
        else:
            self.error(mensagem or f"Esperado {tipo} {valor}")

    def check(self, tipo, valor=None):
        return self.match(tipo, valor)

    def advance(self):
        if self.pos < len(self.tokens):
            self.pos += 1

    def error(self, mensagem):
        raise SyntaxError(f"Erro de sintaxe na posição {self.pos}: {mensagem}")

tokens = [
    ('PALAVRA_CHAVE', 'int'), #0
    ('IDENTIFICADOR', 'x'), #1
    ('SIMBOLO', ';'), #2
    ('PALAVRA_CHAVE', 'float'), #3
    ('IDENTIFICADOR', 'y'), #4
    ('SIMBOLO', ';'), #5
    ('PALAVRA_CHAVE', 'void'), #6
    ('IDENTIFICADOR', 'funcao'), #7
    ('SIMBOLO', '('), #8
    ('PALAVRA_CHAVE', 'int'), #9
    ('IDENTIFICADOR', 'parametro1'), #10
    ('SIMBOLO', ')'), #11
    ('SIMBOLO', '{'), #12
    ('IDENTIFICADOR', 'x'), #13
    ('OPERADOR', '='), #14
    ('NUMERO_INTEIRO', '10'), #15
    ('SIMBOLO', ';'), #16
    ('IDENTIFICADOR', 'y'), #17
    ('OPERADOR', '='), #18
    ('NUMERO_DECIMAL', '3.14'), #19
    ('SIMBOLO', ';'), # 20
    ('SIMBOLO', '}'), #21
    ('SIMBOLO', ';') #22
]

with open("input.txt") as file:
    tokens = file.read()
parser = Parser(Analisador_Lexico.analisador_lexico(tokens))

try:
    parser.parse()
    print("Análise sintática concluída com sucesso.")
except SyntaxError as e:
    print(e)