import streamlit as st

from schemas import *


# Função de autenticação simulada (exemplo simples)
@st.cache_data
def autenticar_usuario(username, password):
    user = select_user(username, password)
    print(user.get("username"), user.get("password"))
    # Aqui você pode adicionar lógica de verificação com um banco de dados ou API
    if username == user.get("username") and password == user.get("password"):
        return True
    return False


# Função para a tela de login
def tela_login():
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        if autenticar_usuario(username, password):
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = username
            st.session_state["pagina"] = "homepage"  # Redireciona para a homepage
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")


# Função para a homepage
def homepage():
    st.title(f"Bem-vindo, {st.session_state['usuario']}!")

    # Opções de navegação
    if st.button("Cadastro de Produtos"):
        st.session_state["pagina"] = "cadastro_produto"
        st.rerun()
    if st.button("Cadastro de Clientes"):
        st.session_state["pagina"] = "cadastro_cliente"
        st.rerun()

    if st.button("Consulta de Produtos"):
        st.session_state["pagina"] = "consulta_produto"
        st.rerun()

    if st.button("Consulta de Dívida de Clientes"):
        st.session_state["pagina"] = "consulta_divida"
        st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state["autenticado"] = False
        st.session_state["pagina"] = "login"
        st.rerun()


# Função para o cadastro de produtos
def cadastro_produto():
    st.title("Cadastro de Produtos")
    nome = st.text_input("Nome do Produto")
    preco = st.number_input("Preço", min_value=0.0, step=0.01)
    qtde = st.number_input("Quantidade", min_value=0, step=1)

    if st.button("Cadastrar Produto"):
        register_product(nome, float(preco), int(qtde))
        st.success(f"Produto {nome} cadastrado com sucesso!")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


# Função para o cadastro de clientes
def cadastro_cliente():
    st.title("Cadastro de Clientes")
    nome = st.text_input("Nome do Cliente")
    cpf = st.text_input("CPF do Cliente", placeholder="123.456.789-00")
    email = st.text_input("Email do Cliente", placeholder="kriptovenio@gmail.com")
    telefone = st.text_input("Telefone do Cliente")

    if st.button("Cadastrar Cliente"):
        cpf = cpf.replace(".", "").replace("-", "")
        register_client(nome, cpf, telefone, email)
        st.success(f"Cliente {nome} cadastrado com sucesso!")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


# Função para a consulta de produtos
def consulta_produto():
    st.title("Consulta de Produtos")
    produtos = select_all_produtoss()
    # Aqui você poderia listar os produtos cadastrados. Exemplo simples:
    st.table(produtos)
    nome = st.text_input("Digite o nome do produto para consultar")
    produto = select_product_by_name(nome)
    if st.button("Consultar"):
        if produto.shape[0] > 0:
            st.write(produto)
        else:
            st.error("Nenhum produto encontrado com esse nome")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


# Função para a consulta de dívida de clientes
def consulta_divida():
    st.title("Consulta de Dívida de Clientes")
    # Simulação de consulta de dívida. Poderia ser ligado a um banco de dados.
    df_clientes = select_all_clientes()

    cliente = st.selectbox("Selecione o cliente", df_clientes["nome"].to_list())
    divida = select_debt_by_client(cliente)
    st.write(f"Divida do cliente {cliente}: R$ {divida}")
    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


# Configurando a sessão para manter o estado do login e da página
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"  # Define a página inicial como login

# Verifica se o usuário está autenticado
if st.session_state["autenticado"]:
    # Navega entre as páginas com base no estado
    if st.session_state["pagina"] == "homepage":
        homepage()
    elif st.session_state["pagina"] == "cadastro_produto":
        cadastro_produto()
    elif st.session_state["pagina"] == "cadastro_cliente":
        cadastro_cliente()
    elif st.session_state["pagina"] == "consulta_produto":
        consulta_produto()
    elif st.session_state["pagina"] == "consulta_divida":
        consulta_divida()
else:
    tela_login()
