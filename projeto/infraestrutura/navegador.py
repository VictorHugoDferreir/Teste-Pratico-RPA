from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from configuracao.configuracoes import Configuracoes


class Navegador:
    
    def abrir(self) -> WebDriver:
        print("Abrindo navegador...")

        opcoes = self._criar_opcoes()

        servico = Service(ChromeDriverManager().install())

        self._driver = webdriver.Chrome(
            service=servico,
            options=opcoes
        )

        print("Navegador aberto.")

        return self._driver
        
    def _criar_opcoes(self) -> Options:
        opcoes = Options()

        if Configuracoes.MODO_HEADLESS:
            opcoes.add_argument("--headless=new")

        opcoes.add_argument("--start-maximized")
        opcoes.add_argument("--disable-notifications")

        opcoes.add_experimental_option(
            "prefs",
            {
                "download.default_directory": str(
                    Configuracoes.DIRETORIO_DOWNLOADS
                ),
                "download.prompt_for_download": False,
            },
        )

        return opcoes