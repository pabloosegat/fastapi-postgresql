from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from routers.contas_pagar_receber_router import ContaPagarReceberResponse
from models.contas_pagar_receber_model import ContaPagarReceber
from shared.dependencies import get_db


router = APIRouter(prefix='/fornecedor-cliente')

@router.get('/{id_fornecedor_cliente}/contas-pagar-receber', response_model=List[ContaPagarReceberResponse])
def obter_contas_pagar_receber_fornecedor_cliente(id_fornecedor_cliente: int,
                                db: Session=Depends(get_db)) -> List[ContaPagarReceberResponse]:
    
    return db.query(ContaPagarReceber).filter_by(id_fornecedor_cliente=id_fornecedor_cliente).all()