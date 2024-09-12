import random
import string
from urllib.parse import urlencode
import requests
from flask import Flask, request, redirect
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Configurações do aplicativo
APP_ID = os.getenv("APP_ID")
CLIENT_KEY = os.getenv("CLIENT_KEY")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "https://211c6ef3-bdf3-4dfa-afff-a9390e064508-00-2h0pvhweacp7n.worf.replit.dev/callback"  # Registre este URI no portal do TikTok
AUTHORIZATION_URL = "https://www.tiktok.com/v2/auth/authorize/"
TOKEN_URL = "https://open-api.tiktok.com/oauth/access_token/"


def gerar_estado_csrf():
    """
    Gera um estado CSRF aleatório para prevenir ataques CSRF.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=30))


@app.route("/login")
def login():
    """
    Redireciona o usuário para a página de autorização do TikTok.
    """
    csrf_state = gerar_estado_csrf()

    params = {
        "client_key": CLIENT_KEY,
        "response_type": "code",
        "scope": "user.info.basic",
        "redirect_uri": REDIRECT_URI,
        "state": csrf_state,
    }

    url = f"{AUTHORIZATION_URL}?{urlencode(params)}"

    # Redireciona o usuário para o TikTok para concessão de permissão
    return redirect(url)


@app.route("/callback")
def callback():
    """
    Captura o código de autorização e troca por um token de acesso.
    """
    authorization_code = request.args.get("code")
    state = request.args.get("state")

    if not authorization_code:
        return "Erro: código de autorização não foi fornecido", 400

    # Troca o authorization code por um access token
    data = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": authorization_code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(TOKEN_URL, data=data)

    # Verifica se a resposta foi bem-sucedida
    response.raise_for_status()

    token_data = response.json().get("data", {})
    access_token = token_data.get("access_token")

    if not access_token:
        return "Erro: Token de acesso não encontrado na resposta", 400

    return {"access_token": access_token}


if __name__ == "__main__":
    app.run(debug=True)
