from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.document_model import DocumentIn
from app.services.document_service import ingest_document
from app.utils.logger import get_logger
from app.services.kafka_service import stream_document_to_kafka

log = get_logger()

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@router.post(
    "/ingest",
    status_code=status.HTTP_201_CREATED,
    summary="Ingestão de documento vetorial",
)
async def ingest(payload: DocumentIn):
    """
    Recebe um documento e um nome de coleção, gera embedding e grava no Postgres+PGVector.
    """
    try:
        ingest_document(
            payload.collection_name,
            payload.content,
            metadata=payload.metadata,
        )
    except Exception as e:
        log.error(f"→ {str(e)} \n → {str(payload)}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    return {
        "status": "success",
        "collection": payload.collection_name
    }
    
@router.post(
    "/ingest/stream",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Enfileirar documento no Kafka (stream)",
)
async def ingest_stream(payload: DocumentIn):
    """
    Recebe um DocumentIn e publica a mensagem no Kafka,
    no tópico cujo nome é payload.collection_name.
    """
    try:
        stream_document_to_kafka(payload)
    except Exception as e:
        log.error(f"Falha ao enfileirar streaming: {e} — payload: {payload.json()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao enviar para Kafka: {e}"
        )
    return {"status": "queued", "topic": payload.collection_name}
