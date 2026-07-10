import time
import pyautogui
from pathlib import Path

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from configuracao import configuracoes


SELETOR_ARQUIVO_PLANILHA = (
    By.XPATH,
    "//div[contains(@aria-label, '.xlsx') or contains(@aria-label, '.xls')]",
) #procurando o arquivo da planilha no google drive, que pode ter extensão .xlsx ou .xls


def baixar_planilha(navegador: WebDriver) -> Path:
    
    print("[INFO] Acessando Google Drive...")

    navegador.get(configuracoes.URL_PLANILHA_GOOGLE_DRIVE) #busca a planilha no google drive
    time.sleep(configuracoes.TEMPO_CARREGAMENTO)

    print("[INFO] Localizando planilha...")

    arquivo = navegador.find_element(*SELETOR_ARQUIVO_PLANILHA) #procura o arquivo da planilha no google drive

    print("[INFO] Abrindo menu de contexto...")
    ActionChains(navegador).context_click(arquivo).perform() #clica com o botão direito do mouse no arquivo da planilha para abrir o menu de contexto

    time.sleep(1)

    pyautogui.press("down") #procura botao de donwload
    pyautogui.press("down")
    pyautogui.press("enter") #da enter no botao de download

    caminho = (
        configuracoes.DIRETORIO_DOWNLOADS / configuracoes.NOME_ARQUIVO_PLANILHA
    )

    print("[INFO] Aguardando download...")

    while not caminho.exists():
        time.sleep(configuracoes.TEMPO_VERIFICACAO_DOWNLOAD) #enquanto nao achar, ele espera e verifica novamente
        print("[INFO] Download nao identificado, verificando novamente...")

    print("[INFO] Download concluido!")

    return caminho