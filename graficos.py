import pandas as pd
import matplotlib.pyplot as plt
from database import conectar


def grafico_produtos_mais_vendidos():
    conexao = conectar()

    query = """
    SELECT
        telemoveis.marca || ' ' || telemoveis.modelo AS produto,
        SUM(detalhes_venda.quantidade) AS total_vendido
    FROM detalhes_venda
    JOIN telemoveis
        ON detalhes_venda.id_telemovel = telemoveis.id_telemovel
    GROUP BY produto
    ORDER BY total_vendido DESC
    """

    dados = pd.read_sql_query(query, conexao)
    conexao.close()

    if dados.empty:
        print("Não existem dados suficientes para gerar o gráfico.")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(dados["produto"], dados["total_vendido"])
    plt.title("Produtos Mais Vendidos")
    plt.xlabel("Produto")
    plt.ylabel("Quantidade Vendida")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def grafico_vendas_por_mes():
    conexao = conectar()

    query = """
    SELECT
        substr(data_venda, 1, 7) AS mes,
        SUM(total_venda) AS total_faturado
    FROM vendas
    GROUP BY mes
    ORDER BY mes
    """

    dados = pd.read_sql_query(query, conexao)
    conexao.close()

    if dados.empty:
        print("Não existem dados suficientes para gerar o gráfico.")
        return

    plt.figure(figsize=(8, 5))
    plt.plot(dados["mes"], dados["total_faturado"], marker="o")
    plt.title("Faturação Mensal")
    plt.xlabel("Mês")
    plt.ylabel("Total Faturado (€)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def grafico_stock_atual():
    conexao = conectar()

    query = """
    SELECT
        marca || ' ' || modelo AS produto,
        stock
    FROM telemoveis
    ORDER BY stock ASC
    """

    dados = pd.read_sql_query(query, conexao)
    conexao.close()

    if dados.empty:
        print("Não existem telemóveis registados.")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(dados["produto"], dados["stock"])
    plt.title("Stock Atual por Produto")
    plt.xlabel("Produto")
    plt.ylabel("Stock")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def menu_graficos():
    while True:
        print("\n" + "=" * 40)
        print("      VISUALIZAÇÃO DE GRÁFICOS")
        print("=" * 40)
        print("1 - Produtos Mais Vendidos")
        print("2 - Faturação Mensal")
        print("3 - Stock Atual")
        print("0 - Voltar")
        print("=" * 40)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            grafico_produtos_mais_vendidos()
        elif opcao == "2":
            grafico_vendas_por_mes()
        elif opcao == "3":
            grafico_stock_atual()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")