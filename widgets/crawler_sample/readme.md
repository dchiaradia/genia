# GenIA - CRAWLER SAMPLE

## Descrição

Este serviço tem como objetivo demonstrar como executar um serviço que coletará dados de um local, e adicionará na base de memoria do nosso projeto.

Esse serviço basico apenas para demonstração onde ele irá realizar os seguintes passos:
- 1. Coletar todas as noticias do site da UOL;
- 2. Criar embeddings dos chunks dessas noticias;
- 3. Realiza o envio dos chunks para o Backend via API;

### Tecnologias

- Python 3.11
- Loguru (logging)
- Docker / Docker Compose
- Requests

### Pré-requisitos

- Python 3.11
- Docker & Docker Compose (para uso em container)



## Estrutura Basica de Pastas

```plaintext
backend/
├─ dockerfile                    # Build Docker do backend
├─ requirements.txt              # Dependências Python
└─ app/
   ├─ core/                      # Configurações e conexão ao DB
   │  ├─ config.py               # Leitura de .env e montagem da URI
   │  ├─ database.py             # Sessões SQLAlchemy
   │  ├─ kafka.py                # Serviço que conecta no Kafka e produz mensagens
   │  └─ vector_db.py            # Registro do tipo VECTOR
   ├─ middleware/                # Middlewares (ex. logging)
   │  └─ logging_middleware.py
   ├─ models/                    # Schemas Pydantic / ORM
   │  ├─ document_model.py       # Identificação e padronização do input de documentos
   ├─ repositories/              # Acesso a dados (CRUD)
   │  ├─ document_repository.py  # Respositorio para manipular a camada de documentos no BD
   ├─ services/                  # Lógica de negócio
   │  └─ document_service.py     # Serviço faz a ingestão de documentos na base
   │  └─ kafka_service.py        # Serviço cria uma mensagem no topico Kafka
   ├─ routes/                    # Definição de endpoints
   │  ├─ document_route.py       # Rotas disponibilizadas para Documentos
   ├─ utils/                     # Helpers gerais
   │  └─ logger.py               # Configuração do Loguru
   └─ main.py                    # Instância FastAPI, roteamento e eventos
```


## Instalação Local

#### Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate       # Linux/macOS
.venv\Scripts\Activate.ps1    # Windows PowerShell
```


### Instale as dependências:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Configuração de Ambiente

As variaveis de ambiente são carregadas do arquivo `.env` localizado na raiz do projeto e injetado pelo `docker-compose`.
Você pode criar um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```bash
# APPS - BACKEND SETTINGS
APP_NAME=GenIA   # Nome da aplicação de API (Principal aplicacao)
DEBUG=True
API_V1_STR=/api/v1
EMBEDDING_DIM=1536

# KAFKA CONFIGURATION
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC_PREFIX=genia


# PG VECTOR DATABASE CONFIGURATION
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ia_team
POSTGRES_PORT=5432
POSTGRES_HOST=postgres

# AZURE - Chat completion
AZURE_OPEN_AI_CHAT_COMPLETION_URI={CHAT_COMPLETION_URI}
AZURE_OPEN_AI_CHAT_COMPLETION_KEY={CHAT_COMPLETION_KEY}
AZURE_OPEN_AI_CHAT_COMPLETION_VERSION={CHAT_COMPLETION_VERSION}
AZURE_OPEN_AI_CHAT_COMPLETION_NAME={CHAT_COMPLETION_NAME}
AZURE_OPEN_AI_CHAT_COMPLETION_MODEL_NAME={CHAT_COMPLETION_MODEL_NAME}


# AZURE LLM - Embedding
AZURE_OPEN_AI_EMBEDDING_URI={EMBEDDING_URI}
AZURE_OPEN_AI_EMBEDDING_KEY={EMBEDDING_KEY}
AZURE_OPEN_AI_EMBEDDING_VERSION={EMBEDDING_VERSION}
AZURE_OPEN_AI_EMBEDDING_NAME={EMBEDDING_NAME}
AZURE_OPEN_AI_EMBEDDING_MODEL_NAME={EMBEDDING_MODEL_NAME}

# SERVICES - APP KAFKA CONSUMER SETTINGS
KAFKA_CONSUMER_APP_NAME=GenIA - Kafka Consumer   # Nome do Serviço Kafka Consumer
KAFKA_CONSUMER_GROUP=genia_consumer
KAFKA_METADATA_MAX_AGE_MS=10000   # atualizacao do kafka metadata a cada 10 segundos


# WIDGETS - CRAWLER SAMPLE SETTINGS
WIDGET_CRAWLER_COLLECTION_NAME=crawler_sample    # Nome do Widgets de Exemplo - Crawler Sample
WIDGET_CRAWLER_API_URL=http://backend_api:8000/api/v1/documents/ingest/stream # URL do endpoint de ingestão
```


### Executando Localmente

Com o ambiente configurado, inicie o servidor:
```bash
python crawler.py
```

## Usando Docker Compose

Na raiz do projeto (/), rode:
```bash
docker compose up -d --build
```

Para parar e remover containers:
```bash
docker com


