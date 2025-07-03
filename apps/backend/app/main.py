from fastapi import FastAPI
from app.core.config import Settings
from app.middleware.logging_middleware import LoggingMiddleware
from app.routes import all_routers
from app.utils.logger import get_logger

settings = Settings()
log = get_logger()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_DOCS_URL}",
)

# registra middleware
app.add_middleware(LoggingMiddleware)

# monta as rotas
for router in all_routers:
    app.include_router(router, prefix=settings.API_V1_STR)

# registra o handler de startup sem usar @on_event
def _startup_log():
    log.success(f"API ONLINE: {settings.API_DOCS_URL}")


app.add_event_handler("startup", _startup_log)

@app.get("/health", tags=["Health"])
async def health_check():
    """Verifica se o serviço está vivo."""
    return {"status": "ok"}
