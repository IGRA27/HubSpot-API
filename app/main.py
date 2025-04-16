from fastapi import FastAPI
from .config import get_settings
from .routers import docs, search, crm
from .workers import indexer

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/swagger",
    redoc_url=None
)

# Routers
app.include_router(docs.router)
app.include_router(search.router)
app.include_router(crm.router)

# Health‑check
@app.get("/health")
async def health():
    return {"status": "ok"}

# Startup: arranca el indexer (seguidor de cambios)
@app.on_event("startup")
async def startup_event():
    import asyncio, logging
    logging.basicConfig(level="INFO")
    asyncio.create_task(indexer.start())
