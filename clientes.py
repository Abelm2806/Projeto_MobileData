from database import conectar
from datetime import datetime
from validacoes import (
    ler_texto_obrigatorio,
    ler_texto_opcional,
    ler_id
)


def adicionar_cliente():
    conexao = conectar()
    cursor = conexao.cursor()

    print("\n=== ADICIONAR CLIENTE ===")

    nome = ler_texto_obrigatorio("Nome: ")
    email = ler_texto_opcional("Email: ")
    telefone = ler_texto_opcional("Telefone: ")
    data_registo = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    INSERT INTO clientes
    (nome, email, telefone, data_registo)
    VALUES (?, ?, ?, ?)
    """, (
        nome,
        email,
        telefone,
        data_registo
    ))

    conexao.commit()
    conexao.close()

    print("Cliente adicionado com sucesso!")


def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    print("\n=== LISTA DE CLIENTES ===")

    if len(clientes) == 0:
        print("Nenhum cliente registado.")
    else:
        for c in clientes:
            print("-" * 40)
            print(f"ID: {c[0]}")
            print(f"Nome: {c[1]}")
            print(f"Email: {c[2]}")
            print(f"Telefone: {c[3]}")
            print(f"Data de registo: {c[4]}")
        print("-" * 40)

    conexao.close()


def editar_cliente():
    conexao = conectar()
    cursor = conexao.cursor()

    listar_clientes()

    id_cliente = ler_id("\nID do cliente a editar: ")

    novo_email = ler_texto_opcional("Novo email: ")
    novo_telefone = ler_texto_opcional("Novo telefone: ")

    cursor.execute("""
    UPDATE clientes
    SET email = ?, telefone = ?
    WHERE id_cliente = ?
    """, (
        novo_email,
        novo_telefone,
        id_cliente
    ))

    conexao.commit()
    conexao.close()

    print("Cliente atualizado com sucesso!")


def remover_cliente():
    conexao = conectar()
    cursor = conexao.cursor()

    listar_clientes()

    id_cliente = ler_id("\nID do cliente a remover: ")

    cursor.execute("""
    DELETE FROM clientes
    WHERE id_cliente = ?
    """, (id_cliente,))

    conexao.commit()
    conexao.close()

    print("Cliente removido com sucesso!")