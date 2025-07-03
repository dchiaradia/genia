from app.core.kafka import send_to_kafka
from app.models.document_model import DocumentIn

def stream_document_to_kafka(doc: DocumentIn) -> None:
    """
    Publica o payload completo de DocumentIn no tópico igual a doc.collection_name.
    """
    # serializa o Pydantic model em dict
    message = doc.dict()
    send_to_kafka(topic=doc.collection_name, message=message)
