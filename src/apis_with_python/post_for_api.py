import requests


def post_api(id: int, prod: str, acrecentado: str):
    params = {"acrecentado": acrecentado}
    requests.post(f"http://127.0.0.1:8080/itens/{id}/{prod}/", params=params)


def pegar_dados(id: int):
    response = requests.get(f"http://127.0.0.1:8080/itens/{id}")
    print(response.json())


post_api(1, "bebidas", "guarana-jesus")
pegar_dados(1)
