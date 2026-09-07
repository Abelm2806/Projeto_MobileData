from database import conectar
from validacoes import (
    ler_texto_obrigatorio,
    ler_texto_opcional,
    ler_id
)


def adicionar_fornecedor():
    conexao = conectar()
    cursor = conexao.cursor()

    print("\n=== ADICIONAR FORNECEDOR ===")

    nome = ler_texto_obrigatorio("Nome: ")
    email = ler_texto_opcional("Email: ")
    telefone = ler_texto_opcional("Telefone: ")
    morada = ler_texto_opcional("Morada: ")

    cursor.execute("""
    INSERT INTO fornecedores
    (nome, email, telefone, morada)
    VALUES (?, ?, ?, ?)
    """, (
        nome,
        email,
        telefone,
        morada
    ))

    conexao.commit()
    conexao.close()

    print("Fornecedor adicionado com sucesso!")


def listar_fornecedores():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM fornecedores")
    fornecedores = cursor.fetchall()

    print("\n=== LISTA DE FORNECEDORES ===")

    if len(fornecedores) == 0:
        print("Nenhum fornecedor registado.")
    else:
        for f in fornecedores:
            print("-" * 40)
            print(f"ID: {f[0]}")
            print(f"Nome: {f[1]}")
            print(f"Email: {f[2]}")
            print(f"Telefone: {f[3]}")
            print(f"Morada: {f[4]}")
        print("-" * 40)

    conexao.close()


def editar_fornecedor():
    conexao = conectar()
    cursor = conexao.cursor()

    listar_fornecedores()

    id_fornecedor = ler_id("\nID do fornecedor a editar: ")

    novo_email = ler_texto_opcional("Novo email: ")
    novo_telefone = ler_texto_opcional("Novo telefone: ")
    nova_morada = ler_texto_opcional("Nova morada: ")

    cursor.execute("""
    UPDATE fornecedores
    SET email = ?, telefone = ?, morada = ?
    WHERE id_fornecedor = ?
    """, (
        novo_email,
        novo_telefone,
        nova_morada,
        id_fornecedor
    ))

    conexao.commit()
    conexao.close()

    print("Fornecedor atualizado com sucesso!")


def remover_fornecedor():
    conexao = conectar()
    cursor = conexao.cursor()

    listar_fornecedores()

    id_fornecedor = ler_id("\nID do fornecedor a remover: ")

    cursor.execute("""
    DELETE FROM fornecedores
    WHERE id_fornecedor = ?
    """, (id_fornecedor,))

    conexao.commit()
    conexao.close()

    print("Fornecedor removido com sucesso!")