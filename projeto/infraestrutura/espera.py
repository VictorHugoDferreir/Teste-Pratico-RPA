from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


TEMPO_ESPERA = 20


def esperar_pagina(navegador):

    WebDriverWait(
        navegador,
        TEMPO_ESPERA
    ).until(
        lambda driver:
        driver.execute_script(
            "return document.readyState"
        ) == "complete"
    )


def esperar_elemento(
    navegador,
    seletor,
):

    return WebDriverWait(
        navegador,
        TEMPO_ESPERA
    ).until(
        EC.presence_of_element_located(seletor)
    )