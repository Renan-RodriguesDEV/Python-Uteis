import datetime as dt
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
import os

load_dotenv()
EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")

print(EMAIL,SENHA)

def createEmailMsg(to_msg, body, attachment_path=None):
    msg = MIMEMultipart()

    msg["Subject"] = (
        f'Relatorio semanal - Music Bot\
    {dt.date.today().strftime("%d/%m/%Y")}'
    )

    msg["From"] = EMAIL

    msg["To"] = to_msg

    msg.attach(
        MIMEText(body, "HTML"),
    )
    if attachment_path != None:
        arquivo = open(attachment_path, "rb")
        att = MIMEBase("application", "octet-stream")
        att.set_payload(arquivo.read())
        encoders.encode_base64(att)

        att.add_header(
            "Content-Disposition",
            f"attachment; filename=Acervo Biblioteca Virtual Pearson para ADS.pdf",
        )
        arquivo.close()
        msg.attach(att)

    enviar(to_msg, msg)


# portas (587 - 465) -> gmail

# with smtplib.SMTP('smtp.gmail.com', 465) as smtp:


def enviar(to_mail, msg_mail):
    try:
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL, SENHA)
        smtp.sendmail(EMAIL, to_mail, msg_mail.as_string())
        print("email enviado")
    except Exception as e:
        raise f"{e}"
    finally:
        smtp.quit()


if __name__ == "__main__":
    corpo = f"""
        <p>Bom dia {EMAIL}, segue o anexao semanal do relatório do <b>Music Bot</b></p>
        <p>Atenciosamente,</p>
        <p>VJ Bots Equipe</p>
    """
    file_cam = "C:/Users/renan/OneDrive/Documentos/FACULDADE/PDFs/Acervo Biblioteca Virtual Pearson para ADS.pdf"
    createEmailMsg(EMAIL, corpo)
