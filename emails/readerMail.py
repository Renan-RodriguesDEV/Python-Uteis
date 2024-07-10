
from creds_my import user,password
from imap_tools import MailBox, AND
def get_mail() -> dict:
    # estrutura with para abrir e fechar email, e configs do email como caixa de msg, senha, usuario e servidor
    with MailBox('imap.hostinger.com', 993).login(username=user, password=password, initial_folder='INBOX') as mailbox:
        # Busca tds os emails da pasta INBOX, caso esteja em spam add (.junk) dps de INBOX, ordenado por data mais recente
        msgs = mailbox.fetch(
            AND(from_='dvrs@droone.com.br'), sort='DATE', reverse=True)
        

        # Acesse o e-mail mais recente
        if msgs:  # verifica se encontrou e-mails
            for msg in msgs:
                sender = msg.to

                subject = msg.subject

                body=msg.text

                # formatando a data
                data = msg.date.strftime('%Y-%m-%d %H:%M:%S')

                if len(msg.attachments) > 0:
                    filename = []
                    for anexo in msg.attachments:
                            # nome da imagem
                            filename.append(anexo.filename)  
                            # transforma em bytes pra dowload 
                            bytes_img = anexo.payload
                            
                            # cria o arquivo da imagem
                            with open(f'anexos\\anexo.filename','wb') as anx:
                                anx.write(bytes_img)

                email = {'sender': sender[0], 
                         'subject': subject,
                         'body': body, 
                         'date': data,
                         'filename':filename}

                return email
        else:
            print("Nenhum email encontrado na pasta.")
            return None