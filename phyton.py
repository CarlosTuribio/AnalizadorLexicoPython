import re
import csv


class EntradaInvalidaError(Exception):
    pass


def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, "r") as f:
        return f.read()


def gerar_tokens(conteudo, regex_tokens):
    tokens = []

    for tipo_token, regex in regex_tokens.items():
        for match in re.finditer(regex, conteudo):
            token = match.group()
            posicao = match.start()
            tamanho = match.end() - posicao
            num_linha = conteudo.count("\n", 0, posicao)
            num_coluna = posicao - conteudo.rfind("\n", 0, posicao)
            if tipo_token == "Invalido":
                raise EntradaInvalidaError(
                    f"Entrada inválida encontrada: '{token}' na linha {num_linha}, coluna {num_coluna}")
            tokens.append((token, tipo_token, tamanho, (num_linha, num_coluna)))

    return tokens


def exportar_tokens(tokens, nome_arquivo):
    with open(nome_arquivo, "w", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(["Token", "Tipo", "Tamanho", "Posição"])
        escritor.writerows(tokens)


def exportar_simbolos(tokens, nome_arquivo):
    simbolos = []
    for token, tipo_token, _, _ in tokens:
        if tipo_token in ["Identificador", "Constante"]:
            if token not in [s[1] for s in simbolos]:
                simbolos.append((len(simbolos) + 1, token))
    with open(nome_arquivo, "w", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(["Índice", "Símbolo"])
        escritor.writerows(simbolos)


def analisador_lexico(nome_arquivo):
    PALAVRAS_RESERVADAS = r"\b(and|as|assert|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)\b"
    IDENTIFICADORES = r"\b(?!and|as|assert|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)[a-zA-Z]+\w*\b"
    OPERADORES = r"[+\-*/%<>=]"
    LOGICOS = r"\b(and|or|not)\b"
    PONTUACAO = r"[\[\](){},.:;]"
    CONSTANTES = r"\d+"
    CARACTERES_INVALIDOS = r"(?![+\-*/<>=;\[\](){},.:;])[^\w\s]"

    regex_tokens = {
        "Palavra Reservada": PALAVRAS_RESERVADAS,
        "Identificador": IDENTIFICADORES,
        "Operador": OPERADORES,
        "Operador Logico": LOGICOS,
        "Pontuacao": PONTUACAO,
        "Constante": CONSTANTES,
        "Invalido": CARACTERES_INVALIDOS,
    }
    conteudo = ler_arquivo(nome_arquivo)
    try:
        tokens = gerar_tokens(conteudo, regex_tokens)
    except EntradaInvalidaError as e:
        print(f"Erro: {str(e)}")
        return
    exportar_tokens(tokens, "tokens.csv")
    exportar_simbolos(tokens, "simbolos.csv")


analisador_lexico("entrada.txt")
