import logging
import os
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from api import api_router, get_db, initialize_database


LOG_LEVEL = os.getenv("SAVE_TEARS_LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("save_tears.backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    logger.info("backend_started service=save-tears-backend")
    yield


app = FastAPI(title="Save Tears Backend", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or uuid.uuid4().hex[:12]
    start_time = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.exception(
            "request_failed method=%s path=%s duration_ms=%.2f request_id=%s",
            request.method,
            request.url.path,
            duration_ms,
            request_id,
        )
        raise

    duration_ms = (time.perf_counter() - start_time) * 1000
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "request_completed method=%s path=%s status=%s duration_ms=%.2f request_id=%s",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        request_id,
    )
    return response


@app.get("/")
def read_root():
    return {"message": "System Online"}


@app.get("/health")
def read_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1")).scalar()
    return {
        "status": "ok",
        "database": "ok",
        "service": "save-tears-backend",
        "version": app.version,
    }


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
