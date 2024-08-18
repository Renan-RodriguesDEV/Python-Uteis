import datetime as dt
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.configs.creds_my import user, senha, enviar_para


def createEmailMsg(from_msg, to_msg, password, body, attachment_path):
    msg = MIMEMultipart()

    msg['Subject'] = f'Relatorio semanal - Music Bot\
    {dt.date.today().strftime("%d/%m/%Y")}'

    msg['From'] = from_msg

    msg['To'] = to_msg

    msg.attach(MIMEText(body, 'HTML'),)

    arquivo = open(attachment_path, 'rb')
    att = MIMEBase('application', 'octet-stream')
    att.set_payload(arquivo.read())
    encoders.encode_base64(att)

    att.add_header('Content-Disposition',
                   f'attachment; filename=Acervo Biblioteca Virtual Pearson para ADS.pdf')
    arquivo.close()
    msg.attach(att)
    enviar(from_msg, to_msg, password, msg)

# portas (587 - 465) -> gmail

# with smtplib.SMTP('smtp.gmail.com', 465) as smtp:


def enviar(from_mail, to_mail, password, msg_mail):
    try:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(from_mail, password)
        smtp.sendmail(from_mail, to_mail, msg_mail.as_string())
        print('email enviado')
    except smtplib._SendErrs as e:
        raise f'{e}'
    finally:
        smtp.quit()


if __name__ == '__main__':
    from poo_with_python import Funcoes
    print(Funcoes.fat(5))
    password = senha
    usuario = user
    to_msg = enviar_para

    corpo = f'''
        <p>Bom dia {to_msg}, segue o anexao semanal do relatório do <b>Music Bot</b></p>
        <p>Atenciosamente,</p>
        <p>VJ Bots Equipe</p>
    '''
    file_cam = 'C:/Users/renan/OneDrive/Documentos/FACULDADE/PDFs/Acervo Biblioteca Virtual Pearson para ADS.pdf'
    createEmailMsg(usuario, to_msg, password, corpo, file_cam)
