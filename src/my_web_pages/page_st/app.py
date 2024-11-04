import streamlit as st
from schemas import *

log_green("[==] Runnig server streamlit localhost [==]")
initialize_database()

st.set_page_config(
    page_title="Sistema de Gerenciamento de Vendas",
    page_icon=":moneybag:",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Função de autenticação simulada (exemplo simples)
@st.cache_data
def autenticar_usuario(username, password, type_user):
    if type_user == "Owner/Employee":
        user = select_user(username, password)
        log_red(
            f'[===] - User: {user.get("username")} [===] Password: {user.get("password")} - [===]'
        )
        # Aqui você pode adicionar lógica de verificação com um banco de dados ou API
        if username == user.get("username") and password == user.get("password"):
            return True
        return False
    elif type_user == "Client":
        user = select_user_client(username, password)
        log_red(
            f'[===] - User: {user.get("username")} [===] Password: {user.get("password")} - [===]'
        )
        # Aqui você pode adicionar lógica de verificação com um banco de dados ou API
        if username == user.get("username") and password == user.get("password"):
            return True
        return False
    return False


# Função para a tela de login
def tela_login():
    st.title("Faça seu Login para continuar")
    tipo_user = st.selectbox("Usuario", ["Owner/Employee", "Client"])
    log_blue(tipo_user)
    username = st.text_input("Usuário", help="Insira seu nome de usuario")
    password = st.text_input(
        "Senha",
        type="password",
        max_chars=14,
        help="insira sua senha de usuario, clientes insiram o CPF cadastrado",
    )
    if username == "" or password == "":
        st.warning("Por favor, preencha os campos de usuário e senha")
    if st.button("Login", type="primary"):
        if autenticar_usuario(username, password, type_user=tipo_user):
            st.session_state["autenticado"] = True
            st.session_state["owner"] = True if tipo_user == "Owner/Employee" else False
            st.session_state["usuario"] = username
            st.session_state["pagina"] = "homepage"  # Redireciona para a homepage
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")


# Função para a homepage
def homepage():
    st.title(f"Bem-vindo, {st.session_state['usuario']}!")
    x, y = st.columns([2, 1], gap="medium", vertical_alignment="top")
    # Opções de navegação
    x.text_area(
        "Feedback do cliente",
        placeholder="Deixe seu feedback aqui",
        max_chars=255,
        height=150,  # Define a altura fixa para o text_area
    )
    if y.button(
        "Cadastro de Produtos",
        use_container_width=True,
        disabled=not st.session_state["owner"],
    ):
        st.session_state["pagina"] = "cadastro_produto"
        st.rerun()
    if y.button(
        "Cadastro de Clientes",
        use_container_width=True,
        disabled=not st.session_state["owner"],
    ):
        st.session_state["pagina"] = "cadastro_cliente"
        st.rerun()

    if y.button("Consulta de Produtos", use_container_width=True):
        st.session_state["pagina"] = "consulta_produto"
        st.rerun()

    if y.button("Consulta de Dívida de Clientes", use_container_width=True):
        st.session_state["pagina"] = "consulta_divida"
        st.rerun()

    if y.button(
        "Atualizar Dívida de Clientes",
        use_container_width=True,
        disabled=not st.session_state["owner"],
    ):
        st.session_state["pagina"] = "atualizar_divida"
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

    if st.button("Cadastrar Produto", type="primary"):
        # preco = preco.replace(",", ".")
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

    if st.button("Cadastrar Cliente", type="primary"):
        cpf = cpf.replace(".", "").replace("-", "")
        register_client(nome, cpf, telefone, email)
        st.success(f"Cliente {nome} cadastrado com sucesso!")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


# Função para a consulta de produtos
def consulta_produto():
    st.title("Consulta de Produtos")
    produtos = select_all_produtos()
    # Aqui você poderia listar os produtos cadastrados. Exemplo simples:
    st.table(produtos)
    nome = st.text_input("Digite o nome do produto para consultar")
    produto = select_product_by_name(nome)
    if st.button("Consultar", type="primary"):
        if produto.shape[0] > 0:
            st.write(produto)
        else:
            st.error("Nenhum produto encontrado com esse nome")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


# Função para a consulta de dívida de clientes
def consulta_divida():
    if st.session_state["owner"]:
        st.title("Consulta de Dívida de Clientes")
        # Simulação de consulta de dívida. Poderia ser ligado a um banco de dados.
        df_clientes = select_all_clientes()

        cliente = st.selectbox(
            "Selecione o cliente",
            df_clientes["nome"].to_list(),
        )
        divida = select_debt_by_client(cliente)
        st.write(f"Divida do cliente {cliente}: R$ {divida}")
        if st.button("Consulta completa"):
            st.table(select_all_sales_by_client(cliente))
        if st.button("Voltar"):
            st.session_state["pagina"] = "homepage"
            st.rerun()
    else:
        st.title("Consulta de Dívida de Clientes")

        with st.form(key="consulta_form"):
            cliente = st.text_input("Nome completo")
            consultar = st.form_submit_button("Consultar")

        if consultar:
            divida = select_debt_by_client(cliente)
            st.write(f"Divida do cliente {cliente}: R$ {divida if divida else 0.00}")
            divida_total = select_all_sales_by_client(cliente)
            if divida_total is not None:
                st.table(divida_total)
            else:
                st.error("Nenhum cliente encontrado com esse nome")

        if st.button("Voltar"):
            st.session_state["pagina"] = "homepage"
            st.rerun()


def atualizar_divida():
    st.title("Atualizar Dívida de Clientes")
    # Simulação de consulta de dívida. Poderia ser ligado a um banco de dados.
    df_clientes = select_all_clientes()
    df_produtos = select_all_produtos()
    cliente = st.selectbox("Selecione o cliente", df_clientes["nome"].to_list())
    produto = st.selectbox("Selecione o produto", df_produtos)
    preco = select_price_by_name(produto)["preco"]
    quantidade = st.number_input("Quantidade", min_value=1, step=1)
    if st.button("Atualizar"):
        is_register = register_sale(cliente, produto, quantidade)
        if is_register:
            st.success(f"Venda registrada com sucesso!")
        else:
            st.error("Erro ao registrar a venda")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.rerun()


# Configurando a sessão para manter o estado do login e da página
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"  # Define a página inicial como login
# Inicializa "owner" com False por padrão, caso ainda não tenha sido definido
if "owner" not in st.session_state:
    st.session_state["owner"] = False
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
    elif st.session_state["pagina"] == "atualizar_divida":
        atualizar_divida()
else:
    tela_login()
