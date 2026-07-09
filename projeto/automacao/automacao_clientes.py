from infraestrutura.navegador import Navegador
from infraestrutura.logger import obter_logger
from servicos.servico_download import ServicoDownload
from servicos.leitor_planilha import LeitorPlanilha
from servicos.servico_consulta import ServicoConsulta

logger = obter_logger(__name__)


class AutomacaoClientes:
    """
    Orquestra o fluxo completo da automação.

    Não contém código de Selenium, XPath, HTML ou planilha.
    Apenas coordena os serviços em ordem.
    """

    def executar(self) -> None:
        """Ponto de entrada da automação. Coordena todas as etapas do fluxo."""
        navegador = Navegador()
        try:
            driver = navegador.abrir()

            caminho_planilha = ServicoDownload(driver).baixar_planilha()
            clientes = LeitorPlanilha().ler(caminho_planilha)

            consulta = ServicoConsulta(driver)
            consulta.acessar_sistema()

            for cliente in clientes:
                resultado = consulta.consultar(cliente)
                logger.info(resultado)

        finally:
            navegador.fechar()
