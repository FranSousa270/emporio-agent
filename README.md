# Empório da Música — Assistente Virtual com IA

Assistente virtual de atendimento ao cliente desenvolvido em Python para o desafio técnico de AI Engineer da Artefact. O projeto utiliza o Gemini para interpretar mensagens em português e acionar ferramentas que consultam o catálogo de produtos e as políticas da loja.

## Tecnologias

- **Python 3.15**
- **Google Gen AI SDK** — integração com o Gemini e Function Calling nativo.
- **Pandas** — leitura e processamento dos arquivos CSV.
- **Pydantic** — validação e estruturação de dados.
- **python-dotenv** — carregamento das variáveis de ambiente.
- **Pytest** — testes automatizados.
- **Black** — formatação do código Python.

## Funcionalidades implementadas

- Interface de conversação via terminal.
- Histórico de mensagens mantido em memória durante a execução do agente.
- Busca de produtos ativos no catálogo, com limite de cinco resultados.
- Consulta de informações de preço, estoque e promoções disponíveis nos dados.
- Aplicação das regras de preço promocional e desconto para pagamento via PIX, conforme os dados retornados pelas ferramentas.
- Busca textual nas políticas da loja, com normalização de acentos e pontuação e classificação por relevância.
- Function Calling para permitir que o Gemini solicite consultas às ferramentas implementadas.
- Tratamento de erros da API Gemini, incluindo limites de cota.
- Testes automatizados para componentes do projeto.

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
│   └── policies/
│       ├── políticas_da_loja.pdf
│       └── policies.json
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
│   │   ├── policy_schema.py
│   │   └── product_schema.py
│   ├── services/
│   │   ├── policy_service.py
│   │   └── product_service.py
│   ├── session/
│   │   ├── conversation_manager.py
│   │   └── session_manager.py
│   ├── tools/
│   │   ├── policy_tools.py
│   │   └── product_tools.py
│   ├── validators/
│   │   └── data_validator.py
│   └── main.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

**Responsabilidades principais:**

- `agent/`: coordenação das interações com o modelo, instruções do sistema e histórico.
- `integrations/`: configuração do cliente da API Gemini.
- `repositories/`: acesso aos arquivos CSV e aos dados de políticas.
- `services/`: regras de busca e processamento de produtos e políticas.
- `schemas/`: declarações das ferramentas disponibilizadas ao modelo.
- `tools/`: validação dos argumentos e execução das consultas solicitadas pelo agente.
- `session/`: estruturas para gerenciamento de sessões.
- `validators/`: validação estrutural dos conjuntos de dados.
- `tests/`: testes automatizados.

## Pré-requisitos

- Python 3.15, ou uma versão compatível com as dependências fixadas.
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

Edite o `.env` e informe sua chave de API:

```dotenv
GEMINI_API_KEY=sua_chave_de_api
GEMINI_MODEL=gemini-3.8-flash
```

Mantenha a chave privada e não a publique no repositório.

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

Foi utilizado o SDK oficial `google-genai`, com declarações de ferramentas para que o modelo possa solicitar consultas ao catálogo de produtos e às políticas da loja.

Essa abordagem mantém a integração próxima à API oficial e evita introduzir frameworks adicionais de orquestração em um projeto de escopo delimitado.

### Separação de responsabilidades

O código separa agente, integração externa, repositórios, serviços, ferramentas e esquemas. Isso facilita os testes e permite evoluir as regras de negócio sem concentrar toda a implementação em um único arquivo.

### Busca determinística

A busca por produtos e políticas é realizada em Python. A normalização textual e a pontuação de relevância tornam os resultados menos dependentes da interpretação do modelo.

As regras de preço e desconto são calculadas pela aplicação, utilizando `Decimal` para evitar imprecisões comuns em operações monetárias com ponto flutuante.

### Histórico em memória

O histórico de interação é mantido em memória durante a execução do agente. Não há persistência de conversas em banco de dados.

## Limitações conhecidas

- O catálogo utilizado é composto por arquivos CSV fornecidos para o desafio; não existe integração com um sistema comercial em tempo real.
- A busca textual é baseada em correspondência lexical e pontuação de relevância, não em busca semântica por embeddings.
- O histórico de conversa não é persistido após o encerramento do processo.
- Embora existam componentes de gerenciamento de sessões no projeto, a interface de terminal atual instancia o agente diretamente.
- As ferramentas atualmente integradas ao agente permitem consultar produtos e políticas. Fluxos completos de autenticação de clientes, consulta de pedidos, cancelamento e devolução ainda não estão conectados à interface de conversação.
- A disponibilidade e o funcionamento das chamadas ao modelo dependem dos limites e das condições da API Gemini.

## Melhorias futuras

- Integrar os fluxos de autenticação e consulta de pedidos.
- Conectar o gerenciamento de sessões à interface de conversação.
- Adicionar persistência de sessões e histórico, com controles adequados de privacidade.
- Expandir os testes de integração e os testes dos fluxos completos do agente.
- Evoluir a busca por políticas com recuperação híbrida, combinando relevância lexical e busca semântica.
- Adicionar observabilidade para chamadas de ferramentas, latência e erros, sem registrar dados pessoais desnecessários.

## Uso de ferramentas de inteligência artificial

O Gemini é utilizado como modelo de linguagem do próprio sistema desenvolvido. Ferramentas de assistência ao desenvolvimento, incluindo o ChatGPT, também foram utilizadas durante a implementação para apoiar atividades de programação, depuração, testes e documentação.

As decisões de arquitetura, a integração das ferramentas e a validação do comportamento do projeto foram conduzidas durante o desenvolvimento, com testes automatizados para verificar os componentes implementados.
