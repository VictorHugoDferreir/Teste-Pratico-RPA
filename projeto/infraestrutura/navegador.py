from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from configuracao import configuracoes


class Navegador:
    
    def abrir(self) -> WebDriver:
        print("[INFO] Abrindo navegador...")

        opcoes = self._criar_opcoes()

        servico = Service(ChromeDriverManager().install())

        self._driver = webdriver.Chrome(
            service=servico,
            options=opcoes
        )

        print("[INFO] Navegador aberto.")

        return self._driver
            
    #configura as opções do navegador, como maximizar a janela, desativar notificações e definir o diretório de download padrão.
    def _criar_opcoes(self) -> Options:
        opcoes = Options()

        opcoes.add_argument("--start-maximized")
        opcoes.add_argument("--disable-notifications")

        opcoes.add_experimental_option(
            "prefs",
            {
                "download.default_directory": str(
                    configuracoes.DIRETORIO_DOWNLOADS
                ),
                "download.prompt_for_download": False,
            },
        )

        return opcoes

    def fechar(self) -> None:
        self._driver.quit()
        print("[INFO] Navegador fechado.")