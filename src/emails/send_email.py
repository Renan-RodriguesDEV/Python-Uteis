import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv

# carrega as variáveis de ambiente do arquivo .env
load_dotenv()
usuario = os.getenv("EMAIL_USER")
senha = os.getenv("EMAIL_PASSWORD")
porta = int(os.getenv("EMAIL_PORT", "587"))
servidor = os.getenv("EMAIL_SERVER")


def enviar_email(
    assunto: str, corpo: str, destinatarios: list[str] = [], anexos: list[Path] = []
):
    # cria instancia do EmailMessage
    msg = EmailMessage()
    # define o assunto do email
    msg["Subject"] = assunto
    # define o remetente do email
    msg["To"] = ", ".join(destinatarios)
    # define o corpo do email
    msg.set_content(corpo)
    # adiciona os anexos ao email
    for anexo in anexos:
        anexo_data = anexo.read_bytes()
        maintype = "application"
        subtype = "octet-stream"
        msg.add_attachment(
            anexo_data, maintype=maintype, subtype=subtype, filename=anexo.name
        )


def build_envio(msg: EmailMessage, remetente: str, senha: str):
    # conecta ao servidor SMTP do Gmail
    with smtplib.SMTP(servidor, porta) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(remetente, senha)
        smtp.send_message(msg)
