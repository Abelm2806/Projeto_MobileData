import sqlite3
import os

# Define o caminho para a base de dados ficar sempre na mesma pasta deste script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "loja_telemoveis.db")

def conectar():
    conexao = sqlite3.connect(DB_PATH)
    criar_tabelas(conexao)
    return conexao

def criar_tabelas(conexao):
    cursor = conexao.cursor()
    
    # Tabela de Telemóveis (Com id_fornecedor incluído)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemoveis (
            id_telemovel INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            armazenamento TEXT,
            ram TEXT,
            cor TEXT,
            preco_compra REAL,
            preco_venda REAL,
            stock INTEGER,
            id_fornecedor INTEGER
        )
    """)
    
    # Tabela de Clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            data_registo TEXT
        )
    """)

    # Tabela de Fornecedores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fornecedores (
            id_fornecedor INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            morada TEXT
        )
    """)
    
    # Tabela de Vendas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER,
            data_venda TEXT,
            total_venda REAL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        )
    """)
    
    # Tabela de Detalhes da Venda
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalhes_venda (
            id_detalhe INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venda INTEGER,
            id_telemovel INTEGER,
            quantidade INTEGER,
            preco_unitario REAL,
            subtotal REAL,
            FOREIGN KEY (id_venda) REFERENCES vendas(id_venda),
            FOREIGN KEY (id_telemovel) REFERENCES telemoveis(id_telemovel)
        )
    """)
    
    conexao.commit()