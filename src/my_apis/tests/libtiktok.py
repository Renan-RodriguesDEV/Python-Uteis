import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def homepage():
    return "Run API of libtiktok"


@app.get("/libtiktok")
def libtiktok():
    return {"libtiktok": "status code -- 200"}

if __name__ == "__main__":
    uvicorn.run('libtiktok:app', host="127.0.0.1", port=8000, reload=True, )
# para rodar no terminal -> uvicorn nomearquivo:nomeapp --reload