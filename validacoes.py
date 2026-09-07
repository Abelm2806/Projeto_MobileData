def ler_texto_obrigatorio(mensagem):
    while True:
        valor = input(mensagem).strip()

        if valor != "":
            return valor

        print("Este campo é obrigatório. Tente novamente.")


def ler_texto_opcional(mensagem):
    return input(mensagem).strip()


def ler_float(mensagem):
    while True:
        valor = input(mensagem).replace(",", ".").strip()

        try:
            numero = float(valor)

            if numero >= 0:
                return numero
            else:
                print("O valor não pode ser negativo.")

        except ValueError:
            print("Digite um número válido.")


def ler_int(mensagem):
    while True:
        valor = input(mensagem).strip()

        try:
            numero = int(valor)

            if numero >= 0:
                return numero
            else:
                print("O valor não pode ser negativo.")

        except ValueError:
            print("Digite um número inteiro válido.")


def ler_id(mensagem):
    while True:
        valor = input(mensagem).strip()

        try:
            numero = int(valor)

            if numero > 0:
                return numero
            else:
                print("O ID deve ser maior que zero.")

        except ValueError:
            print("Digite um ID válido.")