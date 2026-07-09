from pathlib import Path

import openpyxl

from modelos.cliente import Cliente
from configuracao.configuracoes import CABECALHOS_OBRIGATORIOS


def ler_planilha(caminho_arquivo: Path) -> list[Cliente]:
    print("Lendo planilha...")

    planilha = openpyxl.load_workbook(caminho_arquivo, data_only=True)
    aba = planilha.active

    cabecalhos = {
        nome: indice
        for indice, nome in enumerate(
            next(aba.iter_rows(max_row=1, values_only=True))
        )
        if nome
    }

    for coluna in CABECALHOS_OBRIGATORIOS:
        if coluna not in cabecalhos:
            raise ValueError(
                f"Cabeçalho '{coluna}' não encontrado na planilha."
            )

    clientes = []

    for linha in aba.iter_rows(min_row=2, values_only=True):

        if not any(linha):
            continue

        cliente = Cliente(
            email_solicitante=str(
                linha[cabecalhos["Email do Solicitante"]] or ""
            ).strip(),

            montante_emprestimo=str(
                linha[cabecalhos["Montante do Empréstimo"]] or ""
            ).strip(),

            termo_emprestimo=str(
                linha[cabecalhos["Termo do Empréstimo"]] or ""
            ).strip(),

            renda_anual_atual=str(
                linha[cabecalhos["Renda Anual Atual( Antes dos Impostos)"]] or ""
            ).strip(),

            idade=str(
                linha[cabecalhos["Idade"]] or ""
            ).strip(),
        )

        clientes.append(cliente)

    print(f"{len(clientes)} cliente(s) encontrado(s).")

    return clientes