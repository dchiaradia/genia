import uvicorn
from fastapi import FastAPI
from app.services.kafka_listener import start_listener

app = FastAPI(docs_url=None, redoc_url=None)

@app.on_event("startup")
def startup_event():
    start_listener()

# opcional: healthcheck
@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, log_level="info")
