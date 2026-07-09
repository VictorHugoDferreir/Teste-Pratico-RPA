from pathlib import Path

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from configuracao.configuracoes import Configuracoes
from infraestrutura.espera import Espera
from infraestrutura.logger import obter_logger

logger = obter_logger(__name__)


class ServicoDownload:
    """
    Responsável por acessar o Google Drive e baixar a planilha.

    Aguarda o download terminar antes de retornar o caminho do arquivo.
    Nenhuma regra de negócio além do gerenciamento do download.

    --- Regra de uso das bibliotecas ---
    Selenium: uso prioritário para toda interação com o navegador
              (navegação, localização de elementos, cliques, etc.).
    PyAutoGUI: uso complementar e restrito a ações que o Selenium
               não consegue realizar de forma confiável, como janelas
               nativas do sistema operacional ou diálogos do SO.

    Todo código Selenium e PyAutoGUI fica centralizado aqui.
    O restante do sistema não deve importar essas bibliotecas.

    --- Sobre os localizadores do Google Drive ---
    O Google Drive utiliza uma interface dinâmica que pode variar.
    Os seletores abaixo foram definidos para a interface atual (2024+).
    Caso o Drive atualize sua UI, ajustar apenas as constantes abaixo.
    """

    # ---------------------------------------------------------------------------
    # Localizadores — Google Drive (pasta em modo lista ou grade)
    # Estratégia: localizar o item de arquivo por aria-label contendo ".xlsx",
    # pois é o atributo mais estável da interface do Drive.
    # ---------------------------------------------------------------------------
    _SELETOR_ARQUIVO_PLANILHA = (
        By.XPATH,
        "//div[contains(@aria-label, '.xlsx') or contains(@data-tooltip, '.xlsx')]",
    )
    _SELETOR_OPCAO_DOWNLOAD_MENU = (
        By.XPATH,
        "//li[@role='menuitem'][.//span[contains(text(), 'ownload')]]",
    )

    def __init__(self, navegador: WebDriver) -> None:
        self._navegador = navegador
        self._espera = Espera(navegador)

    def baixar_planilha(self) -> Path:
        """
        Navega até a pasta no Google Drive, localiza a planilha,
        aciona o download e aguarda sua conclusão.

        Retorna o caminho absoluto do arquivo baixado.
        """
        logger.info("Acessando pasta do Google Drive...")
        self._navegador.get(Configuracoes.URL_PLANILHA_GOOGLE_DRIVE)

        self._acionar_download_arquivo()

        caminho_destino = Configuracoes.DIRETORIO_DOWNLOADS / Configuracoes.NOME_ARQUIVO_PLANILHA
        logger.info(f"Aguardando conclusão do download: {caminho_destino.name}")
        return self._espera.por_arquivo_baixado(caminho_destino)

    # ---------------------------------------------------------------------------
    # Fluxo interno de download
    # ---------------------------------------------------------------------------

    def _acionar_download_arquivo(self) -> None:
        """Localiza o arquivo, abre o menu de contexto e clica em Download."""
        arquivo = self._localizar_arquivo_planilha()
        self._abrir_menu_contexto(arquivo)
        self._clicar_opcao_download()

    def _localizar_arquivo_planilha(self):
        """Aguarda e retorna o elemento do arquivo .xlsx na listagem do Drive."""
        logger.info("Localizando planilha na pasta do Drive...")
        return self._espera.por_elemento_visivel(*self._SELETOR_ARQUIVO_PLANILHA)

    def _abrir_menu_contexto(self, elemento_arquivo) -> None:
        """Abre o menu de contexto (clique direito) sobre o arquivo."""
        ActionChains(self._navegador).context_click(elemento_arquivo).perform()

    def _clicar_opcao_download(self) -> None:
        """Localiza e clica na opção de download no menu de contexto."""
        opcao = self._espera.por_elemento_clicavel(*self._SELETOR_OPCAO_DOWNLOAD_MENU)
        opcao.click()
        logger.info("Download iniciado.")
