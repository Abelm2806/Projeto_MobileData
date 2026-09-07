import pandas as pd
from sklearn.linear_model import LinearRegression
from database import conectar


def prever_vendas():
    conexao = conectar()

    query = """
    SELECT
        data_venda,
        total_venda
    FROM vendas
    ORDER BY data_venda
    """

    dados = pd.read_sql_query(query, conexao)
    conexao.close()

    print("\n=== PREVISÃO DE VENDAS ===")

    if len(dados) < 2:
        print("Dados insuficientes para realizar previsão.")
        print("É necessário ter pelo menos 2 vendas registadas.")
        return

    dados["data_venda"] = pd.to_datetime(dados["data_venda"])
    dados["mes"] = dados["data_venda"].dt.month

    vendas_por_mes = dados.groupby("mes")["total_venda"].sum().reset_index()

    if len(vendas_por_mes) < 2:
        print("Dados insuficientes para treinar o modelo.")
        print("É necessário ter vendas em pelo menos 2 meses diferentes.")
        return

    x = vendas_por_mes[["mes"]]
    y = vendas_por_mes["total_venda"]

    modelo = LinearRegression()
    modelo.fit(x, y)

    proximo_mes = vendas_por_mes["mes"].max() + 1

    if proximo_mes > 12:
        proximo_mes = 1

    previsao = modelo.predict([[proximo_mes]])

    print(f"Próximo mês analisado: {proximo_mes}")
    print(f"Previsão de faturação: {previsao[0]:.2f} €")
    print("\nNota: Esta previsão é simples e baseada no histórico de vendas.")