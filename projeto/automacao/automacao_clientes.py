from infraestrutura.navegador import Navegador

from servicos.servico_download import baixar_planilha
from servicos.leitor_planilha import ler_planilha
from servicos.servico_consulta import acessar_sistema, consultar_cliente


class AutomacaoClientes:

    def executar(self) -> None:

        navegador = Navegador()

        try:
            sessao = navegador.abrir()

            caminho_planilha = baixar_planilha(sessao)

            clientes = ler_planilha(caminho_planilha)

            acessar_sistema(sessao)

            for cliente in clientes:
                #chama a consulta ao sistema Uibank
                resultado = consultar_cliente(
                    sessao,
                    cliente
                )

                print(f"[INFO] Resultado para {cliente.email_solicitante}:\n")
                print(resultado)
                print("-" * 40)

        finally:
            print("[INFO] Fechando navegador...")
            navegador.fechar()