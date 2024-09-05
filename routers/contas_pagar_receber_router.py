from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from shared.dependencies import get_db
from models.contas_pagar_receber_model import ContaPagarReceber


router = APIRouter(prefix='/contas-pagar-receber')

class ContaPagarReceberResponse(BaseModel):
    id: int
    desc: str
    valor: float
    tipo: str
    
    class Config:
        orm_mode = True

class ContaPagarReceberRequest(BaseModel):
    desc: str
    valor: float
    tipo: str


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