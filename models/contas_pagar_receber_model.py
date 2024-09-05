from sqlalchemy import Column, Integer, Numeric, String
from shared.database import Base

class ContaPagarReceber(Base):
    __tablename__ = 'tbl_contas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    desc = Column(String(30))
    valor = Column(Numeric)
    tipo = Column(String(30))