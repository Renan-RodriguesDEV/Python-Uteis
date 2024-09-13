# importando a bliblioteca
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # criando um navegador (por padçao é headless)
    navegador = p.chromium.launch(headless=False)
    # estanciando uma pagina web
    pagina = navegador.new_page()
    # escolhendo qual sera a pagina
    pagina.goto(url="https://ead.eduvaleavare.com.br/login/index.php")
    # localiza um elemento na tela
    pagina.locator('xpath=//*[@id="username"]')
    # clicka no elemento
    pagina.click('xpath=//*[@id="username"]')
    # preenche o campo do elemento
    pagina.fill('xpath=//*[@id="username"]', "060207")
    pagina.locator('xpath=//*[@id="password"]')
    pagina.click('xpath=//*[@id="password"]')
    pagina.fill('xpath=//*[@id="password"]', "20022005")
    pagina.click('xpath=//*[@id="loginbtn"]')
    time.sleep(15)
