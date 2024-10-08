import datetime
import requests


def send_whats(nome: str, mensagem: str, telefone: str):
    try:
        url = f"https://api.whatsapp.com/send?phone={telefone}&text=Olá, %20{nome}%20. Obrigado por entrar em contato, deixe sua mensagem e retornaremos você."
        response = requests.get(url)
        print(f"{response.status_code} - {response.reason}")

    except Exception as e:
        print(e)


send_whats("Renan", "Teste 2", "5519998722472")

acumulador_alertas = {
    1: {"qtde": 0, "timestemp": datetime.datetime.now()},
    2: {"qtde": 0, "timestemp": datetime.datetime.now()},
}

if __name__ == "__main__":
    acumulador_alertas[1]["qtde"] += 1
    acumulador_alertas[1]["timestemp"] += datetime.timedelta(hours=1)
    print(acumulador_alertas[1]["qtde"])
    print(acumulador_alertas[1]["timestemp"])
