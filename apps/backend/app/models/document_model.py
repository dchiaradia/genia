from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class DocumentIn(BaseModel):
    """
    Payload para ingestão de um documento vetorial.
    """
    collection_name: str = Field(..., example="minha_colecao")
    content: str = Field(..., example="Texto completo do documento a ser indexado")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        example={"url": "https://meusite.com/artigo/123", "author": "João"}
    )
