from time import time

from selenium.webdriver.remote.webdriver import WebDriver

from modelos.cliente import Cliente
from modelos.resultado import Resultado
from configuracao.configuracoes import (
    URL_SISTEMA_UIBANK,
    TEMPO_CARREGAMENTO,
)

def acessar_sistema(navegador: WebDriver) -> None:

    print("Acessando Sistema UiBank...")

    navegador.get(URL_SISTEMA_UIBANK)    
    time.sleep(TEMPO_CARREGAMENTO)