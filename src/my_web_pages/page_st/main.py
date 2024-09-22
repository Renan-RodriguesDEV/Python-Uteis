import streamlit as st

side = st.sidebar.title("Opções")

pg2 = st.Page("pages/produtos.py", icon="📦")


# Função de autenticação simulada (exemplo simples)
def autenticar_usuario(username, password):
    # Aqui você pode adicionar lógica de verificação com um banco de dados ou API
    if username == "admin" and password == "1234":
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
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos")


# Função para a homepage
def homepage():
    st.title(f"Bem-vindo, {st.session_state['usuario']}!")

    # Opções de navegação
    if st.sidebar.button("Cadastro de Produtos"):
        st.session_state["pagina"] = "cadastro_produto"
        st.experimental_rerun()

    if st.sidebar.button("Cadastro de Clientes"):
        st.session_state["pagina"] = "cadastro_cliente"
        st.experimental_rerun()

    if st.sidebar.button("Consulta de Produtos"):
        st.session_state["pagina"] = "consulta_produto"
        st.experimental_rerun()

    if st.sidebar.button("Consulta de Dívida de Clientes"):
        st.session_state["pagina"] = "consulta_divida"
        st.experimental_rerun()

    if st.sidebar.button("Logout"):
        st.session_state["autenticado"] = False
        st.session_state["pagina"] = "login"
        st.experimental_rerun()


# Função para o cadastro de produtos
def cadastro_produto():
    st.title("Cadastro de Produtos")
    nome = st.text_input("Nome do Produto")
    preco = st.number_input("Preço", min_value=0.0, step=0.01)
    qtde = st.number_input("Quantidade", min_value=0, step=1)

    if st.button("Cadastrar Produto"):
        st.success(f"Produto {nome} cadastrado com sucesso!")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.experimental_rerun()


# Função para o cadastro de clientes
def cadastro_cliente():
    st.title("Cadastro de Clientes")
    nome = st.text_input("Nome do Cliente")
    email = st.text_input("Email do Cliente")
    telefone = st.text_input("Telefone do Cliente")

    if st.button("Cadastrar Cliente"):
        st.success(f"Cliente {nome} cadastrado com sucesso!")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.experimental_rerun()


# Função para a consulta de produtos
def consulta_produto():
    st.title("Consulta de Produtos")
    # Aqui você poderia listar os produtos cadastrados. Exemplo simples:
    st.write("Produto 1: Nome: Laptop, Preço: R$3000, Quantidade: 5")
    st.write("Produto 2: Nome: Teclado, Preço: R$150, Quantidade: 10")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.experimental_rerun()


# Função para a consulta de dívida de clientes
def consulta_divida():
    st.title("Consulta de Dívida de Clientes")
    # Simulação de consulta de dívida. Poderia ser ligado a um banco de dados.
    cliente = st.selectbox(
        "Selecione o cliente", ["Cliente 1", "Cliente 2", "Cliente 3"]
    )

    if cliente == "Cliente 1":
        st.write("Dívida Atual: R$ 500,00")
    elif cliente == "Cliente 2":
        st.write("Dívida Atual: R$ 1000,00")
    else:
        st.write("Dívida Atual: R$ 0,00")

    if st.button("Voltar"):
        st.session_state["pagina"] = "homepage"
        st.experimental_rerun()


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
