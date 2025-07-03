# GenIA

## Descrição

Projeto de Arquitetura de solução para um sistema de IA que integra:
- Crawlers para coleta de dados
- Armazenamento em banco de dados PostgreSQL com extensão pgvector
- API RESTful com FastAPI
- Serviços de Mensageria com Kafka
- Integração com Azure OpenAI para chat completions e embeddings
- Interface de visualização com Langflow
- Monitoramento e logging com Loguru
- Docker para containerização


### Tecnologias

- Python 3.11
- FastAPI
- Uvicorn
- Docker
- Langflow
- Kafka (Zookeeper, Kafka, Kafka UI)
- PostgreSQL com extensão pgvector
- Azure OpenAI (Chat Completions e Embeddings)



## Estrutura Basica De Pastas

```plaintext
ROOT/
├─ apps/                                        # Pasta com os aplicativos principais
│   ├─ backend/
│   │     ├─ dockerfile                         # Build Docker do backend
│   │     ├─ requirements.txt                   # Dependências Python
│   │     └─ app/
│   │     │     ├─ core/                        # Configurações e conexão ao DB
│   │     │     ├─ config.py                    # Leitura de .env e montagem da URI
│   │     │     ├─ database.py                  # Sessões SQLAlchemy
│   │     │     ├─ kafka.py                     # Serviço que conecta no Kafka e produz mensagens
│   │     │     └─ vector_db.py                 # Registro do tipo VECTOR
│   │     │     ├─ middleware/                  # Middlewares (ex. logging)
│   │     │     │  └─ logging_middleware.py
│   │     │     ├─ models/                      # Schemas Pydantic / ORM
│   │     │     │  ├─ document_model.py         # Identificação e padronização do input de documentos
│   │     │     ├─ repositories/                # Acesso a dados (CRUD)
│   │     │     │  ├─ document_repository.py    # Respositorio para manipular a camada de documentos no BD
│   │     │     ├─ services/                    # Lógica de negócio
│   │     │     │  └─ document_service.py       # Serviço faz a ingestão de documentos na base
│   │     │     │  └─ kafka_service.py          # Serviço cria uma mensagem no topico Kafka
│   │     │     ├─ routes/                      # Definição de endpoints
│   │     │     │  ├─ document_route.py         # Rotas disponibilizadas para Documentos
│   │     │     ├─ utils/                       # Helpers gerais
│   │     │     │  └─ logger.py                 # Configuração do Loguru
│   │     │     └─ main.py                      # Instância FastAPI, roteamento e eventos
│   ├─ frontend/                                # Frontend (a definir)
├─ langflow/                                    # Langflow Tool
│   ├─ flows/                                   # Fluxos salvos do Langflow
│   ├─ custom_components/                       # Pasta para componentes personalizados do Langflow
│   │   └─ component_A/                         # Definir nome do componente
├─ services/                                    # Pasta contendo nossos componentes (services)
│   ├─ kafka_consumer/
│   │       ├─ dockerfile                       # Build Docker do backend
│   │       ├─ requirements.txt                 # Dependências Python
│   │       └─ app/
│   │           ├─ core/                        # Configurações e conexão ao DB
│   │           │   └─ config.py                # Leitura de .env e montagem da URI
│   │           ├─ services/                    # Lógica de negócio
│   │           │   └─ kafka_listerner.py       # Principal servico da aplicacao, ouvinte dos topicos kafka e ingestão na base de dados
│   │           └─ main.py                      # Instância FastAPI, inicialização do service
├─ widgets/                                     # Pasta contendo services que coletam dados de fontes externas
│    ├─ crawler_sample/                         # Serviço de Crawler de exemplo
│    ├─ sharepoint_service/                     # Serviço que deverá ler o sharepoint e gerar mensagens no Kafka
├─ docker-compose.yml                           # arquivo de configuração do Docker Compose
```

## Instalação do Ambiente

### Instalando o Kafka Confluent
Para que a aplicação consiga se comunicar com o Kafka, é necessário instalar a biblioteca `confluent-kafka`.
Para instalar o Kafka Confluent, siga as instruções abaixo, esse processo pode variar dependendo do seu sistema operacional, porém essa instalação é necessária para disponibilizar a funcionalidade de streaming de documentos para o Kafka.

```bash
# No Ubuntu/Debian:
sudo apt-get update
sudo apt-get install -y librdkafka-dev

# No macOS (com Homebrew):
brew install librdkafka

# Depois, no seu virtualenv Python:
pip install confluent-kafka
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

## Usando Docker Compose

Na raiz do projeto (/), rode:
```bash
docker compose up -d --build
```

Isso irá subir:

- postgres (com pgvector)
- backend_api (FastAPI)
- Outros serviços configurados (crawler, langflow, etc)

Para parar e remover containers:
```bash
docker compose down
```