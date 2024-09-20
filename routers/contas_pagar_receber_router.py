from decimal import Decimal
from enum import Enum
from typing import List, Optional
from datetime import date

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import extract
from sqlalchemy.orm import Session

from shared.dependencies import get_db
from models.contas_pagar_receber_model import ContaPagarReceber
from models.fornecedor_cliente_model import FornecedorCliente
from routers.fornecedor_cliente_router import FornecedorClienteResponse
from shared.exceptions import ContaNotFound, FornecedorNotFound, MonthlyAccountLimitExceededException


QTD_PERMITIDA_MES = 5

router = APIRouter(prefix='/contas-pagar-receber')

class ContaPagarReceberResponse(BaseModel):
    id: int
    desc: str
    valor: Decimal
    tipo: str
    data_previsao: date
    data_baixa:  Optional[date] = None
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
    data_previsao: date

class PrevisaoPorMes(BaseModel):
    mes: int
    valor_total: Decimal

# CRUD

# Create
@router.post('',
    response_model=ContaPagarReceberResponse,
    status_code=201,
    summary='Criar conta',
    description='Cria uma nova conta a pagar/receber'
)
def criar_conta(conta_request: ContaPagarReceberRequest,
                db: Session=Depends(get_db)) -> ContaPagarReceberResponse: 
    valida_fornecedor(conta_request.id_fornecedor_cliente, db)
    valida_limite_de_registro_nova_conta(conta_request, db)
        
    conta = ContaPagarReceber(
        **conta_request.dict()
    )
    
    db.add(conta)
    db.commit()
    db.refresh(conta)
    
    return conta

# Read
@router.get('',
    response_model=List[ContaPagarReceberResponse],
    summary='Listar contas',
    description='Retorna uma lista de todas as contas'
)
def listar_contas(db: Session=Depends(get_db)) -> List[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).all()

@router.get('/previsao-gastos-por-mes',
    response_model=List[PrevisaoPorMes],
    summary='Relatorio gastos previstos no mes',
    description='Retorna um relatorio de gastos previstos para cada mês'
)
def previsao_gastos_por_mes(ano: int = date.today().year,
                    db: Session=Depends(get_db)) -> List[PrevisaoPorMes]:
    return relatorio_gastos_previstos_para_o_mes(db, ano)

@router.get('/{id_conta}',
    response_model=ContaPagarReceberResponse,
    summary='Retornar conta pelo ID',
    description='Retorna uma conta específica pelo seu ID'
)
def listar_uma_conta(id_conta: int,
                    db: Session=Depends(get_db)) -> ContaPagarReceberResponse:
    conta = obter_conta_por_id(id_conta, db)
    
    return conta

# Update
@router.put('/{id_conta}',
    response_model=ContaPagarReceberResponse,
    status_code=200,
    summary='Atualizar conta',
    description='Atualiza os detalhes de uma conta existente'
)
def atualizar_conta(id_conta: int,
                conta_request: ContaPagarReceberRequest,
                db: Session=Depends(get_db)) -> ContaPagarReceberResponse:
    valida_fornecedor(conta_request.id_fornecedor_cliente, db)
    
    conta = obter_conta_por_id(id_conta, db)
    
    conta.desc = conta_request.desc
    conta.valor = conta_request.valor
    conta.tipo = conta_request.tipo
    conta.id_fornecedor_cliente = conta_request.id_fornecedor_cliente
    
    db.add(conta)
    db.commit()
    db.refresh(conta)
    
    return conta

@router.post('/{id_conta}/baixar',
    response_model=ContaPagarReceberResponse,
    status_code=200,
    summary='Baixar conta',
    description='Marca uma conta como baixada (paga ou recebida)'
)
def baixar_conta(id_conta: int,
                db: Session=Depends(get_db)) -> ContaPagarReceberResponse:
    
    conta += obter_conta_por_id(id_conta, db)
    
    if not conta.esta_baixada or (conta.esta_baixada and conta.valor != conta.valor):
        conta.data_baixa = date.today()
        conta.esta_baixada = True
        conta.valor_baixa = conta.valor
    
        db.add(conta)
        db.commit()
        db.refresh(conta)
    
    return conta

# Delete
@router.delete('/{id_conta}',
    status_code=204,
    summary='Deletar conta',
    description='Remove uma conta existente do sistema'
)
def deletar_conta(id_conta: int,
                db: Session=Depends(get_db)):
    
    conta = obter_conta_por_id(id_conta, db)
    db.delete(conta)
    
    db.commit()


# Auxiliar functions
def obter_conta_por_id(id_conta: int,
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

def contar_registros_por_mes(db, mes, ano) -> int:
    qtd_registros = db.query(ContaPagarReceber) \
                        .filter(extract('month', ContaPagarReceber.data_previsao) == mes) \
                        .filter(extract('year', ContaPagarReceber.data_previsao) == ano).count()
    
    return qtd_registros

def valida_limite_de_registro_nova_conta(conta_request: ContaPagarReceberRequest, db) -> None:
    if contar_registros_por_mes(db, conta_request.data_previsao.month, conta_request.data_previsao.year) >= QTD_PERMITIDA_MES:
        raise MonthlyAccountLimitExceededException
    
def relatorio_gastos_previstos_para_o_mes(db, ano) -> List[PrevisaoPorMes]:
    contas = db.query(ContaPagarReceber) \
                .filter(extract('year', ContaPagarReceber.data_previsao) == ano) \
                .filter(ContaPagarReceber.tipo == ContaPagarReceberTipoEnum.PAGAR) \
                .order_by(ContaPagarReceber.data_previsao).all()
    
    valor_por_mes = {}
    for conta in contas:
        mes = conta.data_previsao.month
        
        if valor_por_mes.get(mes) is None:
            valor_por_mes[mes] = 0
        
        valor_por_mes[mes] += conta.valor
    
    return [PrevisaoPorMes(mes=m, valor_total=v) for m, v in valor_por_mes.items()]