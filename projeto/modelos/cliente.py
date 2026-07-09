from dataclasses import dataclass

@dataclass
class Cliente:
    """
    Representa uma linha da planilha de clientes.
    Todos os campos são strings: o uso final é preencher campos de formulário como texto.
    """

    email_solicitante: str
    montante_emprestimo: str
    termo_emprestimo: str
    renda_anual_atual: str
    idade: str
