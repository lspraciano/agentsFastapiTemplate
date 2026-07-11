# Agents FastAPI Template

Template de aplicação centrada em **agentes de IA** (LangChain + LangGraph), servida via **FastAPI** de forma **agnóstica ao transporte**. O núcleo de agentes (`nexus`) não conhece HTTP — hoje é exposto por REST, mas pode ganhar WebSocket, webhook, etc. sem tocar na lógica do agente.

## Arquitetura

Três camadas com responsabilidades bem separadas:

| Camada | Pasta | Responsabilidade |
|---|---|---|
| **nexus** | `app/nexus` | Núcleo de agentes: grafos, agentes, tools, middlewares, exceções de domínio. Não conhece transporte. |
| **entrypoints** | `app/entrypoints` | Adaptadores de transporte (hoje REST/FastAPI). Traduz o mundo externo para os contratos do `nexus`. |
| **infrastructure** | `app/infrastructure` | Preocupações técnicas: checkpointer (SQLite), logger, observabilidade (Langfuse). |

O contrato entre `entrypoints` e `nexus` é explícito: `NexusInput` (entrada) e `NexusOutput` (saída). O `GraphExecutor` é a fachada que roda o grafo e traduz esses contratos — sem saber que existe HTTP.

```
entrypoint (REST)  ──NexusInput──►  GraphExecutor  ──►  GraphV1  ──►  Agentes
                   ◄─NexusOutput──                 ◄──
```

## Stack

- **Python** >= 3.13
- **uv** (gerenciador de pacotes)
- **FastAPI** + **Uvicorn**
- **LangChain** / **LangGraph** (grafo de agentes, `create_agent`)
- **Dynaconf** (configuração por ambiente)
- **Langfuse** (observabilidade de LLM)
- **SQLite** via `langgraph-checkpoint-sqlite` (checkpointer, com fallback em memória)

## Pré-requisitos

- [uv](https://docs.astral.sh/uv/) instalado
- Python 3.13+
- Chave da OpenAI e (opcional) do Langfuse

## Configuração

As configurações ficam em `configuration/`:

- `settings.toml` — valores não-sensíveis, versionado.
- `.secrets.toml` — segredos, **não** versionado (gitignored).

Crie o `configuration/.secrets.toml`:

```toml
[default]
OPENAI_API_KEY = "sk-..."
LANGFUSE_SECRET_KEY = "sk-lf-..."
LANGFUSE_PUBLIC_KEY = "pk-lf-..."
```

### Ambientes

Selecionados via a variável `AGENTS_TEMPLATE_ENVIRONMENT`. Ambientes disponíveis: `development`, `sandbox`, `production`.

Variáveis de ambiente usam o prefixo `AGENTS_TEMPLATE_`. Ex.: para injetar a chave da OpenAI sem o `.secrets.toml`:

```bash
AGENTS_TEMPLATE_OPENAI_API_KEY=sk-...
```

## Rodando local (sem Docker)

```bash
uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API em `http://localhost:8000` · docs em `http://localhost:8000/docs`.

## Rodando com Docker

Há um Dockerfile multi-stage (`docker/api/Dockerfile.api`) e três composes, um por ambiente:

| Compose | Ambiente | Segredos | Reload |
|---|---|---|---|
| `docker-compose.dev.yaml` | `development` | via `.secrets.toml` (bind-mount) | sim |
| `docker-compose.sandbox.yaml` | `sandbox` | via env vars do orquestrador | não |
| `docker-compose.prod.yaml` | `production` | via env vars do orquestrador | não |

### Dev

```bash
docker compose -f docker-compose.dev.yaml up --build
```

O código é montado no container (bind-mount) e o `.secrets.toml` vai junto — hot-reload ativo.

### Sandbox / Prod

Rodam a imagem "limpa"; quem orquestra informa os segredos por variável de ambiente (com o prefixo `AGENTS_TEMPLATE_`):

```bash
export AGENTS_TEMPLATE_OPENAI_API_KEY=sk-...
export AGENTS_TEMPLATE_LANGFUSE_PUBLIC_KEY=pk-lf-...
export AGENTS_TEMPLATE_LANGFUSE_SECRET_KEY=sk-lf-...

docker compose -f docker-compose.prod.yaml up --build
```

## API

### `GET /health`

```json
{ "status": "ok" }
```

### `POST /v1/chat`

Request:

```json
{
  "user_message": "Quanto é 12 * 8 + 5?",
  "conversation_id": "abc-123"
}
```

Response (sucesso):

```json
{
  "conversation_id": "abc-123",
  "response": "12 * 8 + 5 = 101"
}
```

O `conversation_id` é usado como `thread_id` do checkpointer (memória da conversa) e como `session_id` no Langfuse (agrupamento de traces por conversa).

### Respostas de erro

Todos os erros seguem o formato padronizado via `HTTPException`:

```json
{
  "detail": {
    "error_code": "<código>",
    "message": "<descrição>"
  }
}
```

| Status | `error_code` | Situação |
|---|---|---|
| 502 | `graph_response_missing` | O agente terminou sem produzir resposta |
| 502 | `structured_response_retry_exceeded` | O LLM não produziu o formato esperado após N tentativas |
| 503 | `service_unavailable` | O executor não foi inicializado (falha no startup) |
| 500 | `nexus_error` | Erro de domínio não mapeado |
| 500 | `internal_error` | Erro inesperado fora do domínio |
| 422 | — | Corpo do request inválido (FastAPI/Pydantic) |

## Exceções de domínio

As exceções do `nexus` ficam em `app/nexus/exceptions/nexus_exceptions.py` e herdam de `NexusError`. A camada REST é responsável por traduzi-las em HTTP — o `nexus` não conhece status codes.

```
NexusError
├── GraphResponseMissingError
└── StructuredResponseRetryExceededError
```

Para adicionar uma nova exceção de domínio:

1. Crie a classe herdando `NexusError` em `nexus_exceptions.py` com um `code` único.
2. Levante-a no lugar apropriado dentro do `nexus`.
3. Registre um handler em `ExceptionHandlersRegister` (`app/entrypoints/rest/exception/exception_handlers.py`).

## Injeção de dependência

O `GraphExecutor` é injetado nos endpoints via `Depends()`, usando o alias `GraphExecutorDependence` de `app/entrypoints/rest/dependencies/graph_executor_dependence.py`.

```python
async def chat_(
    message: ChatRequestSchema,
    executor: GraphExecutorDependence,
) -> ChatResponseSchema:
    ...
```

Isso permite sobrescrever o executor em testes sem subir Langfuse, SQLite ou LLM real:

```python
app.dependency_overrides[graph_executor_dependence] = lambda: FakeExecutor()
```

## Observabilidade

Traces são enviados ao Langfuse via `CallbackHandler`, injetado no `GraphExecutor` pelo `lifespan`. Cada turno vira um trace; turnos da mesma conversa são agrupados por sessão (`conversation_id`).

## Logs

Logs estruturados em JSON (`app/infrastructure/logger`), incluindo os do uvicorn, com campos extras (ex.: `conversation_id`). Nível controlado por `LOG_LEVEL`.

## Estrutura

```
app/
├── main.py                          # entrypoint: configura logger e cria o app
├── nexus/                           # núcleo de agentes (agnóstico a transporte)
│   ├── contracts/                   # NexusInput / NexusOutput
│   ├── exceptions/                  # NexusError e subclasses (nexus_exceptions.py)
│   ├── executor/                    # GraphExecutor (fachada do grafo)
│   ├── graphs/                      # definição dos grafos e state
│   ├── agents/                      # BaseAgent + agentes concretos
│   ├── middlewares/                 # middlewares dos agentes
│   └── tools/                       # ferramentas
├── entrypoints/
│   └── rest/                        # FastAPI
│       ├── dependencies/            # providers injetados via Depends()
│       ├── exception/               # ExceptionHandlersRegister
│       ├── events/                  # lifespan (startup / shutdown)
│       ├── middleware/              # CORS e outros middlewares HTTP
│       ├── router/                  # rotas por versão
│       └── schemas/                 # schemas de request/response
└── infrastructure/
    ├── database/sqlite/             # checkpointer
    ├── logger/                      # logging JSON estruturado
    └── observability/langfuse/      # provider do Langfuse
configuration/                       # Dynaconf (settings.toml, .secrets.toml)
docker/api/Dockerfile.api            # imagem multi-stage (uv)
docker-compose.*.yaml                # dev / sandbox / prod
```

## Criando um novo agente

1. Crie o schema de saída herdando `BaseModel` com um campo `response: str`.
2. Crie o agente estendendo `BaseAgent` (implementando `_create_llm` e `_build_command`).
3. Adicione as tools necessárias em `app/nexus/tools`.
4. Registre o agente como nó no grafo (`app/nexus/graphs`).

Os middlewares obrigatórios (`ToolLoopGuardMiddleware` e `StructuredResponseRetryMiddleware`) já são injetados pelo `BaseAgent`.

### Execução e Ciclo de Vida do Agente

O `BaseAgent` oferece duas formas de execução:

1. **Como nó de um Grafo (LangGraph)**:
   O `BaseAgent` implementa o método especial `__call__(state: dict) -> Command`. Quando o agente é adicionado como um nó no grafo, o LangGraph o invoca diretamente. Esse método executa o agente e retorna um objeto `Command` para controlar o fluxo do grafo.

2. **Execução Direta (Sem Grafo / Testes)**:
   O método assíncrono `run(state: dict) -> AgentRunResult` permite executar o agente diretamente. Ele retorna um objeto `AgentRunResult` contendo:
   - `structured_response`: A resposta estruturada gerada pelo LLM (conforme o schema definido).
   - `messages`: A lista de mensagens (histórico/transcrição) geradas durante a execução do turno do agente (incluindo chamadas de ferramentas e respostas).

## Criando um novo grafo

1. Crie a classe do grafo em `app/nexus/graphs/` com um `NAME: str` único e um método `compile(checkpointer) -> CompiledStateGraph`.
2. No `lifespan` (`app/entrypoints/rest/events/lifespan.py`), compile o novo grafo e crie o `GraphExecutor` correspondente.
3. Crie a rota e a dependency que injeta o executor correto.

O `GraphExecutor` é genérico — ele roda qualquer `CompiledStateGraph`. A escolha de qual grafo usar é responsabilidade do `lifespan` e dos endpoints, não do executor.
