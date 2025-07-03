# GenIA - Kafka Consumer

## Descrição

Este é um serviço construido utilizando Uvicorn + FastAPI, com objetivo de criar um serviço que escuta alguns topicos no Kafka.

A escolha dos topicos mapeados no Kafka se dá através de um prefixo do topico, configurado no arquivo `.env`, através da variavel `KAFKA_TOPIC_PREFIX`.

Após escutar e receber mensagens esse serviço faz a ingestão dos dados no banco `pgvector`.


### Tecnologias

- Python 3.11
- FastAPI
- Uvicorn
- PGVector
- Loguru (logging)
- Docker / Docker Compose

### Pré-requisitos

- Python 3.11
- Docker & Docker Compose (para uso em container)
- PostgreSQL com extensão pgvector
- confluent-kafka (ver no readme principal como instalar)


## Estrutura Basica de Pastas

```plaintext
kafka_consumer/
   ├─ dockerfile                # Build Docker do backend
   ├─ requirements.txt          # Dependências Python
   └─ app/
      ├─ core/                  # Configurações e conexão ao DB
      │  ├─ config.py           # Leitura de .env e montagem da URI
      ├─ services/              # Lógica de negócio
      │  ├─ kafka_listerner.py  # Principal servico da aplicacao, ouvinte dos topicos kafka e ingestão na base de dados
      └─ main.py                # Instância FastAPI, inicialização do service
```


## Instalação Local

#### Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate       # Linux/macOS
.venv\Scripts\Activate.ps1    # Windows PowerShell
```

### Instale as dependências:

Para realizar a instalação do ambiente execute os passos abaixos
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Para instalação do `confluent-kafka`, veja o Readme na raiz do repositorio.


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
 uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```


### Usando Docker Compose

Na raiz do projeto (/), rode:
```bash
docker compose up -d --build
```

Para parar e remover containers:
```bash
docker compose down
```
