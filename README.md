# Empório da Música — Assistente Virtual com IA

Assistente virtual de atendimento ao cliente desenvolvido em Python para o desafio técnico de AI Engineer da Artefact. O projeto utiliza o Gemini para interpretar mensagens em português e acionar ferramentas que consultam o catálogo de produtos, as políticas da loja e registram reclamações de clientes.

## Tecnologias

- **Python 3.15** — linguagem principal do projeto.
- **Google Gen AI SDK** — integração com o Gemini e Function Calling nativo.
- **Pandas** — leitura e processamento dos arquivos CSV.
- **Pydantic** — validação e estruturação de dados.
- **python-dotenv** — carregamento das variáveis de ambiente.
- **Pytest** — testes automatizados.
- **Black** — formatação do código Python.

## Funcionalidades implementadas

- Interface de conversação via terminal.
- Histórico de mensagens mantido em memória durante a execução do agente.
- Busca de produtos ativos no catálogo, com paginação de até cinco resultados por página.
- Continuação de pesquisas de produtos com preservação dos termos da consulta e controle de páginas disponíveis.
- Consulta de informações de preço, estoque e promoções disponíveis nos dados.
- Aplicação das regras de preço promocional e desconto para pagamento via PIX, conforme os dados retornados pelas ferramentas.
- Busca textual nas políticas da loja, com normalização de acentos e pontuação e classificação por relevância.
- Registro local de reclamações, com validação dos campos obrigatórios e geração de protocolo.
- Armazenamento dos registros de reclamações em arquivo JSON.
- Function Calling para permitir que o Gemini solicite consultas e operações às ferramentas implementadas.
- Tratamento de erros da API Gemini, incluindo problemas de conexão e limites de cota.
- Testes automatizados para os componentes do projeto.

O registro de reclamações não representa uma aprovação de troca, devolução ou reembolso e não envia notificações externas à equipe responsável.

## Arquitetura

```text
emporio-agent/
├── data/
│   ├── csv/
│   │   ├── categories.csv
│   │   ├── customers.csv
│   │   ├── orders.csv
│   │   ├── order_items.csv
│   │   ├── products.csv
│   │   └── promotions.csv
│   ├── policies/
│   │   ├── políticas_da_loja.pdf
│   │   └── policies.json
│   └── complaints.json          # Gerado durante a execução
├── src/
│   ├── agent/
│   │   ├── agent.py
│   │   ├── conversation_history.py
│   │   └── prompts.py
│   ├── core/
│   │   └── config.py
│   ├── integrations/
│   │   └── gemini_client.py
│   ├── repositories/
│   │   ├── csv_repository.py
│   │   └── policy_repository.py
│   ├── schemas/
│   │   ├── complaint_schema.py
│   │   ├── policy_schema.py
│   │   └── product_schema.py
│   ├── services/
│   │   ├── policy_service.py
│   │   └── product_service.py
│   ├── session/
│   │   ├── conversation_manager.py
│   │   └── session_manager.py
│   ├── tools/
│   │   ├── complaint_tools.py
│   │   ├── policy_tools.py
│   │   └── product_tools.py
│   ├── validators/
│   │   └── data_validator.py
│   └── main.py
├── tests/
├── examples/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### Responsabilidades principais

- `agent/`: coordenação das interações com o modelo, instruções do sistema e histórico.
- `integrations/`: configuração do cliente da API Gemini.
- `repositories/`: acesso aos arquivos CSV e aos dados de políticas.
- `services/`: regras de busca e processamento de produtos e políticas.
- `schemas/`: declarações das ferramentas disponibilizadas ao modelo.
- `tools/`: validação dos argumentos e execução das operações solicitadas pelo agente.
- `session/`: estruturas para gerenciamento de sessões.
- `validators/`: validação estrutural dos conjuntos de dados.
- `tests/`: testes automatizados.
- `examples/`: exemplos de conversas que demonstram o comportamento do agente.

O arquivo `data/complaints.json` é criado automaticamente quando necessário. Ele armazena os registros de reclamações e não deve ser publicado, pois pode conter dados pessoais fornecidos durante a execução.

## Pré-requisitos

- Python 3.15 ou uma versão compatível com as dependências fixadas.
- Uma chave de API do Google Gemini.
- Acesso à internet para as chamadas ao modelo.

## Instalação e execução

### 1. Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd emporio-agent
```

Substitua `<URL_DO_REPOSITORIO>` pela URL do repositório publicado.

### 2. Crie e ative um ambiente virtual

No Windows PowerShell:

```powershell
py -3.15 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se a versão especificada não estiver instalada, utilize uma versão compatível com as dependências do projeto.

### 3. Instale as dependências

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

Edite o arquivo `.env` e informe sua chave de API e o modelo Gemini configurado no projeto:

```dotenv
GEMINI_API_KEY=sua_chave_de_api
GEMINI_MODEL=gemini-3.6-flash
```

O nome do modelo acima deve corresponder a um modelo disponível para a API e compatível com a integração utilizada.

Mantenha o arquivo `.env` privado. Não publique a chave de API no repositório.

### 5. Execute o agente

Na raiz do projeto:

```powershell
python -m src.main
```

Digite uma mensagem no terminal para iniciar a conversa. Para encerrar, digite:

```text
sair
```

O funcionamento depende da disponibilidade da API Gemini e da cota associada à chave utilizada.

## Testes

Execute a suíte de testes:

```powershell
python -m pytest
```

Para obter um resumo detalhado:

```powershell
python -m pytest -v
```

Os testes automatizados verificam componentes do sistema e utilizam mocks nos cenários em que não é necessário realizar chamadas reais à API.

A paginação de produtos é coberta por testes que verificam a recuperação dos resultados por página, a ausência de sobreposição entre páginas consecutivas, o comportamento quando não existem mais resultados e a validação dos parâmetros de consulta.

Os testes das ferramentas de reclamações verificam o registro dos dados, a preservação de registros existentes e o tratamento de argumentos inválidos e arquivos com conteúdo inválido.

## Formatação

O código Python foi formatado com Black.

Para verificar a formatação:

```powershell
python -m black --check src tests
```

Para formatar novamente:

```powershell
python -m black src tests
```

Caso o Black não esteja instalado no ambiente, instale-o antes de executar esses comandos:

```powershell
python -m pip install black
```

## Decisões técnicas

### Gemini com Function Calling nativo

Foi utilizado o SDK oficial `google-genai`, com declarações de ferramentas para que o modelo possa solicitar consultas ao catálogo de produtos, às políticas da loja e o registro de reclamações.

Essa abordagem mantém a integração próxima à API oficial e evita introduzir frameworks adicionais de orquestração em um projeto de escopo delimitado.

### Separação de responsabilidades

O código separa agente, integração externa, repositórios, serviços, ferramentas e esquemas. Isso facilita os testes e permite evoluir as regras de negócio sem concentrar toda a implementação em um único