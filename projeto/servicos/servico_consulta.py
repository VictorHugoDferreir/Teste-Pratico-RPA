from selenium.webdriver.remote.webdriver import WebDriver

from modelos.cliente import Cliente
from modelos.resultado import Resultado

class ServicoConsulta:
    
    #Responsável por toda a interação com o Sistema B via Selenium.

    def __init__(self, navegador: WebDriver) -> None:
        self._navegador = navegador 
    