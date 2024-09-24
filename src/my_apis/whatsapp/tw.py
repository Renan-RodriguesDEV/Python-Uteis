from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="src/configs/.env")

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
my_number = os.getenv("my_number")
print("codigo do sid:", account_sid, "token de auth:", auth_token)
client = Client(account_sid, auth_token)


def send_message():
    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body="Essa mensagem de Droone foi um alarme falso ou verdadeiro?\nAgradeçemos seu feedback!!!",
        to=f"whatsapp:+55{my_number}",
    )
    print("Mensagem enviada.")
    print(message.sid)


send_message()
