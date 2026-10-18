from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import engine, Base
from app.routers.tables import router as tables_router
from app.routers.bookings import router as booking_router
from app.routers.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
        await engine.dispose()

app = FastAPI(title="ReserveMaster API", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(tables_router)
app.include_router(booking_router)

@app.get("/")
async def root():
    return {"status": "ok", "message": "ReserveMaster API is running"}