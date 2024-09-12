import random
import string
from urllib.parse import urlencode
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import requests

app = FastAPI()

# Configurações da API TikTok
CLIENT_KEY = "awaulqr7ovnp7sjj"
CLIENT_SECRET = "eBuQu3lGlDTaXp9bM6S6YCuASnAp0Skv"
REDIRECT_URI = "https://211c6ef3-bdf3-4dfa-afff-a9390e064508-00-2h0pvhweacp7n.worf.replit.dev/callback"
TOKEN_URL = "https://open-api.tiktok.com/oauth/access_token/"


def gerar_estado_csrf() -> str:
    """
    Gera um estado CSRF aleatório para prevenir ataques CSRF.
    :return: Estado CSRF gerado.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=30))


@app.get("/oauth")
def oauth():
    """
    Redireciona o usuário para o URL de autorização do TikTok.
    Gera um estado CSRF e o inclui nos parâmetros da solicitação.
    :return: Redirecionamento para a página de autorização do TikTok.
    """
    estado_csrf = gerar_estado_csrf()

    params = {
        "client_key": CLIENT_KEY,
        "scope": "user.info.basic",
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "state": estado_csrf,
    }

    url_autorizacao = f"https://www.tiktok.com/v2/auth/authorize/?{urlencode(params)}"
    return RedirectResponse(url_autorizacao)


@app.get("/callback")
def callback(request: Request):
    """
    Recebe o código de autorização do TikTok e troca-o por um token de acesso.
    :param request: Requisição contendo o código e estado.
    :return: Token de acesso obtido.
    """
    codigo = request.query_params.get("code")
    estado = request.query_params.get("state")

    # Verificar o estado CSRF aqui (opcional, para maior segurança)

    dados_token = {
        "client_key": CLIENT_KEY,
        "client_secret": CLIENT_SECRET,
        "code": codigo,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }

    resposta = requests.post(TOKEN_URL, data=dados_token)

    # Verificar se a resposta é bem-sucedida e tratar erros
    resposta.raise_for_status()

    token_acesso = resposta.json().get("data", {}).get("access_token")

    if not token_acesso:
        print("erro token não encontrado")
        return {
            "erro": "Token de acesso não encontrado na resposta",
            "type": resposta.json(),
        }
    print(token_acesso)

    return {"access_token": token_acesso}
