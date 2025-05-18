from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.db.main import init_db
from app.routers import bookings, customers, rooms

BASE_PATH = Path(__file__).parent

version_prefix = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(customers.router, prefix=f"{version_prefix}/customers", tags=["Customers"])
app.include_router(rooms.router, prefix=f"{version_prefix}/rooms", tags=["Rooms"])
app.include_router(bookings.router, prefix=f"{version_prefix}/bookings", tags=["Bookings"])
