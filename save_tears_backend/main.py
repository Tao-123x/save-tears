import asyncio
import logging
import os
import time
import uuid
from contextlib import asynccontextmanager, suppress

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from api import SessionLocal, api_router, get_db, initialize_database, sync_thingspeak_events


LOG_LEVEL = os.getenv("SAVE_TEARS_LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("save_tears.backend")


def get_thingspeak_sync_interval_seconds() -> int:
    raw_value = os.getenv("SAVE_TEARS_THINGSPEAK_SYNC_INTERVAL_SECONDS", "0").strip()
    if not raw_value:
        return 0
    try:
        return max(int(raw_value), 0)
    except ValueError:
        logger.warning("thingspeak_sync_disabled reason=invalid_interval value=%s", raw_value)
        return 0


def get_thingspeak_sync_results() -> int:
    raw_value = os.getenv("SAVE_TEARS_THINGSPEAK_SYNC_RESULTS", "20").strip()
    try:
        return max(int(raw_value), 1)
    except ValueError:
        logger.warning("thingspeak_sync_results_defaulted reason=invalid_value value=%s", raw_value)
        return 20


def run_thingspeak_sync_once() -> None:
    db = SessionLocal()
    try:
        result = sync_thingspeak_events(results=get_thingspeak_sync_results(), db=db, _=None)
        logger.info(
            "thingspeak_sync_completed synced=%s skipped=%s",
            result.get("synced"),
            result.get("skipped"),
        )
    except Exception:
        logger.exception("thingspeak_sync_failed")
    finally:
        db.close()


async def run_thingspeak_sync_loop(interval_seconds: int) -> None:
    while True:
        await asyncio.to_thread(run_thingspeak_sync_once)
        await asyncio.sleep(interval_seconds)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    sync_task = None
    sync_interval = get_thingspeak_sync_interval_seconds()
    if sync_interval > 0:
        sync_task = asyncio.create_task(run_thingspeak_sync_loop(sync_interval))
        logger.info("thingspeak_sync_enabled interval_seconds=%s", sync_interval)
    logger.info("backend_started service=save-tears-backend")
    try:
        yield
    finally:
        if sync_task:
            sync_task.cancel()
            with suppress(asyncio.CancelledError):
                await sync_task


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
