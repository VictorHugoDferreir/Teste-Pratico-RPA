from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from configuracao.configuracoes import Configuracoes
from infraestrutura.logger import obter_logger

logger = obter_logger(__name__)


class Navegador:
    """
    Gerencia o ciclo de vida do ChromeDriver.

    Responsável por abrir, configurar e fechar o navegador.
    Nenhuma regra de negócio deve residir aqui.
    """

    def __init__(self) -> None:
        self._driver: WebDriver | None = None

    def abrir(self) -> WebDriver:
        """Inicializa o ChromeDriver com as opções configuradas e retorna o WebDriver."""
        logger.info("Iniciando o navegador...")
        opcoes = self._configurar_opcoes()
        servico = Service(ChromeDriverManager().install())
        self._driver = webdriver.Chrome(service=servico, options=opcoes)
        logger.info("Navegador aberto com sucesso.")
        return self._driver

    def fechar(self) -> None:
        """Encerra o navegador de forma segura, mesmo que não tenha sido aberto."""
        if self._driver is not None:
            self._driver.quit()
            self._driver = None
            logger.info("Navegador encerrado.")

    @property
    def driver(self) -> WebDriver:
        """Retorna o driver ativo. Lança erro se o navegador não foi aberto."""
        if self._driver is None:
            raise RuntimeError("Navegador não foi inicializado. Chame abrir() primeiro.")
        return self._driver

    # ---------------------------------------------------------------------------
    # Configuração interna
    # ---------------------------------------------------------------------------

    def _configurar_opcoes(self) -> Options:
        """Monta as opções do Chrome, incluindo diretório de download e modo headless."""
        opcoes = Options()

        if Configuracoes.MODO_HEADLESS:
            opcoes.add_argument("--headless=new")

        opcoes.add_argument("--start-maximized")
        opcoes.add_argument("--disable-notifications")
        opcoes.add_argument("--no-sandbox")
        opcoes.add_argument("--disable-dev-shm-usage")

        opcoes.add_experimental_option("prefs", self._preferencias_download())
        opcoes.add_experimental_option("excludeSwitches", ["enable-logging"])

        return opcoes

    def _preferencias_download(self) -> dict:
        """Retorna as preferências do Chrome para download automático sem prompts."""
        return {
            "download.default_directory": str(Configuracoes.DIRETORIO_DOWNLOADS),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
