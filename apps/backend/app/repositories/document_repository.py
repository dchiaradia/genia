import os
from typing import Any, Dict
from langchain_openai import AzureOpenAIEmbeddings
from langchain.schema import Document
from langchain_community.vectorstores.pgvector import PGVector

from app.core.config import settings


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

def add_document_to_collection(
    collection_name: str,
    content: str,
    metadata: Dict[str, Any],
) -> None:
    """
    Cria a extensão, garante a tabela e insere um único documento via PGVector.
    """
    client = _pgvector_client(collection_name)

    doc = Document(page_content=content, metadata=metadata)

    client.add_documents([doc])
