import json
import time
from playwright.sync_api import sync_playwright


def salvar_dados_sessao(contexto, arquivo):
    # Salva cookies
    cookies = contexto.cookies()
    # Salva local storage
    local_storage = []
    for pagina in contexto.pages:
        storage = pagina.evaluate("() => JSON.stringify(localStorage)")
        local_storage.append({"url": pagina.url, "storage": storage})

    # Salva cookies e local storage em um arquivo
    with open(arquivo, "w") as f:
        json.dump({"cookies": cookies, "local_storage": local_storage}, f)


def carregar_dados_sessao(contexto, arquivo):
    # Carrega cookies e local storage de um arquivo
    with open(arquivo, "r") as f:
        dados = json.load(f)

        # Define os cookies no contexto
        contexto.add_cookies(dados["cookies"])

        # Define o local storage em cada página
        for pagina in contexto.pages:
            for item in dados["local_storage"]:
                if pagina.url.startswith(item["url"]):
                    pagina.evaluate(
                        f"() => {{ const data = JSON.parse('{item['storage']}'); for (const key in data) {{ localStorage.setItem(key, data[key]); }} }}"
                    )


if __name__ == "__main__":
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False)
        contexto = navegador.new_context()

        # Realiza login ou outras ações que criam uma sessão
        pagina = contexto.new_page()
        pagina.goto("https://www.tiktok.com/")
        time.sleep(45)

        # Salva os dados da sessão em um arquivo
        salvar_dados_sessao(contexto, "./sessao.json")

        navegador.close()

    # with sync_playwright() as p:
    #     navegador = p.chromium.launch(headless=False)
    #     contexto = navegador.new_context()

    #     # Carrega os dados da sessão
    #     carregar_dados_sessao(contexto, 'sessao.json')

    #     # Abre uma nova página com os dados da sessão carregados
    #     pagina = contexto.new_page()
    #     pagina.goto('https://www.tiktok.com/')

    #     navegador.close()
