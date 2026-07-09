from pathlib import Path


class Configuracoes:
    """Centraliza todas as constantes e parâmetros de configuração do projeto."""

    #Diretorios 
    DIRETORIO_RAIZ: Path = Path(__file__).parent.parent
    DIRETORIO_DOWNLOADS: Path = DIRETORIO_RAIZ / "downloads"

    #Google Drive
    URL_PLANILHA_GOOGLE_DRIVE: str = "https://drive.google.com/drive/folders/1I1byidvRDJk4T_Sfl7QmdZjPEnfHLQi5"
    URL_SISTEMA_UIBANK: str = "https://uibank.uipath.com/loans/apply"

    NOME_ARQUIVO_PLANILHA: str = "planilha.xlsx"

    # Site final
    URL_SISTEMA_B: str = "TODO: URL_DO_SISTEMA_B"

    # Configurações do navegador
    CABECALHOS_OBRIGATORIOS: list[str] = [
        "Email do Solicitante",
        "Montante do Empréstimo",
        "Termo do Empréstimo",
        "Renda Anual Atual( Antes dos Impostos)",
        "Idade",
    ]

    # Configurações de tempo (em segundos)
    TEMPO_CARREGAMENTO = 2
    TEMPO_DOWNLOAD = 5
    TEMPO_VERIFICACAO_DOWNLOAD = 1