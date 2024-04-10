import time
import pyautogui as pg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = webdriver.ChromeService()
options = webdriver.ChromeOptions()
gc = webdriver.Chrome(service=service, options=options)


def abrir_site():
    gc.get('https://www.youtube.com/')
    print('tamanho')

    while len(gc.find_elements(By.ID, 'search')) <= 3:
        time.sleep(1)
    gc.find_element(By.XPATH, '//*[@id="search"]').send_keys('python')
    gc.quit()


if __name__ == "__main__":
    abrir_site()
