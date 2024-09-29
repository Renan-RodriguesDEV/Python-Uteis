import requests
import json

# URL da API (note que há um espaço vazio onde deveria estar o ID do número de telefone)


# url = "https://graph.facebook.com/v20.0//messages"
# Configurações
phone_number_id = "422087710990271"

# Token de acesso à API
access_token = "EAAFPzmpZAYyEBOzqgVgqET9DNgdgTgxp6brOZCQcurik5kt5yRQhZAU22OAj6KqA069M47y0TFNZC6BZBcwBLoJrHYIZBjnNw4fGdz8rZCpEuBG27h7hHDIp4zhmoFJwRHHXXTmt5knm6cfZAjFMHLnKOblA9UByAEuFap0yDqfZCdfIBqw2FXo6p5gQ8r6AtNaotLyMVcskwAAZAUuJ18W2eIPw2kA2gZD"

to_phone_number = "11122233344"

url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

data = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": to_phone_number,
    "type": "interactive",
    "interactive": {
        "type": "button",
        "header": {
            "type": "image",
            "image": {"link": "https://exemplo.com/imagem.jpg"},
        },
        "body": {"text": "Olá tudo bem? Confira este link: https://exemplo.com"},
        "action": {
            "buttons": [
                {"type": "reply", "reply": {"id": "sim_button", "title": "Sim"}},
                {"type": "reply", "reply": {"id": "nao_button", "title": "Não"}},
            ]
        },
    },
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.status_code)
print(response.json())
