import pandas as pd
import os
from database import conectar


def exportar_dados():
    conexao = conectar()

    pasta_projeto = os.path.dirname(__file__)
    pasta_dados = os.path.join(
        pasta_projeto,
        "dados"
    )

    os.makedirs(
        pasta_dados,
        exist_ok=True
    )

    tabelas = [
        "clientes",
        "telemoveis",
        "fornecedores",
        "vendas"
    ]

    print("\n=== EXPORTAR DADOS ===")

    for tabela in tabelas:
        query = f"SELECT * FROM {tabela}"
        dados = pd.read_sql_query(
            query,
            conexao
        )

        caminho = os.path.join(
            pasta_dados,
            f"{tabela}.csv"
        )

        dados.to_csv(
            caminho,
            index=False,
            encoding="utf-8-sig"
        )

        print(
            f"{tabela}.csv exportado em /dados"
        )

    conexao.close()

    print("\nExportação concluída!")