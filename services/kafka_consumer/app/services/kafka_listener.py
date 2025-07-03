import json
import logging
import threading
from confluent_kafka import Consumer, KafkaError
from langchain.schema import Document
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores.pgvector import PGVector

from tabulate import tabulate

from app.core.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _azure_embeddings() -> AzureOpenAIEmbeddings:
    return AzureOpenAIEmbeddings(
        openai_api_base=settings.AZURE_OPEN_AI_EMBEDDING_URI,
        openai_api_version=settings.AZURE_OPEN_AI_EMBEDDING_VERSION,
        openai_api_key=settings.AZURE_OPEN_AI_EMBEDDING_KEY,
        model=settings.AZURE_OPEN_AI_EMBEDDING_MODEL_NAME,
        max_retries=3,
        request_timeout=60,
    )


def _pgvector_client(collection_name: str) -> PGVector:
    logger.info(f"Creating PGVector client for collection: {collection_name}")
    embeddings = _azure_embeddings()

    
    client = PGVector(
        settings.DATABASE_URL,
        embeddings,
        collection_name=collection_name,
        embedding_length=settings.EMBEDDING_DIM,
        use_jsonb=True,
        create_extension=True,
    )
    return client


def _process_message(msg) -> None:
    """
    Espera um JSON com as chaves:
      - collection_name: str
      - content: str
      - metadata: dict

    Se qualquer uma faltar, cai de volta para valores padrão.
    """
    raw = msg.value().decode("utf-8")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        logger.error("Mensagem inválida, não é um JSON:", raw)
        return

    # 1) Nome da coleção
    collection = payload.get("collection_name", msg.topic())

    # 2) Conteúdo do documento
    content = payload.get("content")
    if content is None:
        # fallback para todo o JSON serializado
        content = raw

    # 3) Metadata enviada no payload (apenas campos custom do usuário)
    metadata = payload.get("metadata", {})

    # (Opcional) incluir também metadata do Kafka dentro de um subcampo:
    metadata.update({
        "__kafka_topic": msg.topic(),
        "__kafka_partition": msg.partition(),
        "__kafka_offset": msg.offset(),
    })

    # 4) Envia ao PGVector
    client = _pgvector_client(collection)
    doc = Document(page_content=content, metadata=metadata)
    client.add_documents([doc])
    
    headers = ["Status", "Collection", "Content", "Metadata", "Offset", "Topic"]
    row = [[
        "Saved",
        collection,
        _truncate(content),
        _truncate(json.dumps(metadata)),
        msg.offset(),
        msg.topic(),
    ]]

    table = tabulate(row, headers=headers, tablefmt="github")
    # Loga a tabela inteira
    logger.info("\n%s", table)

def _consumer_loop() -> None:
    conf = {
        "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
        "group.id": settings.KAFKA_CONSUMER_GROUP,
        "auto.offset.reset": "earliest",
        "metadata.max.age.ms": str(settings.KAFKA_METADATA_MAX_AGE_MS),
        "topic.metadata.refresh.interval.ms": str(settings.KAFKA_METADATA_MAX_AGE_MS),

    }
    consumer = Consumer(conf)
    regex = f"^{settings.KAFKA_TOPIC_PREFIX}.*"
    consumer.subscribe([regex])
    logger.info(f"Subscribed to Kafka topics matching /{regex}/")

    try:
        while True:
            msg = consumer.poll(1.0)
            if not msg:
                continue
            if msg.error():
                if msg.error().code() != KafkaError._PARTITION_EOF:
                    logger.error(f"Kafka error: {msg.error()}")
                continue
            _process_message(msg)
    except Exception:
        logger.exception("Error in Kafka consumer loop")
    finally:
        consumer.close()


def start_listener() -> None:
    thread = threading.Thread(target=_consumer_loop, daemon=True)
    thread.start()
    logger.info("Kafka listener thread started")


def _truncate(text: str, length: int = 50) -> str:
    """Retorna até `length` chars e adiciona '...' se maior."""
    return (text[: length - 3] + "...") if len(text) > length else text
