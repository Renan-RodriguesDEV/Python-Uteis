from requests import Session
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
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(255), nullable=False)
    preco = Column("preco", Double(10, 2), nullable=False)
    estoque = Column("estoque", Integer, nullable=False)


class Cliente(Base):
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(255), nullable=False)
    cpf = Column("cpf", String(11), nullable=True, unique=True)
    telefone = Column("telefone", String(15), nullable=True)
    email = Column("email", String(255), nullable=True)


class Cliente_Produto(Base):
    __tablename__ = "cliente_produto"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
