import requests
import json

# URL da API (note que há um espaço vazio onde deveria estar o ID do número de telefone)
url = "https://graph.facebook.com/v20.0//messages"

# Token de acesso à API
access_token = "<ACESS_TOKEN>"

# Cabeçalhos da requisição
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

# Dados da requisição (corpo do JSON)
data = {
    "messaging_product": "whatsapp",
    "to": "",  # Número de telefone do destinatário (formato internacional, ex: "5511999999999")
    "type": "template",
    "template": {"name": "hello_world", "language": {"code": "en_US"}},
}

# Enviar a requisição POST
response = requests.post(url, headers=headers, data=json.dumps(data))

# Verificar o resultado da requisição
if response.status_code == 200:
    print("Mensagem enviada com sucesso!")
    print(response.json())  # Exibe a resposta JSON
else:
    print(f"Erro ao enviar mensagem: {response.status_code}")
    print(response.text)  # Exibe a mensagem de erro
