from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Float

engine = create_engine('sqlite:///:memory')

metadata_obj = MetaData()
user = Table(
    'user',
    metadata_obj,
    Column('cliente_id', Integer, primary_key=True),
    Column('cliente_name', String(40), nullable=False),
    Column('cpf', String(11)),
    Column('endereco', String(50), nullable=False)
)

user_prefs = Table(
    'user_prefs', metadata_obj,
    Column('pref_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
    Column('pref_name', String(40), nullable=False),
    Column('pref_value', String(100))
)

for table in metadata_obj.sorted_tables:
    print(table)