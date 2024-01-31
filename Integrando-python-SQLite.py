from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column, inspect, select, func
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Float


Base = declarative_base()


class Cliente(Base):
    __tablename__ = "cliente_account"
    #atributos
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    endereco = Column(String)


    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"


class Conta(Base):
    __tablename__ = "conta"
    id_conta = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)
    agencia = Column(String, nullable=False)
    numero = Column(Integer)
    saldo = Column(Float)   


    id_cliente = Column(Integer, ForeignKey("cliente_account.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Conta (id={self.id_cliente}, tipo={self.tipo}, agencia={self.agencia}, numero={self.numero}, saldo={self.saldo})"


print(Cliente.__tablename__)
print(Conta.__tablename__)
    
# conexão com Banco de Dados
engine = create_engine("sqlite://")

# criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# investiga o esquema de banco de dados
inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("cliente_account"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

# criando um sessão para persistir dados no SQlite
with Session(engine) as session:
    patricia = Cliente(
        nome='Patricia Silva',
        cpf=12345678900,
        endereco='Rua dos Alfeneiros, 4',
        conta=[Conta(tipo='corrente', agencia='001',  numero=775, saldo=300000)]
    )

    mateus = Cliente(
        nome='Mateus Henrique',
        cpf=11122233344,
        endereco='Beco Diagonal, 93',
        conta=[Conta(tipo='corrente', agencia='456',  numero=2222, saldo=10000)]
    )

    juliana = Cliente(
        nome='Juliana Mascarenhas',
        cpf=33344456789,
        endereco='Avenida Steve Jobs, 1',
        conta=[Conta(tipo='poupanca', agencia='789',  numero=3333, saldo=50)]
    )

    mario = Cliente(
        nome='Mario Bros',
        cpf=99988877766,
        endereco='Rua Luigi, 2',
        conta=[Conta(tipo='poupanca', agencia='000',  numero=444, saldo=25.10)]
    )

    joao = Cliente(
        nome='Joao Carlos',
        cpf=98798798766,
        endereco='Rua dos programadores, 7',
        conta=[Conta(tipo='corrente', agencia='789',  numero=1111, saldo=50)]
    )


    # enviando para o banco de dados (persistência de dados)
    session.add_all([patricia, mateus, juliana, mario, joao])

    session.commit()

# utilizando um statiment -- consulta de informações
stmt = select(Cliente).where(Cliente.nome.in_(['mateus']))

print('Recuperando usuários a partir de condição de filtragem')
for cliente in session.scalars(stmt):
    print(cliente)

# print('\nRecuperando os endereços de email de Mateus')
# stmt_address = select(Address).where(Address.user_id.in_([2]))
# for address in session.scalars(stmt_address):
#     print(address)


stmt_order = select(Cliente).order_by(Cliente.nome) #order_stmt = select(User).order_by(User.fullname.desc()) > ordem decrescente
print("\nRecuperando info de maneira ordenada")
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(Cliente.nome, Conta.saldo).join_from(Cliente, Conta)
print("\n")
for result in session.scalars(stmt_join):
    print(result)

#print(select(Cliente.nome, Conta.saldo).join_from(Cliente, Conta))

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(Cliente)
print("\nTotal de instâncias em Cliente")
for result in session.scalars(stmt_count):
    print(result)


