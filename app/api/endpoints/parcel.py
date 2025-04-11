import uuid

from fastapi import Request, APIRouter, Depends
from sqlalchemy import select
from typing import List, Optional

from app.db.database import AsyncSession, get_db
from app.api.schemas.parcel import ParcelCreate, ParcelOut, ParcelTypeOut
from app.db.models import Parcel, ParcelType

parcel_router = APIRouter(
    prefix="/parcel",
    tags=["Parcel"]
)


@parcel_router.post("/parcels/", response_model=dict)
async def register_parcel(parcel: ParcelCreate, request: Request, db: AsyncSession = Depends(get_db)):
    session_id = request.session.setdefault("session_id", str(uuid.uuid4()))
    db_parcel = Parcel(**parcel.dict(), session_id=session_id)
    db.add(db_parcel)
    await db.commit()
    return {"id": db_parcel.id, "message": "Посылка зарегистрирована"}


@parcel_router.get("/types/", response_model=List[ParcelTypeOut])
async def get_parcel_types(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ParcelType))
    return result.scalars().all()


@parcel_router.get("/parcels/", response_model=List[ParcelOut])
async def get_user_parcels(
    request: Request,
    type_id: Optional[int] = None,
    is_cost_calculated: Optional[bool] = None,
    page: int = 1,
    size: int = 10,
    db: AsyncSession = Depends(get_db),
):
    session_id = request.session.get("session_id")
    if not session_id:
        return []
    stmt = select(Parcel).where(Parcel.session_id == session_id)
    if type_id:
        stmt = stmt.where(Parcel.type_id == type_id)
    if is_cost_calculated is not None:
        if is_cost_calculated:
            stmt = stmt.where(Parcel.delivery_cost_rub != None)
        else:
            stmt = stmt.where(Parcel.delivery_cost_rub == None)
    stmt = stmt.offset((page - 1) * size).limit(size)
    result = await db.execute(stmt)
    parcels = result.scalars().all()
    return [
        ParcelOut(
            id=p.id,
            name=p.name,
            weight=p.weight,
            declared_value_usd=p.declared_value_usd,
            type_name=p.type.name,
            delivery_cost_rub=p.delivery_cost_rub if p.delivery_cost_rub else "Не рассчитано"
        ) for p in parcels
    ]

@parcel_router.get("/parcels/{parcel_id}", response_model=ParcelOut)
async def get_parcel(parcel_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    session_id = request.session.get("session_id")
    stmt = select(Parcel).where(Parcel.id == parcel_id, Parcel.session_id == session_id)
    result = await db.execute(stmt)
    parcel = result.scalar_one_or_none()
    if not parcel:
        raise HTTPException(status_code=404, detail="Посылка не найдена")
    return ParcelOut(
        id=parcel.id,
        name=parcel.name,
        weight=parcel.weight,
        declared_value_usd=parcel.declared_value_usd,
        type_name=parcel.type.name,
        delivery_cost_rub=parcel.delivery_cost_rub if parcel.delivery_cost_rub else "Не рассчитано"
    )

