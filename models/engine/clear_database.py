import sqlalchemy as sa
from sqlalchemy import create_engine, MetaData
from os import getenv
from dotenv import load_dotenv
from alembic import op


load_dotenv()
MYSQL_USER = getenv('DBUSER')
MYSQL_PWD = getenv('DBPWD')
MYSQL_HOST = getenv('HOST')
MYSQL_DB = getenv('DB')
ENV = getenv('ENV')
# print(MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_DB, ENV)
engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                            format(MYSQL_USER,
                                    MYSQL_PWD,
                                    MYSQL_HOST,
                                    MYSQL_DB),
                            pool_pre_ping=True)
# print(engine)
# metadata = MetaData()

# metadata.reflect(bind=engine)

# metadata.drop_all(bind=engine)

def upgrade():
    op.add_column('users', sa.Column('password', sa.String(128), nullable=False))

def downgrade():
    op.drop_column('users', 'password')