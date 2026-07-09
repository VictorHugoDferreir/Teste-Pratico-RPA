import time
from pathlib import Path

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from configuracao.configuracoes import Configuracoes


class ServicoDownload:

    SELETOR_ARQUIVO_PLANILHA = (
        By.XPATH,
        "//div[contains(@aria-label, '.xlsx') or contains(@data-tooltip, '.xlsx')]",
    )

    SELETOR_OPCAO_DOWNLOAD_MENU = (
        By.XPATH,
        "//li[@role='menuitem'][.//span[contains(text(), 'ownload')]]",
    )

    def __init__(self, navegador: WebDriver) -> None:
        self._navegador = navegador

    def baixar_planilha(self) -> Path:
        print("Acessando Google Drive...")

        self._navegador.get(Configuracoes.URL_PLANILHA_GOOGLE_DRIVE)

        time.sleep(3)

        arquivo = self._navegador.find_element(*self.SELETOR_ARQUIVO_PLANILHA)

        ActionChains(self._navegador).context_click(arquivo).perform()

        time.sleep(1)
        opcao_download = self._navegador.find_element(
            
    self.SELETOR_OPCAO_DOWNLOAD_MENU
        )

        opcao_download.click()

        print("Baixando planilha...")

        caminho = (
            Configuracoes.DIRETORIO_DOWNLOADS
            / Configuracoes.NOME_ARQUIVO_PLANILHA
        )

        while not caminho.exists():
            time.sleep(1)

        print("Download concluído.")

        return caminho