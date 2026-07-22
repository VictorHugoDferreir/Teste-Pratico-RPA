import time
import pyautogui

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


from configuracao import configuracoes
from modelos.cliente import Cliente
from infraestrutura.espera import esperar_elemento, esperar_pagina

#localiza os elementos da página web usando seletores do Selenium (pelo ID).
CAMPO_EMAIL = (By.ID, "email")
CAMPO_MONTANTE = (By.ID, "amount")
CAMPO_TERMO = (By.ID, "term")
CAMPO_RENDA = (By.ID, "income")
CAMPO_IDADE = (By.ID, "age")
BOTAO_CARREGAR = (By.ID, "submitButton")
BOTAO_VOLTAR = (By.ID, "applyForNewLoanButton")

def acessar_sistema(navegador: WebDriver) -> None:
    print("[INFO] Acessando Sistema UiBank...")

    navegador.get(configuracoes.URL_SISTEMA_UIBANK)

    esperar_pagina(navegador)

def consultar_cliente(
    navegador: WebDriver,
    cliente: Cliente,
) -> str:

    print(f"[INFO] Consultando cliente: {cliente.email_solicitante}")

    _preencher_formulario(navegador, cliente) #realiza o preenchimento do formulário com os dados do cliente

    _clicar_carregar(navegador) #realiza o clique no botão de carregar para enviar o formulário

    return _obter_resultado(navegador) 

def _preencher_formulario(
    navegador: WebDriver,
    cliente: Cliente,
) -> None:

    navegador.find_element(*CAMPO_EMAIL).send_keys(
        cliente.email_solicitante
    ) #localiza e preenche o campo email

    navegador.find_element(*CAMPO_MONTANTE).send_keys(
        str(cliente.montante_emprestimo)
    )    #localiza e preenche o campo montante de empréstimo

    navegador.find_element(*CAMPO_TERMO).click()    #encontra o campo de termo, clica nele
    selecao = Select(navegador.find_element(*CAMPO_TERMO)) #localiza o campo de termo e cria um objeto Select para interagir com ele
    selecao.select_by_value(cliente.termo_emprestimo) #seleciona a opção correspondente ao valor do termo de empréstimo do cliente

    navegador.find_element(*CAMPO_RENDA).send_keys(
        str(cliente.renda_anual_atual)
    )#preenche o campo de renda anual atual com o valor do cliente

    navegador.find_element(*CAMPO_IDADE).send_keys(
        str(cliente.idade)
    )              #preenche o campo de idade com o valor do cliente
    

def _clicar_carregar(
    navegador: WebDriver,
) -> None:
    esperar_elemento(
        navegador,
        BOTAO_CARREGAR
    ) #espera o botão de carregar estar presente na página antes de clicar nele

    botao = navegador.find_element(*BOTAO_CARREGAR) #encontra o botão de carregar e clica nele
    botao.send_keys(Keys.ENTER)

def _obter_resultado(navegador: WebDriver) -> str:

    # 1. Espera a página de resultado carregar aguardando o surgimento do botão de voltar
    botao_voltar = esperar_elemento(
        navegador,
        BOTAO_VOLTAR
    )

    # 2. Com a página de resultado já carregada, localiza o container e os textos
    resultado = navegador.find_element(
        By.CLASS_NAME,
        "text-center"
    ) #localiza o elemento que contém o resultado da consulta, usando a classe CSS "text-center"

    elementos = resultado.find_elements(
        By.XPATH,
        ".//h1 | .//h4 | .//h5"
    ) #localiza os elementos dentro do resultado que são cabeçalhos (h1, h4, h5) usando uma expressão XPath. 

    mensagem = "\n".join(
        elemento.text
        for elemento in elementos
        if elemento.text.strip()
    )

    # 3. Clica no botão para voltar ao formulário
    botao_voltar.send_keys(Keys.ENTER)

    return mensagem