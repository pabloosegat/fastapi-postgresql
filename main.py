import uvicorn
from fastapi import FastAPI

from routers import contas_pagar_receber_router
from routers import fornecedor_cliente_router
from shared.exceptions import NotFound
from shared.exceptions_handler import not_found_exception_handler


app = FastAPI()
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

@app.get('/')
def hello_world() -> dict:
    return {'message': 'Hello, World!'}

app.include_router(contas_pagar_receber_router.router)
app.include_router(fornecedor_cliente_router.router)
app.add_exception_handler(NotFound, not_found_exception_handler)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True)