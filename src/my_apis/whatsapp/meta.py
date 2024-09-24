import requests
import json
from fastapi import HTTPException

# from verify_bd import MySqlConnector

TOKEN_ACESS = "EAAFPzmpZAYyEBO31VvvGlzRJZB5pi34FbxSEOYPrawoPBijoCmp0DETDn0poUMcyilr00jyJj4Y7FineGY9nNKQEmdH6tuQwkOHyNZC9c9MDvEJg2dZBbZBJEvneTXxZCJNGZCblaWQ9UrZBYtMr3C6Loo3pDR9reZCKfiZCZAaNxQZBi1cKFOl9zfZBlge5E44eept9EAyZArwrtG6rZC5U8eHqIfPZCV3VzBIZD"


def sugestao_db(nome, mensagem, telefone):
    # MySQL = MySqlConnector()
    try:
        # Enviar mensagem pelo WhatsApp
        mensagem = f"Olá, {nome}. Obrigado por entrar em contato, deixe sua mensagem e retornaremos você."
        resultado = enviar_mensagem_whatsapp(telefone, mensagem)

        # Salvar no banco de dados
        # cnx, cur = MySQL._cnx, MySQL._cur
        # insert = "INSERT INTO tbl_pessoa_sugestao (nome, email, telefone) VALUES (%s, %s, %s)"
        # cur.execute(insert, (nome, email, telefone))
        # cnx.commit()

        return {"message": "Sugestão enviada com sucesso e dados salvos no banco!"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar sugestão: {str(e)}"
        )
    finally:
        # MySQL.close_connection()
        ...


def enviar_mensagem_whatsapp(
    numero_telefone, mensagem, APP_ID="369222942810913"
):
    url = f"https://graph.facebook.com/v20.0/{APP_ID}/messages"

    headers = {
        "Authorization": f"Bearer {APP_ID}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "to": numero_telefone,
        "type": "text",
        "text": {"body": mensagem},
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return {"message": "Mensagem enviada com sucesso!"}
    else:
        raise Exception(f"Erro ao enviar mensagem: {response.text}")


# Uso da função
try:
    resultado = sugestao_db("Renan", "Renan@email.com", "5519998722472")
    print(resultado)
except HTTPException as e:
    print(f"Ocorreu um erro: {e.detail}")
