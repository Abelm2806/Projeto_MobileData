import pandas as pd
from database import conectar


def limpar_texto(valor):
    if pd.isna(valor):
        return ""

    return str(valor).strip().title()


def limpar_dados_telemoveis():
    conexao = conectar()

    query = "SELECT * FROM telemoveis"
    dados = pd.read_sql_query(query, conexao)

    print("\n=== LIMPEZA DE DADOS DOS TELEMÓVEIS ===")

    if dados.empty:
        print("Não existem telemóveis para limpar.")
        conexao.close()
        return

    dados["marca"] = dados["marca"].apply(limpar_texto)
    dados["modelo"] = dados["modelo"].apply(lambda x: str(x).strip())
    dados["cor"] = dados["cor"].apply(limpar_texto)

    cursor = conexao.cursor()

    for _, linha in dados.iterrows():
        cursor.execute("""
        UPDATE telemoveis
        SET marca = ?, modelo = ?, cor = ?
        WHERE id_telemovel = ?
        """, (
            linha["marca"],
            linha["modelo"],
            linha["cor"],
            linha["id_telemovel"]
        ))

    conexao.commit()
    conexao.close()

    print("Dados dos telemóveis limpos com sucesso!")


def limpar_dados_clientes():
    conexao = conectar()

    query = "SELECT * FROM clientes"
    dados = pd.read_sql_query(query, conexao)

    print("\n=== LIMPEZA DE DADOS DOS CLIENTES ===")

    if dados.empty:
        print("Não existem clientes para limpar.")
        conexao.close()
        return

    dados["nome"] = dados["nome"].apply(limpar_texto)
    dados["email"] = dados["email"].apply(lambda x: str(x).strip().lower())
    dados["telefone"] = dados["telefone"].apply(lambda x: str(x).strip())

    cursor = conexao.cursor()

    for _, linha in dados.iterrows():
        cursor.execute("""
        UPDATE clientes
        SET nome = ?, email = ?, telefone = ?
        WHERE id_cliente = ?
        """, (
            linha["nome"],
            linha["email"],
            linha["telefone"],
            linha["id_cliente"]
        ))

    conexao.commit()
    conexao.close()

    print("Dados dos clientes limpos com sucesso!")


def menu_limpeza_dados():
    while True:
        print("\n" + "=" * 40)
        print("      LIMPEZA E TRATAMENTO DE DADOS")
        print("=" * 40)
        print("1 - Limpar dados dos telemóveis")
        print("2 - Limpar dados dos clientes")
        print("3 - Limpar todos os dados")
        print("0 - Voltar")
        print("=" * 40)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            limpar_dados_telemoveis()
        elif opcao == "2":
            limpar_dados_clientes()
        elif opcao == "3":
            limpar_dados_telemoveis()
            limpar_dados_clientes()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")