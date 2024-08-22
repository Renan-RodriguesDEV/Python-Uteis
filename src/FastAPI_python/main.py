from fastapi import FastAPI

"""uvicorn main:app --reload -> para gerar link da api"""
"""uvicorn send_api:app --reload --host 0.0.0.0 --port 8000"""
conteudo_api = {
    1: {"bebidas": ["one"]},
    2: {"doces": ["two"]},
    3: {"salgados": ["tri"]},
    4: {
        "outros": [
            "for",
        ]
    },
}

# criando API
app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.get("/itens/{id}")
def pegar_item(id: int):
    return conteudo_api[id]


@app.post("/itens/{id}/{prod}/{acrecentado}")
def adicionar_item(id: int, prod: str, acrecentado: str):
    conteudo_api[id][prod].append(acrecentado)
    return conteudo_api[id][prod]
