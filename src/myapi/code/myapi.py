import requests

# URL da API
url = "http://127.0.0.1:8080/send"

# Parâmetros de consulta (query parameters)
params = {
    "num": "1234567890",
    "msg": "Hello World",
    "time": "10:30"
}

# Fazendo a requisição POST
response = requests.post(url, params=params)

# Exibindo a resposta da API
print("Resposta da API:", response.json())
