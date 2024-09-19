import requests


def send_whats(nome: str, mensagem: str, telefone: str):
    try:
        url = f"https://api.whatsapp.com/send?phone={telefone}&text=Olá, %20{nome}%20. Obrigado por entrar em contato, deixe sua mensagem e retornaremos você."
        response = requests.get(url)
        print(f"{response.status_code} - {response.reason}")

    except Exception as e:
        print(e)


send_whats("Renan", "Teste 2", "556791758876")
