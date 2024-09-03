# import sys
# sys.path.append('./')

import uvicorn
from fastapi import FastAPI

from contas_pagar_receber.routers import contas_pagar_receber_router


app = FastAPI()

@app.get('/')
def hello_world() -> dict:
    return {'message': 'Hello, World!'}

app.include_router(contas_pagar_receber_router.router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True)