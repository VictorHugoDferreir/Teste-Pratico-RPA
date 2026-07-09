from infraestrutura.navegador import Navegador
from infraestrutura.logger import obter_logger
from servicos.servico_download import ServicoDownload
from servicos.leitor_planilha import LeitorPlanilha
from servicos.servico_consulta import ServicoConsulta

logger = obter_logger(__name__)

class AutomacaoClientes:
    #Orquestra o fluxo da automação (completa)

    def executar(self) -> None:
        #Ponto de entrada da automação. Coordena as etapas do fluxo.
        navegador = Navegador()
        try:
            sessao = navegador.abrir()

            caminho_planilha = ServicoDownload(sessao).baixar_planilha()
            clientes = LeitorPlanilha().ler(caminho_planilha)

            consulta = ServicoConsulta(sessao)
            consulta.acessar_sistema()

            for cliente in clientes:
                resultado = consulta.consultar(cliente)
                logger.info(resultado)

        finally:
            navegador.fechar()
