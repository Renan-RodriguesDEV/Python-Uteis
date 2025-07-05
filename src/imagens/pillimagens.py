# %%
# !pip install pillow

import time

from PIL import Image
from pyautogui import press
from selenium import webdriver

# %%
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Abrir a imagem
imagem = Image.open(
    r"C:\Users\renan\OneDrive\Documentos\Python Scripts\imagens\batman.jpg"
)

# Converter para escala de cinza'
imagem_gray = imagem.convert("L")

# Salvar a imagem em escala de cinza
imagem_gray.save("imagem_gray.png")

# Fechar a imagem original
imagem.close()


# %%

# Configuração do WebDriver do Microsoft Edge
driver = webdriver.Edge(EdgeChromiumDriverManager().install())

#  Abrindo uma página da web
driver.get("https://web.whatsapp.com/")


# Exemplo de uso: Obter o título da página
print(driver.title)

driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys("renanrodrigues7110")
driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
driver.find_element(
    By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p'
).click()
driver.find_element(
    By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p'
).send_keys("renan filho")
press("enter")
driver.find_element(
    By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
).send_keys("Ola")
time.sleep(10)
# Fechar o navegador
driver.quit()


# %%
