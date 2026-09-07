import pandas as pd
from database import conectar


def resumo_vendas():
    conexao = conectar()

    vendas = pd.read_sql_query("""
    SELECT *
    FROM vendas
    """, conexao)

    if vendas.empty:
        print("\nNenhuma venda registada.")
        conexao.close()
        return

    print("\n=== RESUMO DE VENDAS ===")

    total_faturado = vendas["total_venda"].sum()
    numero_vendas = len(vendas)

    print(f"Total faturado: {total_faturado:.2f} €")
    print(f"Número de vendas: {numero_vendas}")

    conexao.close()


def produto_mais_vendido():
    conexao = conectar()

    query = """
    SELECT
        telemoveis.marca,
        telemoveis.modelo,
        SUM(detalhes_venda.quantidade) AS total_vendido
    FROM detalhes_venda
    JOIN telemoveis
        ON detalhes_venda.id_telemovel =
           telemoveis.id_telemovel
    GROUP BY telemoveis.id_telemovel
    ORDER BY total_vendido DESC
    LIMIT 1
    """

    resultado = pd.read_sql_query(query, conexao)

    print("\n=== PRODUTO MAIS VENDIDO ===")

    if resultado.empty:
        print("Nenhuma venda registada.")
    else:
        marca = resultado.loc[0, "marca"]
        modelo = resultado.loc[0, "modelo"]
        total = resultado.loc[0, "total_vendido"]

        print(f"{marca} {modelo}")
        print(f"Quantidade vendida: {total}")

    conexao.close()


def stock_baixo():
    conexao = conectar()

    query = """
    SELECT marca, modelo, stock
    FROM telemoveis
    WHERE stock <= 3
    """

    resultado = pd.read_sql_query(query, conexao)

    print("\n=== STOCK BAIXO ===")

    if resultado.empty:
        print("Nenhum produto com stock baixo.")
    else:
        print(resultado)

    conexao.close()


def menu_analise():
    while True:
        print("\n" + "=" * 40)
        print("        ANÁLISE DE DADOS")
        print("=" * 40)
        print("1 - Resumo de Vendas")
        print("2 - Produto Mais Vendido")
        print("3 - Stock Baixo")
        print("0 - Voltar")
        print("=" * 40)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            resumo_vendas()
        elif opcao == "2":
            produto_mais_vendido()
        elif opcao == "3":
            stock_baixo()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")