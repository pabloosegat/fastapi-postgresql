from decimal import Decimal
from enum import Enum
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from shared.dependencies import get_db
from models.contas_pagar_receber_model import ContaPagarReceber
from models.fornecedor_cliente_model import FornecedorCliente
from routers.fornecedor_cliente_router import FornecedorClienteResponse
from shared.exceptions import NotFound



router = APIRouter(prefix='/contas-pagar-receber')

class ContaPagarReceberResponse(BaseModel):
    id: int
    desc: str
    valor: Decimal
    tipo: str
    fornecedor_cliente: Union[FornecedorClienteResponse, None] = None
    
    class Config:
        orm_mode = True

class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = 'pagar'
    RECEBER = 'receber'

class ContaPagarReceberRequest(BaseModel):
    desc: str = Field(min_length=3, max_length=30)
    valor: Decimal = Field(gt=0)
    tipo: ContaPagarReceberTipoEnum
    id_fornecedor_cliente: Union[int, None] = None

# CRUD

# Create
@router.post('', response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest,
                db: Session=Depends(get_db)) -> ContaPagarReceberResponse: 
    conta_pagar_receber = ContaPagarReceber(
        **conta.dict()
    )
    
    valida_fornecedor(conta_pagar_receber.id_fornecedor_cliente, db)
    
    db.add(conta_pagar_receber)
    db.commit()
    db.refresh(conta_pagar_receber)
    
    return conta_pagar_receber

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
    
    conta = consultar_conta_por_id(id_conta, db)
    
    valida_fornecedor(conta.id_fornecedor_cliente, db)
    
    conta.desc = conta_request.desc
    conta.valor = conta_request.valor
    conta.tipo = conta_request.tipo
    conta.id_fornecedor_cliente = conta_request.id_fornecedor_cliente
    
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
        raise NotFound('Conta')
    
    return conta

def valida_fornecedor(id_fornecedor_cliente: int,
                    db: Session=Depends(get_db)):
    if id_fornecedor_cliente is not None:
        fornecedor_cliente = db.get(FornecedorCliente, id_fornecedor_cliente)
        if fornecedor_cliente is None:
            raise NotFound('Fornecedor')