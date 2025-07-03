from typing import Any, Dict
from sqlalchemy.orm import Session
from app.repositories.document_repository import add_document_to_collection

def ingest_document(
    collection_name: str,
    content: str,
    metadata: Dict[str, Any],
) -> None:
    """
    Lógica de negócio para ingestão vetorial, com metadados.
    """
    add_document_to_collection(
        collection_name=collection_name,
        content=content,
        metadata=metadata,
    )
