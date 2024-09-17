from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from shared.database import Base

class ContaPagarReceber(Base):
    __tablename__ = 'tbl_contas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    desc = Column(String(30))
    valor = Column(Numeric)
    tipo = Column(String(30))
    data_baixa = Column(DateTime())
    valor_baixa = Column(Numeric)
    esta_baixada = Column(Boolean, default=False)
    
    id_fornecedor_cliente = Column(Integer, ForeignKey('tbl_fornecedor_cliente.id'))
    fornecedor_cliente = relationship('FornecedorCliente')