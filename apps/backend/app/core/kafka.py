import json
from confluent_kafka import Producer
from app.core.config import settings

def send_to_kafka(topic: str, message: dict) -> None:
    """
    Envia uma mensagem (dicionário) para o tópico Kafka especificado,
    aplicando o prefixo definido em KAFKA_TOPIC_PREFIX.

    Args:
        topic (str): Nome base do tópico.
        message (dict): Payload que será serializado como JSON.
    """
    # constrói o nome do tópico com prefixo
    prefix = settings.KAFKA_TOPIC_PREFIX.strip()
    if prefix:
        full_topic = f"{prefix}_{topic}"
    else:
        full_topic = topic

    # configura o producer sempre com o valor mais recente\    
    cfg = {'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS}
    producer = Producer(cfg)
    
    # serializa e envia
    producer.produce(full_topic, json.dumps(message).encode('utf-8'))
    producer.flush()  # garante que a mensagem seja enviada imediatamente