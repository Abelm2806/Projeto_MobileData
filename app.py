import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import conectar
from datetime import datetime
import json

st.set_page_config(
    page_title="Mobile Data Store",
    page_icon="📱",
    layout="wide"
)

st.markdown("""
    <style>
        .stImage img {
            max-height: 280px;
            object-fit: cover;
            width: 100%;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

def resetar_e_popular_dados():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS detalhes_venda")
    cursor.execute("DROP TABLE IF EXISTS vendas")
    cursor.execute("DROP TABLE IF EXISTS telemoveis")
    cursor.execute("DROP TABLE IF EXISTS clientes")
    
    cursor.execute("""
        CREATE TABLE telemoveis (
            id_telemovel INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            armazenamento TEXT,
            ram TEXT,
            cor TEXT,
            preco_compra REAL,
            preco_venda REAL,
            stock INTEGER
        )
    """)
    
    cursor.execute("""
        CREATE TABLE clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            data_registo TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE vendas (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER,
            data_venda TEXT,
            total_venda REAL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE detalhes_venda (
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
    
    telemoveis_exemplo = [
        ("Apple", "iPhone 15", "128GB", "6GB", "Preto", 750.00, 999.00, 10),
        ("Samsung", "Galaxy S24", "256GB", "8GB", "Cinzento", 700.00, 920.00, 8),
        ("Xiaomi", "Redmi Note 13", "128GB", "6GB", "Azul", 150.00, 249.00, 15),
        ("Google", "Pixel 8", "128GB", "8GB", "Rosa", 550.00, 720.00, 5)
    ]
    cursor.executemany("""
        INSERT INTO telemoveis (marca, modelo, armazenamento, ram, cor, preco_compra, preco_venda, stock)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, telemoveis_exemplo)
    
    clientes_exemplo = [
        ("João Silva", "joao.silva@email.com", "912345678", "2026-06-01"),
        ("Maria Santos", "maria.santos@email.com", "961112233", "2026-06-15"),
        ("Carlos Oliveira", "carlos.oliveira@email.com", "933445566", "2026-07-10")
    ]
    cursor.executemany("""
        INSERT INTO clientes (nome, email, telefone, data_registo)
        VALUES (?, ?, ?, ?)
    """, clientes_exemplo)
    
    conexao.commit()
    conexao.close()

if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "Início"

st.sidebar.title("📱 Mobile Data Store")
st.sidebar.markdown("---")

opcoes_menu = [
    "Início", 
    "Consultar Stock", 
    "Gerir Registos", 
    "Gerir Telemóveis",
    "Registar Venda", 
    "Análise e Gráficos"
]

indice_atual = opcoes_menu.index(st.session_state.pagina_atual)
menu = st.sidebar.radio("Navegação", opcoes_menu, index=indice_atual)
st.session_state.pagina_atual = menu

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Área de Testes")
if st.sidebar.button("🔄 Resetar e Inserir Exemplos", width='stretch'):
    resetar_e_popular_dados()
    st.sidebar.success("Base de dados recriada e IDs a começar no 1!")
    st.rerun()

def mostrar_botoes_navegacao():
    st.markdown("---")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("🏠 Início", width='stretch'):
            st.session_state.pagina_atual = "Início"
            st.rerun()
    with col2:
        if st.button("📦 Stock", width='stretch'):
            st.session_state.pagina_atual = "Consultar Stock"
            st.rerun()
            
    with col3:
        if st.button("📝 Gerir Registos", width='stretch'):
            st.session_state.pagina_atual = "Gerir Registos"
            st.rerun()

    with col4:
        if st.button("⚙️ Telemóveis", width='stretch'):
            st.session_state.pagina_atual = "Gerir Telemóveis"
            st.rerun()
            
    with col5:
        if st.button("🛒 Venda", width='stretch'):
            st.session_state.pagina_atual = "Registar Venda"
            st.rerun()

    with col6:
        if st.button("📊 Gráficos", width='stretch'):
            st.session_state.pagina_atual = "Análise e Gráficos"
            st.rerun()

# ---------------------------------------------------------
# PÁGINA: INÍCIO
# ---------------------------------------------------------
if st.session_state.pagina_atual == "Início":
    st.title("📱 Bem-vindo ao Mobile Data Store")
    
    st.image(
        "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?q=80&w=1600&auto=format&fit=crop",
        width='stretch',
        caption="Gestão Inteligente de Telemóveis e Stock"
    )
    
    st.markdown("### Atalhos Rápidos")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📦 Consultar Stock", width='stretch'):
            st.session_state.pagina_atual = "Consultar Stock"
            st.rerun()
            
    with col2:
        if st.button("📝 Gerir Registos", width='stretch'):
            st.session_state.pagina_atual = "Gerir Registos"
            st.rerun()

    with col3:
        if st.button("⚙️ Gerir Telemóveis", width='stretch'):
            st.session_state.pagina_atual = "Gerir Telemóveis"
            st.rerun()

    with col4:
        if st.button("🛒 Registar Venda", width='stretch'):
            st.session_state.pagina_atual = "Registar Venda"
            st.rerun()
            
    with col5:
        if st.button("📊 Ver Gráficos", width='stretch'):
            st.session_state.pagina_atual = "Análise e Gráficos"
            st.rerun()

# ---------------------------------------------------------
# PÁGINA: CONSULTAR STOCK
# ---------------------------------------------------------
elif st.session_state.pagina_atual == "Consultar Stock":
    st.title("📦 Consulta de Stock, Clientes e Vendas")
    
    conexao = conectar()
    telemoveis_df = pd.read_sql_query("SELECT * FROM telemoveis", conexao)
    clientes_df = pd.read_sql_query("SELECT * FROM clientes", conexao)
    
    query_vendas = """
        SELECT v.id_venda, c.nome AS cliente, v.data_venda, v.total_venda 
        FROM vendas v 
        LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
    """
    vendas_df = pd.read_sql_query(query_vendas, conexao)
    conexao.close()

    st.subheader("Telemóveis em Stock")
    if telemoveis_df.empty:
        st.warning("Não existem telemóveis registados.")
    else:
        st.dataframe(telemoveis_df, width='stretch')
        st.download_button(
            label="📥 Descarregar Telemóveis (JSON)",
            data=telemoveis_df.to_json(orient="records", force_ascii=False, indent=4),
            file_name="telemoveis.json",
            mime="application/json"
        )

    st.markdown("---")
    st.subheader("Clientes Registados")
    if clientes_df.empty:
        st.warning("Não existem clientes registados.")
    else:
        st.dataframe(clientes_df, width='stretch')
        st.download_button(
            label="📥 Descarregar Clientes (JSON)",
            data=clientes_df.to_json(orient="records", force_ascii=False, indent=4),
            file_name="clientes.json",
            mime="application/json"
        )

    st.markdown("---")
    st.subheader("Histórico de Vendas")
    if vendas_df.empty:
        st.info("Não existem vendas registadas.")
    else:
        st.dataframe(vendas_df, width='stretch')
        st.download_button(
            label="📥 Descarregar Vendas (JSON)",
            data=vendas_df.to_json(orient="records", force_ascii=False, indent=4),
            file_name="vendas.json",
            mime="application/json"
        )

    mostrar_botoes_navegacao()

# ---------------------------------------------------------
# PÁGINA: GERIR REGISTOS (CRUD COMPLETO TELEMÓVEIS E CLIENTES)
# ---------------------------------------------------------
elif st.session_state.pagina_atual == "Gerir Registos":
    st.title("📝 Painel de Gestão de Registos (CRUD)")
    
    tab_tel, tab_cli = st.tabs(["📱 Gestão de Telemóveis", "👤 Gestão de Clientes"])
    
    with tab_tel:
        sub_adicionar, sub_consultar, sub_editar, sub_remover = st.tabs(["➕ Adicionar", "🔍 Consultar", "✏️ Atualizar", "🗑️ Remover"])
        
        with sub_adicionar:
            st.subheader("Registar Novo Telemóvel")
            with st.form("form_add_tel"):
                marca = st.text_input("Marca *")
                modelo = st.text_input("Modelo *")
                armazenamento = st.text_input("Armazenamento (ex: 128GB)")
                ram = st.text_input("RAM (ex: 4GB)")
                cor = st.text_input("Cor")
                preco_compra = st.number_input("Preço de Compra (€)", min_value=0.0, format="%.2f", key="pc_tel")
                preco_venda = st.number_input("Preço de Venda (€)", min_value=0.0, format="%.2f", key="pv_tel")
                stock = st.number_input("Stock Inicial", min_value=0, step=1, key="st_tel")
                
                if st.form_submit_button("Guardar Telemóvel"):
                    if not marca.strip() or not modelo.strip():
                        st.error("A marca e o modelo são obrigatórios!")
                    else:
                        conexao = conectar()
                        cursor = conexao.cursor()
                        cursor.execute("""
                            INSERT INTO telemoveis (marca, modelo, armazenamento, ram, cor, preco_compra, preco_venda, stock)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (marca, modelo, armazenamento, ram, cor, preco_compra, preco_venda, stock))
                        conexao.commit()
                        conexao.close()
                        st.success("Telemóvel adicionado com sucesso!")
                        st.rerun()

        with sub_consultar:
            st.subheader("Lista de Telemóveis")
            conexao = conectar()
            df_tels = pd.read_sql_query("SELECT * FROM telemoveis", conexao)
            conexao.close()
            if df_tels.empty:
                st.info("Nenhum telemóvel registado.")
            else:
                st.dataframe(df_tels, width='stretch')
                st.download_button(
                    label="📥 Descarregar Esta Tabela (JSON)",
                    data=df_tels.to_json(orient="records", force_ascii=False, indent=4),
                    file_name="telemoveis_gerir.json",
                    mime="application/json"
                )

        with sub_editar:
            st.subheader("Atualizar Dados do Telemóvel")
            conexao = conectar()
            df_tels = pd.read_sql_query("SELECT id_telemovel, marca, modelo, preco_venda, stock FROM telemoveis", conexao)
            conexao.close()
            if df_tels.empty:
                st.info("Sem telemóveis para atualizar.")
            else:
                with st.form("form_edit_tel_geral"):
                    opcoes_tels = (df_tels["id_telemovel"].astype(str) + " - " + df_tels["marca"] + " " + df_tels["modelo"]).tolist()
                    selecionado = st.selectbox("Selecione o Telemóvel", options=opcoes_tels)
                    novo_preco = st.number_input("Novo Preço de Venda (€)", min_value=0.0, format="%.2f", key="up_preco")
                    novo_stock = st.number_input("Novo Stock", min_value=0, step=1, key="up_stock")
                    
                    if st.form_submit_button("Atualizar Registo"):
                        id_t = int(selecionado.split(" - ")[0])
                        conexao = conectar()
                        cursor = conexao.cursor()
                        cursor.execute("UPDATE telemoveis SET preco_venda = ?, stock = ? WHERE id_telemovel = ?", (novo_preco, novo_stock, id_t))
                        conexao.commit()
                        conexao.close()
                        st.success("Telemóvel atualizado com sucesso!")
                        st.rerun()

        with sub_remover:
            st.subheader("Remover Telemóvel")
            conexao = conectar()
            df_tels = pd.read_sql_query("SELECT id_telemovel, marca, modelo FROM telemoveis", conexao)
            conexao.close()
            if df_tels.empty:
                st.info("Sem telemóveis para remover.")
            else:
                with st.form("form_rem_tel_geral"):
                    opcoes_tels = (df_tels["id_telemovel"].astype(str) + " - " + df_tels["marca"] + " " + df_tels["modelo"]).tolist()
                    selecionado = st.selectbox("Selecione o Telemóvel a Remover", options=opcoes_tels, key="sel_rem_tel")
                    
                    if st.form_submit_button("Remover Permanentemente"):
                        id_t = int(selecionado.split(" - ")[0])
                        conexao = conectar()
                        cursor = conexao.cursor()
                        cursor.execute("DELETE FROM telemoveis WHERE id_telemovel = ?", (id_t,))
                        conexao.commit()
                        conexao.close()
                        st.success("Telemóvel removido com sucesso!")
                        st.rerun()

    with tab_cli:
        sub_c_adicionar, sub_c_consultar, sub_c_editar, sub_c_remover = st.tabs(["➕ Adicionar", "🔍 Consultar", "✏️ Atualizar", "🗑️ Remover"])
        
        with sub_c_adicionar:
            st.subheader("Registar Novo Cliente")
            with st.form("form_add_cli"):
                nome = st.text_input("Nome do Cliente *")
                email = st.text_input("Email")
                telefone = st.text_input("Telefone")
                
                if st.form_submit_button("Guardar Cliente"):
                    if not nome.strip():
                        st.error("O nome do cliente é obrigatório!")
                    else:
                        data_registo = datetime.now().strftime("%Y-%m-%d")
                        conexao = conectar()
                        cursor = conexao.cursor()
                        cursor.execute("""
                            INSERT INTO clientes (nome, email, telefone, data_registo)
                            VALUES (?, ?, ?, ?)
                        """, (nome, email, telefone, data_registo))
                        conexao.commit()
                        conexao.close()
                        st.success("Cliente adicionado com sucesso!")
                        st.rerun()

        with sub_c_consultar:
            st.subheader("Lista de Clientes")
            conexao = conectar()
            df_cli = pd.read_sql_query("SELECT * FROM clientes", conexao)
            conexao.close()
            if df_cli.empty:
                st.info("Nenhum cliente registado.")
            else:
                st.dataframe(df_cli, width='stretch')
                st.download_button(
                    label="📥 Descarregar Clientes (JSON)",
                    data=df_cli.to_json(orient="records", force_ascii=False, indent=4),
                    file_name="clientes_gerir.json",
                    mime="application/json"
                )

        with sub_c_editar:
            st.subheader("Atualizar Dados do Cliente")
            conexao = conectar()
            df_cli = pd.read_sql_query("SELECT id_cliente, nome, email, telefone FROM clientes", conexao)
            conexao.close()
            if df_cli.empty:
                st.info("Sem clientes para atualizar.")
            else:
                with st.form("form_edit_cli_geral"):
                    opcoes_cli = (df_cli["id_cliente"].astype(str) + " - " + df_cli["nome"]).tolist()
                    selecionado_cli = st.selectbox("Selecione o Cliente", options=opcoes_cli)
                    novo_email = st.text_input("Novo Email")
                    novo_telefone = st.text_input("Novo Telefone")
                    
                    if st.form_submit_button("Atualizar Cliente"):
                        id_c = int(selecionado_cli.split(" - ")[0])
                        conexao = conectar()
                        cursor = conexao.cursor()
                        cursor.execute("UPDATE clientes SET email = ?, telefone = ? WHERE id_cliente = ?", (novo_email, novo_telefone, id_c))
                        conexao.commit()
                        conexao.close()
                        st.success("Cliente atualizado com sucesso!")
                        st.rerun()

        with sub_c_remover:
            st.subheader("Remover Cliente")
            conexao = conectar()
            df_cli = pd.read_sql_query("SELECT id_cliente, nome FROM clientes", conexao)
            conexao.close()
            if df_cli.empty:
                st.info("Sem clientes para remover.")
            else:
                with st.form("form_rem_cli_geral"):
                    opcoes_cli = (df_cli["id_cliente"].astype(str) + " - " + df_cli["nome"]).tolist()
                    selecionado = st.selectbox("Selecione o Cliente a Remover", options=opcoes_cli)
                    
                    if st.form_submit_button("Remover Cliente"):
                        id_c = int(selecionado.split(" - ")[0])
                        conexao = conectar()
                        cursor = conexao.cursor()
                        cursor.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_c,))
                        conexao.commit()
                        conexao.close()
                        st.success("Cliente removido com sucesso!")
                        st.rerun()

    mostrar_botoes_navegacao()

# ---------------------------------------------------------
# PÁGINA: GERIR TELEMÓVEIS
# ---------------------------------------------------------
elif st.session_state.pagina_atual == "Gerir Telemóveis":
    st.title("⚙️ Atalho Direto: Gestão Rápida de Telemóveis")
    conexao = conectar()
    telemoveis_df = pd.read_sql_query("SELECT * FROM telemoveis", conexao)
    conexao.close()
    
    if telemoveis_df.empty:
        st.warning("Não existem telemóveis registados.")
    else:
        st.dataframe(telemoveis_df, width='stretch')
        st.download_button(
            label="📥 Descarregar Dados (JSON)",
            data=telemoveis_df.to_json(orient="records", force_ascii=False, indent=4),
            file_name="gestao_telemoveis.json",
            mime="application/json"
        )
        
        with st.form("form_quick_edit"):
            id_editar = st.selectbox("Selecione o ID para atualizar preço/stock rápido", options=telemoveis_df["id_telemovel"].tolist())
            novo_preco = st.number_input("Preço de Venda (€)", min_value=0.0, format="%.2f")
            novo_stock = st.number_input("Stock", min_value=0, step=1)
            if st.form_submit_button("Atualizar Stock/Preço"):
                conexao = conectar()
                cursor = conexao.cursor()
                cursor.execute("UPDATE telemoveis SET preco_venda = ?, stock = ? WHERE id_telemovel = ?", (novo_preco, novo_stock, id_editar))
                conexao.commit()
                conexao.close()
                st.success("Atualizado com sucesso!")
                st.rerun()

    mostrar_botoes_navegacao()

# ---------------------------------------------------------
# PÁGINA: REGISTAR VENDA
# ---------------------------------------------------------
elif st.session_state.pagina_atual == "Registar Venda":
    st.title("🛒 Registar Nova Venda")
    
    conexao = conectar()
    clientes_df = pd.read_sql_query("SELECT id_cliente, nome FROM clientes", conexao)
    telemoveis_df = pd.read_sql_query("SELECT id_telemovel, marca, modelo, preco_venda, stock FROM telemoveis", conexao)
    conexao.close()
    
    if clientes_df.empty or telemoveis_df.empty:
        st.warning("Precisa de ter pelo menos um cliente e um telemóvel registados para efetuar vendas.")
    else:
        with st.form("form_venda"):
            cliente_escolhido = st.selectbox("Selecione o Cliente", options=clientes_df["nome"].tolist())
            telemovel_opcoes = (telemoveis_df["marca"] + " " + telemoveis_df["modelo"] + " (Stock: " + telemoveis_df["stock"].astype(str) + ")").tolist()
            telemovel_escolhido = st.selectbox("Selecione o Telemóvel", options=telemovel_opcoes)
            quantidade = st.number_input("Quantidade", min_value=1, step=1)
            
            if st.form_submit_button("Concluir Venda"):
                id_cliente = clientes_df.loc[clientes_df["nome"] == cliente_escolhido, "id_cliente"].values[0]
                idx_tel = telemovel_opcoes.index(telemovel_escolhido)
                id_telemovel = telemoveis_df.loc[idx_tel, "id_telemovel"]
                preco_unitario = telemoveis_df.loc[idx_tel, "preco_venda"]
                stock_atual = telemoveis_df.loc[idx_tel, "stock"]
                
                if quantidade > stock_atual:
                    st.error("Stock insuficiente para realizar esta venda!")
                else:
                    subtotal = preco_unitario * quantidade
                    data_venda = datetime.now().strftime("%Y-%m-%d")
                    
                    conexao = conectar()
                    cursor = conexao.cursor()
                    cursor.execute("INSERT INTO vendas (id_cliente, data_venda, total_venda) VALUES (?, ?, ?)", (id_cliente, data_venda, subtotal))
                    id_venda = cursor.lastrowid
                    cursor.execute("INSERT INTO detalhes_venda (id_venda, id_telemovel, quantidade, preco_unitario, subtotal) VALUES (?, ?, ?, ?, ?)", (id_venda, id_telemovel, quantidade, preco_unitario, subtotal))
                    novo_stock = stock_atual - quantidade
                    cursor.execute("UPDATE telemoveis SET stock = ? WHERE id_telemovel = ?", (novo_stock, id_telemovel))
                    conexao.commit()
                    conexao.close()
                    st.success(f"Venda registada com sucesso! Total: {subtotal:.2f} €")

    mostrar_botoes_navegacao()

# ---------------------------------------------------------
# PÁGINA: ANÁLISE E GRÁFICOS
# ---------------------------------------------------------
elif st.session_state.pagina_atual == "Análise e Gráficos":
    st.title("📊 Análise de Stock")
    
    conexao = conectar()
    query_stock = "SELECT marca || ' ' || modelo AS produto, stock FROM telemoveis ORDER BY stock DESC"
    grafico_df = pd.read_sql_query(query_stock, conexao)
    conexao.close()

    if grafico_df.empty:
        st.warning("Não existem dados suficientes para gerar gráficos.")
    else:
        st.subheader("📈 Distribuição de Stock por Produto")
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(grafico_df["stock"], labels=grafico_df["produto"], autopct='%1.1f%%', startangle=90, colors=['#4C72B0', '#55A868', '#C44E52', '#8172B3', '#CCB974'])
        ax.axis('equal')
        plt.tight_layout()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.pyplot(fig)
            
        st.markdown("---")
        st.download_button(
            label="📥 Descarregar Dados do Gráfico (JSON)",
            data=grafico_df.to_json(orient="records", force_ascii=False, indent=4),
            file_name="dados_grafico_stock.json",
            mime="application/json"
        )

    mostrar_botoes_navegacao()