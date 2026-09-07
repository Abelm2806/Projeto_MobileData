from database import conectar
from datetime import datetime
from validacoes import ler_id, ler_int


def listar_clientes_resumido():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id_cliente, nome FROM clientes")
    clientes = cursor.fetchall()

    print("\n=== CLIENTES DISPONÍVEIS ===")

    if len(clientes) == 0:
        print("Nenhum cliente registado.")
    else:
        for c in clientes:
            print(f"ID: {c[0]} | Nome: {c[1]}")

    conexao.close()


def listar_telemoveis_resumido():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT id_telemovel, marca, modelo, preco_venda, stock
    FROM telemoveis
    """)
    telemoveis = cursor.fetchall()

    print("\n=== TELEMÓVEIS DISPONÍVEIS ===")

    if len(telemoveis) == 0:
        print("Nenhum telemóvel registado.")
    else:
        for t in telemoveis:
            print(
                f"ID: {t[0]} | {t[1]} {t[2]} | "
                f"Preço: {t[3]} € | Stock: {t[4]}"
            )

    conexao.close()


def registar_venda():
    conexao = conectar()
    cursor = conexao.cursor()

    print("\n=== REGISTAR VENDA ===")

    listar_clientes_resumido()
    id_cliente = ler_id("\nID do cliente: ")

    cursor.execute("""
    SELECT id_cliente
    FROM clientes
    WHERE id_cliente = ?
    """, (id_cliente,))

    cliente = cursor.fetchone()

    if cliente is None:
        print("Cliente não encontrado.")
        conexao.close()
        return

    listar_telemoveis_resumido()
    id_telemovel = ler_id("\nID do telemóvel: ")

    quantidade = ler_int("Quantidade: ")

    if quantidade == 0:
        print("A quantidade deve ser maior que zero.")
        conexao.close()
        return

    cursor.execute("""
    SELECT preco_venda, stock
    FROM telemoveis
    WHERE id_telemovel = ?
    """, (id_telemovel,))

    telemovel = cursor.fetchone()

    if telemovel is None:
        print("Telemóvel não encontrado.")
        conexao.close()
        return

    preco_unitario = telemovel[0]
    stock_atual = telemovel[1]

    if quantidade > stock_atual:
        print("Stock insuficiente para realizar a venda.")
        conexao.close()
        return

    subtotal = preco_unitario * quantidade
    total_venda = subtotal
    data_venda = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    INSERT INTO vendas
    (id_cliente, data_venda, total_venda)
    VALUES (?, ?, ?)
    """, (
        id_cliente,
        data_venda,
        total_venda
    ))

    id_venda = cursor.lastrowid

    cursor.execute("""
    INSERT INTO detalhes_venda
    (id_venda, id_telemovel, quantidade, preco_unitario, subtotal)
    VALUES (?, ?, ?, ?, ?)
    """, (
        id_venda,
        id_telemovel,
        quantidade,
        preco_unitario,
        subtotal
    ))

    novo_stock = stock_atual - quantidade

    cursor.execute("""
    UPDATE telemoveis
    SET stock = ?
    WHERE id_telemovel = ?
    """, (
        novo_stock,
        id_telemovel
    ))

    conexao.commit()
    conexao.close()

    print("\nVenda registada com sucesso!")
    print(f"Total da venda: {total_venda:.2f} €")
    print(f"Stock atualizado: {novo_stock}")