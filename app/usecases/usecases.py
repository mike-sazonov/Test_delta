from decimal import Decimal
from sqlalchemy.future import select
from app.db.database import AsyncSession
from app.db.models import Parcel
from app.api.external_api.get_usb_to_rub import get_usd_to_rub_rate


async def calculate_delivery_costs(db: AsyncSession):
    rate = await get_usd_to_rub_rate()
    result = await db.execute(select(Parcel).where(Parcel.delivery_cost_rub == None))
    parcels = result.scalars().all()
    for parcel in parcels:
        cost = (parcel.weight * Decimal("0.5") + parcel.declared_value_usd * Decimal("0.01")) * rate
        parcel.delivery_cost_rub = cost.quantize(Decimal("0.01"))
    await db.commit()
