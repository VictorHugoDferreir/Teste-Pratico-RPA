from infraestrutura.logger import configurar_logging
from automacao.automacao_clientes import AutomacaoClientes


if __name__ == "__main__":
    
    configurar_logging()
    AutomacaoClientes().executar()
