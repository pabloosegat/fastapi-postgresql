from decimal import Decimal
from enum import Enum
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from shared.dependencies import get_db
from models.contas_pagar_receber_model import ContaPagarReceber
from shared.exceptions import NotFound


router = APIRouter(prefix='/contas-pagar-receber')

class ContaPagarReceberResponse(BaseModel):
    id: int
    desc: str
    valor: Decimal
    tipo: str
    
    class Config:
        orm_mode = True

class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = 'pagar'
    RECEBER = 'receber'

class ContaPagarReceberRequest(BaseModel):
    desc: str = Field(min_length=3, max_length=30)
    valor: Decimal = Field(gt=0, )
    tipo: ContaPagarReceberTipoEnum

# CRUD

# Create
@router.post('', response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest,
                db: Session=Depends(get_db)) -> ContaPagarReceberResponse: 
    
    conta_pagar_receber = ContaPagarReceber(
        **conta.dict()
    )
    
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
    
    conta.desc = conta_request.desc
    conta.valor = conta_request.valor
    conta.tipo = conta_request.tipo
    
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