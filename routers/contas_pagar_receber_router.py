from decimal import Decimal
from enum import Enum
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from shared.dependencies import get_db
from models.contas_pagar_receber_model import ContaPagarReceber
from models.fornecedor_cliente_model import FornecedorCliente
from routers.fornecedor_cliente_router import FornecedorClienteResponse
from shared.exceptions import ContaNotFound, FornecedorNotFound


router = APIRouter(prefix='/contas-pagar-receber')

class ContaPagarReceberResponse(BaseModel):
    id: int
    desc: str
    valor: Decimal
    tipo: str
    data_baixa:  Optional[datetime] = None
    valor_baixa:  Optional[Decimal] = None
    esta_baixada:  Optional[bool] = None
    fornecedor_cliente: Optional[FornecedorClienteResponse] = None
    
    class Config:
        orm_mode = True

class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = 'pagar'
    RECEBER = 'receber'

class ContaPagarReceberRequest(BaseModel):
    desc: str = Field(min_length=3, max_length=30)
    valor: Decimal = Field(gt=0)
    tipo: ContaPagarReceberTipoEnum
    id_fornecedor_cliente: Optional[int] = None

# CRUD

# Create
@router.post('', response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta_request: ContaPagarReceberRequest,
                db: Session=Depends(get_db)) -> ContaPagarReceberResponse: 
    valida_fornecedor(conta_request.id_fornecedor_cliente, db)
    
    conta = ContaPagarReceber(
        **conta_request.dict()
    )
    
    db.add(conta)
    db.commit()
    db.refresh(conta)
    
    return conta

# Read
@router.get('', response_model=List[ContaPagarReceberResponse])
def listar_contas(db: Session=Depends(get_db)) -> List[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).all()

@router.get('/{id_conta}', response_model=ContaPagarReceberResponse)
def listar_uma_conta(id_conta: int,
                    db: Session=Depends(get_db)) -> ContaPagarReceberResponse:
    conta = consultar_conta_por_id(id_conta, db)
    
    return conta

# Update
@router.put('/{id_conta}', response_model=ContaPagarReceberResponse, status_code=200)
def atualizar_conta(id_conta: int,
                conta_request: ContaPagarReceberRequest,
                db: Session=Depends(get_db)) -> ContaPagarReceberResponse:
    valida_fornecedor(conta_request.id_fornecedor_cliente, db)
    
    conta = consultar_conta_por_id(id_conta, db)
    
    
    conta.desc = conta_request.desc
    conta.valor = conta_request.valor
    conta.tipo = conta_request.tipo
    conta.id_fornecedor_cliente = conta_request.id_fornecedor_cliente
    
    db.add(conta)
    db.commit()
    db.refresh(conta)
    
    return conta

@router.post('/{id_conta}/baixar', response_model=ContaPagarReceberResponse, status_code=200)
def baixar_conta(id_conta: int,
                db: Session=Depends(get_db)) -> ContaPagarReceberResponse:
    
    conta += consultar_conta_por_id(id_conta, db)
    
    if not conta.esta_baixada or (conta.esta_baixada and conta.valor != conta.valor):
        conta.data_baixa = datetime.now()
        conta.esta_baixada = True
        conta.valor_baixa = conta.valor
    
        db.add(conta)
        db.commit()
        db.refresh(conta)
    
    return conta

# Delete
@router.delete('/{id_conta}', status_code=204)
def deletar_conta(id_conta: int,
                db: Session=Depends(get_db)):
    
    conta = consultar_conta_por_id(id_conta, db)
    db.delete(conta)
    
    db.commit()


def consultar_conta_por_id(id_conta: int,
                        db: Session=Depends(get_db)) -> ContaPagarReceber:
    conta: ContaPagarReceber = db.get(ContaPagarReceber, id_conta)
    
    if conta is None:
        raise ContaNotFound
    
    return conta

def valida_fornecedor(id_fornecedor_cliente: int,
                    db: Session=Depends(get_db)):
    if id_fornecedor_cliente is not None:
        fornecedor_cliente: FornecedorCliente = db.get(FornecedorCliente, id_fornecedor_cliente)
        if fornecedor_cliente is None:
            raise FornecedorNotFound