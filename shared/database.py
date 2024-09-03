from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_user = 'millenium_falcon'
db_password = 'x_wing'
db_host = 'localhost'
db_port = 5432
db_name = 'contas_pagar_receber'

DATABASE_URL = f'postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
