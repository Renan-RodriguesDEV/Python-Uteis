from sqlalchemy import (
    create_engine,
    Integer,
    String,
    Column,
    Boolean,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import sessionmaker, declarative_base

user = "root"
host = "localhost"
database = "loja"
password = ""
db = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

# Cria uma Classe sessão para interagir com o banco de dados
Session = sessionmaker(bind=db)

# Esta classe de sessao para interagir com o banco de dados
session = Session()

# Cria uma Classe Base para contruirmos as tabelas
Base = declarative_base()


# Tabelas
class Cliente(Base):
    # define o nome da tabela
    __tablename__ = "clientes"

    # campos da coluna de clientes
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(50))
    cpf = Column("cpf", String(14), unique=True)

    # construtor da classe para sempre que for estanciar/criar cliente novo no bd
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf


# Create a new client
def create_cliente(nome: str, cpf: str):
    cliente = Cliente(nome=nome, cpf=cpf)
    # Add a sessao nosso novo cliente
    session.add(cliente)
    # Commita as mudanças
    session.commit()
    print("### Cliente inserido com sucesso ###")


# Read
# Pega uma lista
def get_all_client():
    return session.query(Cliente).all()


# Pega um cliente
def get_first_client():
    return session.query(Cliente).first()


# Pega um cliente pelo filtro, parametro são os atributos da classe Cliente
def get_cliente_by_name(name: str):
    return session.query(Cliente).filter_by(nome=name).first()


# Atualiza um cliente
def update_name_cpf(cliente: Cliente, new_name, new_cpf):
    cliente.nome = new_name
    cliente.cpf = new_cpf
    session.add(cliente)
    session.commit()
    print("### Cliente atualizado com sucesso ###")


# Apaga um cliente
def delete_cliente(cliente: Cliente):
    session.delete(cliente)
    session.commit()
    print("### Cliente deletado com sucesso ###")


# Crie todas as tabelas
Base.metadata.create_all(db)

if __name__ == "__main__":
    # create_cliente("Renan", "456.719.678-30")

    clientes = get_all_client()
    cliente = get_first_client()
    cliente_ = get_cliente_by_name("Renan")
    for c in clientes:
        print(f"Clientes: {c.nome}")
        print(f"Clientes: {c.cpf}")

    print(f"Cliente: {cliente.nome}")
    print(f"Cliente: {cliente.cpf}")
    print(f"Filtrado: {cliente_.nome}")
    print(f"Filtrado: {cliente_.cpf}")

    # delete_cliente(cliente_)
