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

## Decisões técnicas e arquitetura

Esta seção apresenta as principais decisões técnicas do projeto, as alternativas consideradas e os motivos pelos quais a implementação foi estruturada dessa forma.

### 1. Abordagem de desenvolvimento do agente

O agente foi desenvolvido em Python utilizando o SDK oficial `google-genai` e o mecanismo nativo de Function Calling do Gemini.

A escolha permite utilizar um modelo de linguagem para interpretar as mensagens dos clientes e decidir quando consultar informações externas ao contexto da conversa, mantendo a execução das operações sob controle da aplicação.

Em vez de concentrar toda a lógica em um único prompt, o sistema disponibiliza ferramentas específicas para consultar produtos, pesquisar políticas e registrar reclamações. O modelo pode solicitar essas operações, mas a execução é realizada pelo código Python.

Essa abordagem separa duas responsabilidades:

- **Interpretação e comunicação:** o modelo compreende a solicitação, identifica a ferramenta pertinente e formula a resposta em linguagem natural.
- **Execução e validação:** a aplicação valida argumentos, executa as operações e devolve os resultados ao modelo.

O Function Calling não garante, por si só, que o modelo sempre escolha a ferramenta correta. Por isso, as instruções do sistema definem quando as ferramentas devem ser utilizadas e quais limitações precisam ser respeitadas.

#### Alternativas consideradas

Frameworks de orquestração de agentes, como LangChain e LangGraph, poderiam oferecer abstrações adicionais para composição de ferramentas, fluxos com estado e orquestração de tarefas.

Entretanto, para o escopo deste desafio, a integração direta com o SDK oficial reduz dependências e torna explícito o fluxo de execução, facilitando a compreensão, a depuração e os testes.

### 2. Escolha do modelo de linguagem

O Gemini foi escolhido como provedor do modelo de linguagem, utilizando um modelo configurável por variável de ambiente.

A configuração separada do código permite alterar o modelo sem modificar diretamente a implementação do agente. A integração também concentra a criação do cliente e a configuração de chamadas em um módulo próprio.

Como a aplicação depende de um serviço externo, seu funcionamento está sujeito à disponibilidade, à latência, aos limites de requisições e à cota da API.

Por esse motivo, o agente contempla tratamento específico para falhas de conexão e erros da API, incluindo situações relacionadas à cota. Esses tratamentos permitem retornar mensagens controladas nos cenários previstos, sem transformar falhas de infraestrutura em respostas de sucesso.

A escolha do provedor não elimina a necessidade de testes: o comportamento do modelo pode variar, mesmo quando as instruções e as ferramentas permanecem iguais.

### 3. Separação entre LLM e regras determinísticas

Uma decisão central do projeto foi não delegar ao modelo de linguagem todas as operações do atendimento.

O LLM é responsável pela interpretação da solicitação e pela construção da resposta. Já as operações que exigem consulta a dados, validação ou aplicação de regras são executadas por componentes determinísticos em Python.

Essa separação é especialmente importante para:

- Consultas ao catálogo e verificação de disponibilidade.
- Aplicação das regras de preço e promoções.
- Cálculos monetários e descontos para pagamento via PIX.
- Validação dos argumentos recebidos pelas ferramentas.
- Registro persistente de reclamações e geração de protocolos.
- Recuperação de informações relacionadas às políticas da loja.

Dessa forma, o modelo não precisa inventar valores ou executar cálculos comerciais por conta própria. Ele recebe os resultados produzidos pela aplicação e os utiliza para construir uma resposta adequada ao cliente.

Essa abordagem reduz a dependência da geração probabilística em operações que exigem resultados verificáveis, embora não elimine completamente o risco de respostas incorretas do modelo.

### 4. Organização em camadas

A aplicação foi organizada para separar responsabilidades e reduzir o acoplamento entre o modelo de linguagem, as regras de negócio e as fontes de dados.

As principais camadas são:

- **Agent:** coordena as interações com o Gemini, mantém o contexto da conversa e processa as chamadas de ferramentas.
- **Integrations:** encapsula a configuração do cliente externo utilizado para acessar o modelo.
- **Schemas:** declara os contratos e os argumentos aceitos pelas ferramentas disponibilizadas ao modelo.
- **Tools:** valida os argumentos e encaminha as solicitações para os componentes responsáveis pela execução.
- **Services:** concentra as regras de busca e processamento dos dados.
- **Repositories:** fornece acesso às fontes de dados locais, como os arquivos CSV.
- **Validators:** verifica a integridade estrutural dos conjuntos de dados.
- **Tests:** verifica o comportamento dos componentes e o tratamento de cenários inválidos.

Essa organização permite testar regras de negócio sem depender de chamadas reais ao LLM em todos os cenários. Também facilita substituir uma fonte de dados ou modificar uma regra sem concentrar todas as alterações no agente.

### 5. Recuperação e tratamento dos dados

Os dados fornecidos para o desafio são utilizados como fonte de informação para o atendimento. O catálogo é consultado por meio de componentes Python, em vez de ser tratado exclusivamente como contexto textual enviado ao modelo.

A busca de produtos utiliza normalização textual, incluindo tratamento de acentos e diferenças de capitalização, além de correspondência entre os termos da consulta e os campos disponíveis.

Os resultados são classificados por relevância e limitados para evitar respostas excessivamente extensas. A busca considera apenas produtos ativos e mantém informações de estoque para distinguir a existência de um produto de sua disponibilidade para compra.

A implementação também trata casos em que a consulta não encontra resultados, evitando apresentar produtos que não correspondam aos critérios da busca.

#### Por que não utilizar busca vetorial?

Uma alternativa seria utilizar embeddings e um banco de dados vetorial para recuperar produtos e documentos por similaridade semântica.

Essa abordagem poderia melhorar consultas formuladas com sinônimos ou descrições conceitualmente semelhantes, mas acrescentaria dependências e uma etapa de geração e armazenamento de embeddings.

Para o escopo atual, a busca lexical foi considerada suficiente como solução inicial, pois os dados são locais e a aplicação pode controlar diretamente os critérios de correspondência.

A principal limitação é que correspondência textual não equivale a compreensão semântica. Consultas com vocabulário muito diferente do catálogo podem não recuperar os resultados esperados.

### 6. Paginação e controle dos resultados

A busca de produtos utiliza paginação para limitar a quantidade de itens apresentados em cada interação.

Cada consulta retorna no máximo cinco produtos por página e informa se existem resultados adicionais. A ferramenta consulta até seis resultados para identificar a existência de uma próxima página, utilizando o item excedente apenas como indicador de continuidade.

Quando o cliente solicita mais opções, o agente deve manter os termos da consulta anterior e avançar sequencialmente, respeitando o indicador de disponibilidade da próxima página.

Essa decisão reduz o volume de informações apresentado por interação e permite explorar catálogos maiores sem retornar todos os produtos de uma só vez.

O controle da paginação permanece na aplicação, enquanto o modelo interpreta a solicitação do cliente e decide quando solicitar a continuação dos resultados.

### 7. Regras comerciais e precisão monetária

As regras comerciais são aplicadas no código Python, utilizando os dados recuperados pelas ferramentas.

A aplicação distingue produtos com promoções ativas de produtos sem promoção, evitando combinar descontos quando as regras da loja não permitem essa composição.

Para operações monetárias, é utilizado `Decimal`, em vez de depender exclusivamente de números de ponto flutuante binário. Essa escolha ajuda a evitar imprecisões em cálculos financeiros e permite aplicar regras explícitas de arredondamento.

A implementação procura manter os valores calculados separados da formulação textual da resposta, reduzindo a possibilidade de o modelo alterar preços ou descontos durante a explicação ao cliente.

### 8. Recuperação de políticas e limites de decisão

As políticas da loja são recuperadas por uma ferramenta dedicada, com busca textual e classificação por relevância.

Essa abordagem permite que o agente consulte informações pertinentes à solicitação, em vez de depender apenas do conhecimento geral do modelo ou de reproduzir integralmente todos os documentos em cada interação.

As políticas encontradas orientam a resposta, mas o agente não possui autonomia para aprovar operações que dependam de avaliação humana, como determinadas solicitações de troca, devolução ou reembolso.

Quando uma operação não está implementada ou não pode ser confirmada pela aplicação, o agente deve comunicar essa limitação sem afirmar que uma ação externa foi realizada.

A recuperação textual possui limitações: a relevância depende dos termos presentes na consulta e nos documentos. Uma evolução possível seria combinar busca lexical com recuperação semântica e regras determinísticas para as políticas mais críticas.

### 9. Registro de reclamações

O registro de reclamações foi implementado como uma ferramenta específica, separada da lógica de conversação.

Antes de registrar uma reclamação, o agente deve coletar os campos obrigatórios e utilizar informações que o cliente já tenha fornecido, evitando solicitar repetidamente os mesmos dados.

A ferramenta valida os argumentos, gera um protocolo e armazena o registro em um arquivo JSON local, com status inicial de análise pendente.

O protocolo só deve ser apresentado como confirmado quando a operação de gravação retorna sucesso. Se a gravação falhar, a aplicação retorna um resultado de erro, evitando confirmar um registro inexistente.

O armazenamento local foi escolhido pela simplicidade e adequação ao escopo do desafio. Ele não equivale a um sistema de atendimento compartilhado: não envia notificações externas, não encaminha automaticamente a reclamação a uma equipe e não aprova solicitações comerciais.

Como os registros contêm dados pessoais, o arquivo gerado deve permanecer fora do controle de versão.

Em uma aplicação de produção, essa funcionalidade exigiria persistência adequada, controle de acesso, políticas de retenção, auditoria e integração com o sistema responsável pelo atendimento.

### 10. Histórico de conversação e gerenciamento de sessões

O histórico da conversa é mantido em memória durante a execução do agente, permitindo que mensagens anteriores sejam utilizadas como contexto nas interações seguintes.

Essa escolha evita a necessidade de configurar um banco de dados exclusivamente para persistência de conversas em um protótipo de escopo limitado.

A principal limitação é que o histórico não é preservado após o encerramento do processo. Além disso, embora existam componentes destinados ao gerenciamento de sessões, a interface de terminal atual instancia o agente diretamente, sem integrar completamente esse gerenciamento ao fluxo principal.

Uma evolução futura seria persistir sessões e mensagens em uma fonte de dados apropriada, com isolamento entre clientes, controle de acesso e regras de retenção. O histórico conversacional não deve ser tratado como fonte de verdade para informações comerciais que precisam ser recuperadas dos dados oficiais.

### 11. Controle de execução e tratamento de falhas

O agente processa as respostas do modelo em um fluxo de interação que pode incluir chamadas de ferramentas e o retorno dos respectivos resultados ao Gemini.

O número de rodadas de execução de ferramentas é limitado para evitar ciclos excessivos de chamadas em uma mesma interação. No estado atual, o limite é de cinco rodadas por resposta.

As ferramentas também validam os argumentos recebidos e retornam resultados estruturados, incluindo indicadores de sucesso ou falha quando aplicável.

A integração externa possui tratamento específico para erros de conexão e erros da API previstos na implementação. Isso é importante porque uma falha do provedor não deve ser confundida com um resultado válido de consulta ou de registro.

Esses mecanismos reduzem o risco de execuções descontroladas e de confirmações indevidas, mas não substituem monitoramento, métricas operacionais ou testes em condições reais de indisponibilidade.

### 12. Estratégia de testes

O projeto utiliza Pytest para verificar o comportamento dos principais componentes, incluindo repositórios, validadores, serviços, ferramentas, integração com o Gemini e agente.

Os testes unitários isolam dependências externas com mocks quando a chamada real à API não é necessária. Isso permite validar entradas inválidas, resultados esperados, erros e fluxos de execução sem depender constantemente da disponibilidade ou da cota do provedor.

A suíte também contempla cenários relacionados à paginação de produtos e ao registro local de reclamações.

A integração real com um modelo de linguagem possui características diferentes de um teste unitário, pois as respostas podem variar e a API depende de condições externas. Por isso, os testes automatizados devem ser complementados por testes manuais de conversação, especialmente nos cenários que envolvem escolha de ferramentas e formulação de respostas finais.

### 13. Limitações e evolução da solução

A implementação prioriza uma arquitetura simples, testável e compatível com o escopo do desafio. Algumas funcionalidades permanecem limitadas ao protótipo, incluindo a ausência de persistência de conversas, a inexistência de integração externa para reclamações e a falta de conexão completa dos fluxos de autenticação e operações de pedidos à interface de terminal.

Com mais tempo, as principais evoluções seriam:

- Persistência de sessões e histórico com isolamento e controles de privacidade.
- Integração das ferramentas de atendimento com sistemas externos reais.
- Recuperação híbrida de políticas, combinando busca lexical e semântica.
- Testes de integração mais abrangentes para os fluxos completos do agente.
- Observabilidade das chamadas ao modelo e das ferramentas, com métricas de latência e falhas.
- Avaliação sistemática da qualidade das respostas e da seleção de ferramentas, utilizando um conjunto de conversas representativas.

As evoluções propostas são separadas das funcionalidades já implementadas: o objetivo é explicitar o caminho de evolução sem atribuir à solução atual capacidades que ela ainda não possui.
