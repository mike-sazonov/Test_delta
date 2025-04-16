import uvicorn

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from apscheduler.triggers.cron import CronTrigger

from app.api.endpoints.parcel import parcel_router
from app.api.endpoints.commands import command_router
from app.db.database import engine, Base, AsyncSessionLocal
from app.usecases.usecases import calculate_delivery_costs
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.config import settings


scheduler = AsyncIOScheduler()

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET)
app.include_router(parcel_router)
app.include_router(command_router)


async def calculate_delivery_costs_with_session():
    async with AsyncSessionLocal() as session:
        await calculate_delivery_costs(session)


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    scheduler.add_job(
        func=calculate_delivery_costs_with_session,
        trigger=CronTrigger(minute="*/5")
    )
    scheduler.start()


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
