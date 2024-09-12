from fastapi import FastAPI
import uvicorn

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


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
