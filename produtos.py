from database import conectar
from validacoes import (
    ler_texto_obrigatorio,
    ler_texto_opcional,
    ler_float,
    ler_int,
    ler_id
)


def adicionar_telemovel():
    conexao = conectar()
    cursor = conexao.cursor()

    print("\n=== ADICIONAR TELEMÓVEL ===")

    marca = ler_texto_obrigatorio("Marca: ")
    modelo = ler_texto_obrigatorio("Modelo: ")
    armazenamento = ler_texto_opcional("Armazenamento: ")
    ram = ler_texto_opcional("RAM: ")
    cor = ler_texto_opcional("Cor: ")
    preco_compra = ler_float("Preço de compra: ")
    preco_venda = ler_float("Preço de venda: ")
    stock = ler_int("Stock: ")

    id_fornecedor = input(
        "ID fornecedor (opcional): "
    ).strip()

    if id_fornecedor == "":
        id_fornecedor = None
    else:
        try:
            id_fornecedor = int(id_fornecedor)
        except ValueError:
            id_fornecedor = None

    cursor.execute("""
    INSERT INTO telemoveis
    (marca, modelo, armazenamento, ram, cor,
    preco_compra, preco_venda, stock, id_fornecedor)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        marca,
        modelo,
        armazenamento,
        ram,
        cor,
        preco_compra,
        preco_venda,
        stock,
        id_fornecedor
    ))

    conexao.commit()
    conexao.close()

    print("Telemóvel adicionado com sucesso!")


def listar_telemoveis():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM telemoveis")
    telemoveis = cursor.fetchall()

    print("\n=== LISTA DE TELEMÓVEIS ===")

    if len(telemoveis) == 0:
        print("Nenhum telemóvel registado.")
    else:
        for t in telemoveis:
            print("-" * 40)
            print(f"ID: {t[0]}")
            print(f"Marca: {t[1]}")
            print(f"Modelo: {t[2]}")
            print(f"Armazenamento: {t[3]}")
            print(f"RAM: {t[4]}")
            print(f"Cor: {t[5]}")
            print(f"Preço de compra: {t[6]} €")
            print(f"Preço de venda: {t[7]} €")
            print(f"Stock: {t[8]}")
            print(f"ID Fornecedor: {t[9]}")
        print("-" * 40)

    conexao.close()


def editar_telemovel():
    conexao = conectar()
    cursor = conexao.cursor()

    listar_telemoveis()

    id_telemovel = ler_id(
        "\nID do telemóvel a editar: "
    )

    novo_preco = ler_float(
        "Novo preço de venda: "
    )

    novo_stock = ler_int(
        "Novo stock: "
    )

    cursor.execute("""
    UPDATE telemoveis
    SET preco_venda = ?, stock = ?
    WHERE id_telemovel = ?
    """, (
        novo_preco,
        novo_stock,
        id_telemovel
    ))

    conexao.commit()
    conexao.close()

    print("Telemóvel atualizado com sucesso!")


def remover_telemovel():
    conexao = conectar()
    cursor = conexao.cursor()

    listar_telemoveis()

    id_telemovel = ler_id(
        "\nID do telemóvel a remover: "
    )

    cursor.execute("""
    DELETE FROM telemoveis
    WHERE id_telemovel = ?
    """, (id_telemovel,))

    conexao.commit()
    conexao.close()

    print("Telemóvel removido com sucesso!")