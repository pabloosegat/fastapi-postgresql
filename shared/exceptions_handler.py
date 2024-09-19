from fastapi import Request
from fastapi.responses import JSONResponse

from shared.exceptions import ContaNotFound, FornecedorNotFound, MonthlyAccountLimitExceededException


async def conta_not_found_handler(request: Request, exc: ContaNotFound):
    return JSONResponse(
        status_code=404,
        content={'message': exc.message}
    )

async def fornecedor_not_found_handler(request: Request, exc: FornecedorNotFound):
    return JSONResponse(
        status_code=404,
        content={'message': exc.message}
    )

async def monthly_account_limit_exceeded_handler(request: Request, exc: MonthlyAccountLimitExceededException):
    return JSONResponse(
        status_code=404,
        content={'message': exc.message}
    )