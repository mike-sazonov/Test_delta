from fastapi import APIRouter, Depends

from app.db.database import AsyncSession, get_db
from app.usecases.usecases import calculate_delivery_costs


command_router = APIRouter(
    prefix="/command",
    tags=["Command"]
)

@command_router.get("/run-delivery-calc/")
async def run_delivery_calculation(db: AsyncSession = Depends(get_db)):
    await calculate_delivery_costs(db)
    return {"message": "Расчет выполнен вручную"}
