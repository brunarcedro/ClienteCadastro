from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

origins = ['http://localhost:5500']

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class Cliente(BaseModel):
    id: Optional[int]
    nome_completo: str
    data_nascimento: str
    cpf: str
    numero_telefone: str
    email: str

banco_clientes: List[Cliente] = []
cliente_id_counter = 1

@app.get('/clientes')
def listar_clientes():
    return banco_clientes

@app.post('/clientes')
def criar_cliente(cliente: Cliente):
    global cliente_id_counter
    try:
        cliente.id = cliente_id_counter
        banco_clientes.append(cliente)
        cliente_id_counter += 1
        return cliente
    except Exception as e:
        print("Erro ao criar cliente:", e)
        raise HTTPException(status_code=500, detail="Erro interno do servidor ao criar cliente")

@app.delete('/clientes/{cliente_id}')
def deletar_cliente(cliente_id: int):
    try:
        for index, cliente in enumerate(banco_clientes):
            if cliente.id == cliente_id:
                del banco_clientes[index]
                return None
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    except Exception as e:
        print("Erro ao deletar cliente:", e)
        raise HTTPException(status_code=500, detail="Erro interno do servidor ao deletar cliente")