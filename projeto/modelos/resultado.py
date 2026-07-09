from dataclasses import dataclass

@dataclass
class Resultado:
    """
    Representa o retorno obtido no Sistema B para um cliente consultado.

    email_solicitante: identifica de qual cliente este resultado é.
    mensagem: texto retornado pelo Sistema B após a consulta.
    sucesso: indica se a consulta foi concluída sem erro de automação.
    """

    email_solicitante: str
    mensagem: str
    sucesso: bool = False

    def __str__(self) -> str:
        status = "OK" if self.sucesso else "ERRO"
        return f"[{status}] {self.email_solicitante} — {self.mensagem}"
