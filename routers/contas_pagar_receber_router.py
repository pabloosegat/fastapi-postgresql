from decimal import Decimal
from enum import Enum
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from shared.dependencies import get_db
from models.contas_pagar_receber_model import ContaPagarReceber


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


@router.get('', response_model=List[ContaPagarReceberResponse])
def listar_contas(db: Session=Depends(get_db)) -> List[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).all()

@router.post('', response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest,
                db: Session=Depends(get_db)) -> ContaPagarReceberResponse: 
    
    contas_pagar_receber = ContaPagarReceber(
        **conta.dict()
    )
    
    db.add(contas_pagar_receber)
    db.commit()
    db.refresh(contas_pagar_receber)
    
    return contas_pagar_receber