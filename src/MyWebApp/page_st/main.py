import streamlit as st

# Title
st.title("Streamlit App")

st.write("this my page with streamlit")

# Sidebar
st.sidebar.title("Menu")


def logar():
    # redicerionar para a página de login
    st.switch_page("login.py")


def cadastros():
    # redicerionar para a página de login
    st.switch_page("cadastros.py")


def produtos():
    # redicerionar para a página de login
    st.switch_page("produtos.py")


def clietes():
    # redicerionar para a página de login
    st.switch_page("produtos.py")


st.sidebar.subheader("Menu de Opções")
st.sidebar.button("Login", on_click=logar)
st.sidebar.button("Cadastros", on_click=cadastros)
st.sidebar.button("Produtos", on_click=produtos)
