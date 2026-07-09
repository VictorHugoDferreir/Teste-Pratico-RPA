import time
from pathlib import Path

import pyautogui
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from configuracao.configuracoes import (
    URL_PLANILHA_GOOGLE_DRIVE,
    DIRETORIO_DOWNLOADS,
    NOME_ARQUIVO_PLANILHA,
    TEMPO_CARREGAMENTO,
    TEMPO_VERIFICACAO_DOWNLOAD,
)


SELETOR_ARQUIVO_PLANILHA = (
    By.XPATH,
    "//div[contains(@aria-label, '.xlsx') or contains(@aria-label, '.xls')]",
)


def baixar_planilha(navegador: WebDriver) -> Path:
    
    print("Acessando Google Drive...")

    navegador.get(URL_PLANILHA_GOOGLE_DRIVE) #busca a planilha no google drive
    time.sleep(TEMPO_CARREGAMENTO)

    print("Localizando planilha...")

    arquivo = navegador.find_element(*SELETOR_ARQUIVO_PLANILHA) #encontra o arquivo da planilha

    ActionChains(navegador).move_to_element(arquivo).perform() #move o mouse para o elemento

    print("Abrindo menu de contexto...")

    pyautogui.click(button="right")

    print("Selecionando Download...")

    pyautogui.press("down")
    pyautogui.press("enter")

    caminho = (
        DIRETORIO_DOWNLOADS / NOME_ARQUIVO_PLANILHA
    )

    print("Aguardando download...")

    while not caminho.exists():
        time.sleep(TEMPO_VERIFICACAO_DOWNLOAD)

    print("Download concluído!")

    return caminho