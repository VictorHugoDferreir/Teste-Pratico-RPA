# Teste Prático RPA

Automação RPA desenvolvida em Python que simula um fluxo de análise de pedidos de empréstimo:

1. Acessa uma pasta do **Google Drive** e baixa a planilha `PedidosEmprestimo.xlsx`;
2. Lê os dados dos clientes contidos na planilha (`openpyxl`);
3. Acessa o sistema **UiBank** (ambiente de prática da UiPath) e, para cada cliente, preenche o formulário de solicitação de empréstimo;
4. Captura e exibe no console o resultado retornado para cada solicitação.

## Tecnologias utilizadas

- Python 3
- [Selenium](https://pypi.org/project/selenium/) — automação do navegador
- [webdriver-manager](https://pypi.org/project/webdriver-manager/) — gerencia o ChromeDriver automaticamente
- [openpyxl](https://pypi.org/project/openpyxl/) — leitura da planilha `.xlsx`
- [PyAutoGUI](https://pypi.org/project/PyAutoGUI/) — interação com o menu de contexto nativo do sistema operacional (usado no download do arquivo no Google Drive)

## Estrutura do projeto

```
projeto/
├── automacao/
│   └── automacao_clientes.py   # Orquestra o fluxo completo da automação
├── configuracao/
│   └── configuracoes.py        # Constantes: URLs, diretórios, tempos de espera, cabeçalhos
├── dowloads/                   # Pasta de destino da planilha
├── infraestrutura/
│   ├── navegador.py            # Configuração e ciclo de vida do navegador (Selenium)
    └── espera.py               # Configuração de espera para renderização de página e elementos HTML
├── modelos/
│   └── cliente.py              # Dataclass Cliente
├── servicos/
│   ├── servico_download.py     # Download da planilha no Google Drive
│   ├── leitor_planilha.py      # Leitura e validação da planilha
│   └── servico_consulta.py     # Preenchimento do formulário e captura do resultado no UiBank
├── main.py                     # Ponto de entrada da aplicação
└── requirements.txt
```

## Arquitetura da solução

O projeto segue uma separação de responsabilidades em camadas:

- **`automacao/`** — Contém `AutomacaoClientes`, a classe orquestradora do fluxo. Ela **não implementa regras de negócio**, apenas decide a ordem em que os serviços são chamados (abrir navegador → baixar planilha → ler planilha → acessar sistema → consultar cada cliente → fechar navegador).
- **`configuracao/`** — Centraliza constantes do projeto (URLs, diretórios, cabeçalhos obrigatórios, tempos de espera), evitando valores "mágicos" espalhados pelo código.
- **`infraestrutura/`** — Responsável por recursos de baixo nível compartilhados, como a criação e o encerramento do navegador (`Navegador`).
- **`modelos/`** — Define as estruturas de dados do domínio, como a dataclass `Cliente`, usada para representar cada linha da planilha.
- **`servicos/`** — Implementa as regras de negócio específicas: baixar a planilha do Google Drive, ler e validar seu conteúdo, e preencher/consultar o formulário no sistema UiBank.
- **`main.py`** — Ponto de entrada; apenas instancia e chama `AutomacaoClientes().executar()`.

Em resumo, `AutomacaoClientes` funciona como um **maestro**: ela orquestra a ordem das etapas, mas delega a execução de cada responsabilidade específica para as classes/funções de `infraestrutura` e `servicos`. Essa separação facilita testes, manutenção e reuso de cada parte isoladamente.

### Fluxo da automação

```
main.py
    │
    ▼
AutomacaoClientes.executar()
    │
    ▼
Abrir navegador
    │
    ▼
Baixar planilha
    │
    ▼
Ler planilha
    │
    ▼
Criar lista de Clientes
    │
    ▼
Para cada cliente
    │
    ├── Preencher formulário
    ├── Enviar solicitação
    └── Capturar resultado
    │
    ▼
Fechar navegador
```

## Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/) instalado
- [Google Chrome](https://www.google.com/chrome/) instalado (o `webdriver-manager` baixa o ChromeDriver compatível automaticamente)
- Acesso de rede para abrir o Google Drive e o site UiBank
- Sistema operacional com interface gráfica (o `pyautogui` simula teclas do sistema, portanto **não funciona em ambientes headless/servidor sem tela**)

## Instalação

Clone o repositório:

```bash
git clone https://github.com/VictorHugoDferreir/Teste-Pratico-RPA.git
cd Teste-Pratico-RPA/projeto
```

Crie e ative um ambiente virtual (recomendado):

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

## Execução

Dentro da pasta `projeto`, com o ambiente virtual ativado, execute:

```bash
python main.py
```

O que acontece ao rodar:

1. O Chrome é aberto automaticamente (maximizado, com notificações desativadas e a pasta `projeto/downloads` configurada como destino padrão de downloads).
2. O navegador acessa a pasta do Google Drive configurada e realiza o download da planilha `PedidosEmprestimo.xlsx`, salvando-a na pasta **`projeto/downloads`** (o script fica em espera ativa até o arquivo aparecer nesse diretório).
3. A planilha é lida e validada — os seguintes cabeçalhos são obrigatórios:
   - `Email do Solicitante`
   - `Montante do Empréstimo`
   - `Termo do Empréstimo`
   - `Renda Anual Atual( Antes dos Impostos)`
   - `Idade`
4. O navegador acessa o sistema UiBank e, para cada cliente da planilha, preenche o formulário e envia a solicitação.
5. O resultado de cada consulta é impresso no console.
6. Ao final (ou em caso de erro), o navegador é fechado automaticamente.

> **Observação:** como o download depende de um clique com o botão direito seguido de navegação por teclado (via `pyautogui`), não mova o mouse nem use o teclado enquanto a automação estiver em execução, para não interferir na etapa de download.

## Configurações

Os principais parâmetros do projeto ficam centralizados em `configuracao/configuracoes.py`, entre eles:

| Parâmetro | Descrição |
|---|---|
| `URL_PLANILHA_GOOGLE_DRIVE` | Link da pasta do Google Drive onde está a planilha |
| `URL_SISTEMA_UIBANK` | URL do sistema de simulação de empréstimos |
| `NOME_ARQUIVO_PLANILHA` | Nome esperado do arquivo baixado |
| `DIRETORIO_DOWNLOADS` | Pasta local `projeto/downloads`, definida como diretório padrão de download do Chrome e onde a planilha `PedidosEmprestimo.xlsx` é salva |
| `CABECALHOS_OBRIGATORIOS` | Colunas exigidas na planilha |
| `TEMPO_CARREGAMENTO`, `TEMPO_DOWNLOAD`, `TEMPO_VERIFICACAO_DOWNLOAD` | Tempos de espera (em segundos) usados durante a automação |

Caso a URL da planilha, do sistema ou o nome do arquivo mudem, basta ajustar esse arquivo.
