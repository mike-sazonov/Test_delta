from fastapi import APIRouter, Depends

from app.db.models import ParcelType
from app.db.database import AsyncSession, get_db
from app.api.schemas.parcel import ParcelTypeCreate
from app.usecases.usecases import calculate_delivery_costs


command_router = APIRouter(
    prefix="/command",
    tags=["Command"]
)

@command_router.get("/run-delivery-calc/")
async def run_delivery_calculation(db: AsyncSession = Depends(get_db)):
    await calculate_delivery_costs(db)
    return {"message": "Расчет выполнен вручную"}


@command_router.post("/create-parcel-type/")
async def create_parcel_type(parcel_type: ParcelTypeCreate, db: AsyncSession = Depends(get_db)):
    db_parcel_type = ParcelType(**parcel_type.dict())
    db.add(db_parcel_type)
    await db.commit()
    return {"id": db_parcel_type.id, "message": "Тип посылки добавлен"}