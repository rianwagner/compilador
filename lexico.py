import re

ESPECIFICACAO_TOKENS = [
    ('NUMERO_DECIMAL', r'\d+\.\d+'),
    ('NUMERO_INTEIRO', r'\d+'),
    ('STRING', r'"[^"\n]*"'),
    ('COMPARACAO', r'==|!=|<=|>=|<|>'),
    ('ATRIBUICAO', r'='),
    ('OPERADOR', r'[+\-*/]'),
    ('DELIMITADOR', r'[();{}]'),
    ('IDENTIFICADOR', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('COMENTARIO', r'\#.*'),
    ('ESPACO', r'[ \t]+'),
    ('NOVA_LINHA', r'\n'),
    ('ERRO', r'.'),
]

PALAVRAS_RESERVADAS = {'inicio', 'fim', 'se', 'senao', 'enquanto', 'escreva'}

regex_tokens = '|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in ESPECIFICACAO_TOKENS)

def analisador_lexico(codigo):
    linha = 1
    coluna = 1

    for correspondencia in re.finditer(regex_tokens, codigo):
        tipo = correspondencia.lastgroup
        valor = correspondencia.group()
        
        if tipo == 'NOVA_LINHA':
            linha += 1
            coluna = 1
            continue
        elif tipo == 'ESPACO' or tipo == 'COMENTARIO':
            coluna += len(valor)
            continue
        elif tipo == 'NUMERO_INTEIRO':
            valor = int(valor)
        elif tipo == 'NUMERO_DECIMAL':
            valor = float(valor)
        elif tipo == 'IDENTIFICADOR' and valor in PALAVRAS_RESERVADAS:
            tipo = 'PALAVRA_RESERVADA'
        elif tipo == 'ERRO':
            raise RuntimeError(f'Erro léxico: Caractere inválido {valor!r} na linha {linha}, coluna {coluna}')
        yield (tipo, valor, linha, coluna)
        coluna += len(str(valor))

if __name__ == "__main__":
    nome_arquivo = "programa.txt"
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
        exit(1)

    print("Tokens encontrados:\n")
    try:
        for token in analisador_lexico(codigo):
            print(token)
    except RuntimeError as e:
        print(e)
