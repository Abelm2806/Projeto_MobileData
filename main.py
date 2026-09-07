import questionary
from database import conectar

from produtos import adicionar_telemovel, listar_telemoveis, editar_telemovel, remover_telemovel
from clientes import adicionar_cliente, listar_clientes, editar_cliente, remover_cliente
from fornecedores import adicionar_fornecedor, listar_fornecedores, editar_fornecedor, remover_fornecedor
from vendas import registar_venda
from analise import menu_analise
from graficos import menu_graficos
from machine_learning import prever_vendas
from exportar import exportar_dados
from limpeza_dados import menu_limpeza_dados


def menu_telemoveis():
    while True:
        opcao = questionary.select(
            "GERIR TELEMÓVEIS",
            choices=[
                "Adicionar Telemóvel",
                "Listar Telemóveis",
                "Editar Telemóvel",
                "Remover Telemóvel",
                "Voltar"
            ]
        ).ask()

        if opcao == "Adicionar Telemóvel":
            adicionar_telemovel()
        elif opcao == "Listar Telemóveis":
            listar_telemoveis()
        elif opcao == "Editar Telemóvel":
            editar_telemovel()
        elif opcao == "Remover Telemóvel":
            remover_telemovel()
        elif opcao == "Voltar":
            break


def menu_clientes():
    while True:
        opcao = questionary.select(
            "GERIR CLIENTES",
            choices=[
                "Adicionar Cliente",
                "Listar Clientes",
                "Editar Cliente",
                "Remover Cliente",
                "Voltar"
            ]
        ).ask()

        if opcao == "Adicionar Cliente":
            adicionar_cliente()
        elif opcao == "Listar Clientes":
            listar_clientes()
        elif opcao == "Editar Cliente":
            editar_cliente()
        elif opcao == "Remover Cliente":
            remover_cliente()
        elif opcao == "Voltar":
            break


def menu_fornecedores():
    while True:
        opcao = questionary.select(
            "GERIR FORNECEDORES",
            choices=[
                "Adicionar Fornecedor",
                "Listar Fornecedores",
                "Editar Fornecedor",
                "Remover Fornecedor",
                "Voltar"
            ]
        ).ask()

        if opcao == "Adicionar Fornecedor":
            adicionar_fornecedor()
        elif opcao == "Listar Fornecedores":
            listar_fornecedores()
        elif opcao == "Editar Fornecedor":
            editar_fornecedor()
        elif opcao == "Remover Fornecedor":
            remover_fornecedor()
        elif opcao == "Voltar":
            break


def menu_principal():
    while True:
        opcao = questionary.select(
            "MOBILE DATA STORE",
            choices=[
                "Gerir Telemóveis",
                "Gerir Clientes",
                "Gerir Fornecedores",
                "Registar Venda",
                "Consultar Stock",
                "Análise de Dados",
                "Visualização de Gráficos",
                "Previsão de Vendas",
                "Exportar Dados",
                "Limpeza de Dados",
                "Sair"
            ]
        ).ask()

        if opcao == "Gerir Telemóveis":
            menu_telemoveis()
        elif opcao == "Gerir Clientes":
            menu_clientes()
        elif opcao == "Gerir Fornecedores":
            menu_fornecedores()
        elif opcao == "Registar Venda":
            regista_venda = registar_venda() if callable(registar_venda) else None
        elif opcao == "Consultar Stock":
            listar_telemoveis()
        elif opcao == "Análise de Dados":
            menu_analise()
        elif opcao == "Visualização de Gráficos":
            menu_graficos()
        elif opcao == "Previsão de Vendas":
            prever_vendas()
        elif opcao == "Exportar Dados":
            exportar_dados()
        elif opcao == "Limpeza de Dados":
            menu_limpeza_dados()
        elif opcao == "Sair":
            print("A sair do sistema...")
            break


if __name__ == "__main__":
    conexao = conectar()
    conexao.close()
    
    menu_principal()