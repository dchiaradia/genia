from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.utils.logger import get_logger 

log = get_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        log.info(f"Incoming request: {request.method} {request.url.path}")
        response = await call_next(request)
        log.info(f"Response status: {response.status_code}")
        return response
