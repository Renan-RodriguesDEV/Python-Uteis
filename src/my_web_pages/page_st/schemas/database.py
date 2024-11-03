from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Double,
)
from sqlalchemy.orm import sessionmaker, declarative_base

user = "root"
host = "localhost"
database = "db_comercio"
password = ""
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Produto(Base):
    __tablename__ = "produtos"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(255), nullable=False)
    preco = Column("preco", Double(10, 2), nullable=False)
    estoque = Column("estoque", Integer, nullable=False)

    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque


class Cliente(Base):
    __tablename__ = "clientes"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(255))
    cpf = Column("cpf", String(11), nullable=True, unique=True)
    telefone = Column("telefone", String(15), nullable=True)
    email = Column("email", String(255), nullable=True)

    def __init__(self, nome, cpf=None, telefone=None, email=None):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(255), nullable=False)
    senha = Column("senha", String(13), nullable=True, unique=True)

    def __init__(self, nome, senha=None):
        self.nome = nome
        self.senha = senha


class Cliente_Produto(Base):
    __tablename__ = "cliente_produto"
    id = Column(
        "id", Integer, primary_key=True, autoincrement=True
    )  # Adiciona chave primária
    id_cliente = Column("id_cliente", ForeignKey("clientes.id"), nullable=False)
    id_produto = Column("id_produto", ForeignKey("produtos.id"), nullable=False)
    preco = Column("preco", Double(10, 2))
    quantidade = Column(
        "quantidade",
        Integer,
    )
    total = Column("total", Double(10, 2))
    data = Column("data", DateTime())


def initialize_database():
    # Criação das tabelas no banco de dados
    Base.metadata.create_all(engine)
    print(("### Initialization database sucessfully ###"))
