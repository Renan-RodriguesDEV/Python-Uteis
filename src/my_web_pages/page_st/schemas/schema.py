import pymysql
import pandas as pd

db_data = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "padaria",
    "cursorclass": pymysql.cursors.DictCursor,
}


# Função para selecionar todos os produtos
def select_all_produtoss():
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute("SELECT nome FROM produtos")
            df = pd.DataFrame(cursor.fetchall())
            return df


# Função para selecionar todos os clientes
def select_all_clientes():
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute("SELECT nome FROM clientes")
            df = pd.DataFrame(cursor.fetchall())
            return df


# Função para selecionar o preço do produto pelo nome
def select_price_by_name(name):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute("SELECT preco FROM produtos WHERE nome = %s", (name,))
            df = pd.DataFrame(cursor.fetchall())
            return df


# Função para selecionar o cliente pelo nome
def select_cliente_by_name(name):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute("SELECT nome FROM clientes WHERE nome = %s", (name,))
            df = pd.DataFrame(cursor.fetchall())
            return df


# Função para selecionar o estoque pelo nome do produto
def select_count_by_name(name):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute("SELECT estoque FROM produtos WHERE nome = %s", (name,))
            df = pd.DataFrame(cursor.fetchall())
            return df


# Função para registrar um produto
def register_product(name, price, count):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            cursor.execute(
                "INSERT INTO produtos (nome, preco, estoque) VALUES (%s, %s, %s)",
                (name, price, count),
            )
            connective.commit()
            return True


# Função para registrar um cliente
def register_client(name, cpf, telefone, email):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            sentence = "INSERT INTO clientes (nome, cpf, telefone, email) VALUES (%s, %s, %s, %s)"
            cursor.execute(
                sentence,
                (name, cpf, telefone, email),
            )
            connective.commit()
            return True


# Função para registrar uma venda
def register_sale(cliente, produtos_quantidade):
    """
    Registra uma venda para um cliente, inserindo ou atualizando a quantidade de produtos adquiridos.

    :param cliente: Nome do cliente.
    :param produtos_quantidade: Lista de tuplas com (id_produto, quantidade).
    """
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            # Obter o ID do cliente pelo nome
            cursor.execute("SELECT id FROM clientes WHERE nome = %s", (cliente,))
            result = cursor.fetchone()
            if result:
                id_cliente = result["id"]
            else:
                raise ValueError(f"Cliente '{cliente}' não encontrado.")

            # Inserir ou atualizar cada produto comprado
            for id_produto, quantidade in produtos_quantidade:
                # Verificar se o cliente já comprou este produto
                cursor.execute(
                    """
                    SELECT quantidade FROM cliente_produto 
                    WHERE id_cliente = %s AND id_produto = %s
                    """,
                    (id_cliente, id_produto),
                )
                existing = cursor.fetchone()

                if existing:
                    # Atualizar a quantidade se o produto já foi comprado antes
                    nova_quantidade = existing["quantidade"] + quantidade
                    cursor.execute(
                        """
                        UPDATE cliente_produto 
                        SET quantidade = %s, preco = (
                            SELECT preco FROM produtos WHERE id = %s
                        )
                        WHERE id_cliente = %s AND id_produto = %s
                        """,
                        (nova_quantidade, id_produto, id_cliente, id_produto),
                    )
                else:
                    # Inserir nova compra
                    cursor.execute(
                        """
                        INSERT INTO cliente_produto (id_cliente, id_produto, preco, quantidade)
                        VALUES (%s, %s, (SELECT preco FROM produtos WHERE id = %s), %s)
                        """,
                        (id_cliente, id_produto, id_produto, quantidade),
                    )

            connective.commit()
            return True


# Função para consultar a dívida do cliente
def select_debt_by_client(cliente):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            query = """
                SELECT SUM(p.preco * cp.quantidade) AS divida_total
                FROM produtos p
                JOIN cliente_produto cp ON p.id = cp.id_produto
                JOIN clientes c ON c.id = cp.id_cliente
                WHERE c.nome = %s
            """
            cursor.execute(query, (cliente,))
            df = pd.DataFrame(cursor.fetchall(), columns=["divida_total"])
            return df


def select_user(name, passwd):
    connective = pymysql.connect(**db_data)
    with connective as connective:
        with connective.cursor() as cursor:
            query = "SELECT * FROM users WHERE nome = %s AND senha = %s"
            cursor.execute(query, (name, passwd))
            result = cursor.fetchone()
            if result:
                senha = result["senha"]
                usuario = result["nome"]
                return {"username": usuario, "password": senha}
            else:
                return {"username": "", "password": ""}


# Teste básico
if __name__ == "__main__":
    df = select_price_by_name("banana")
    print(df)
