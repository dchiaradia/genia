from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from pgvector.psycopg2 import register_vector
from app.core.config import settings

vector_engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

@event.listens_for(vector_engine, "connect")
def _register_vector(dbapi_connection, connection_record):
    register_vector(dbapi_connection)

VectorSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=vector_engine,
)

def get_vector_db():
    db = VectorSessionLocal()
    try:
        yield db
    finally:
        db.close()
