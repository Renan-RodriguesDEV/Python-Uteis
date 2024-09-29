from fastapi.responses import RedirectResponse
from fastapi import FastAPI
import uvicorn

# TODO: Para rodar no terminal -> uvicorn {nome_do_arquivo}:app --reload --port 8080
app = FastAPI()

dados = {"numero": "", "msg": "", "time": ""}


@app.post("/send")
def deploy(num: str, msg: str, time: str):
    dados["numero"] = num
    dados["msg"] = msg
    dados["time"] = time
    return dados


@app.get("/")
def getdata():
    return dados


@app.get("/redirect", tags=["redirect"])
def redrect():

    return RedirectResponse(url="https://www.youtube.com/")


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
