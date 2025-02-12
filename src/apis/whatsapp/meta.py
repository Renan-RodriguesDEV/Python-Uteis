import os, sys
import requests
import json
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
from src.configs.creds_my import TOKEN_API

load_dotenv()

# Configurações
token = TOKEN_API
phone_number_id = "385364571321840"
recipient = "5519998722472"  # Número do destinatário no formato internacional (sem +)
template_name = "relatorio_class"  # Nome do template aprovado
language_code = "pt_BR"  # Idioma do template

url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


# Função para enviar mensagem de texto simples
def send_message_text(recipient, body):
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {"body": body},
    }
    return payload


# Função para enviar mensagem com template
def send_template_message(
    recipient, template_name, language_code, header_params, body_params
):
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code},
            "components": [],
        },
    }

    if header_params:
        payload["template"]["components"].append(
            {"type": "header", "parameters": header_params}
        )

    if body_params:
        payload["template"]["components"].append(
            {"type": "body", "parameters": body_params}
        )

    return payload


# Parâmetros dinâmicos para o template
variables_header = [
    {"type": "text", "text": "30/01/2025"}  # Parâmetro do header ({{1}})
]

variables_body = [
    {"type": "text", "text": "compra"},  # Parâmetro do body ({{2}})
    {"type": "text", "text": "https://www.vjbots.com.br"},  # Parâmetro do body ({{3}})
]

# Criar payloads
payload_template = send_template_message(
    recipient, template_name, language_code, variables_header, variables_body
)
payload_text = send_message_text(recipient, "Olá, tudo bem?")

# Lista para armazenar respostas
responses = []

# Enviar mensagens
try:
    responses.append(
        requests.post(url, headers=headers, data=json.dumps(payload_template))
    )
    responses.append(requests.post(url, headers=headers, data=json.dumps(payload_text)))
except Exception as e:
    print(f"Erro ao enviar mensagem: {e}")

# Verificar resposta
for response in responses:
    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
        print(f"Mensagem : {response.json()}")
    else:
        print(f"Erro {response.status_code}: {response.text}")
