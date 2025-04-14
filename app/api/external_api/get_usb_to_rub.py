import httpx

from app.core.config import settings
from app.db.redis import redis_client
from decimal import Decimal


async def get_usd_to_rub_rate():
    rate = await redis_client.get("usd_to_rub")
    if rate:
        return Decimal(rate)
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.DAILY_USD_RUB)
        data = response.json()
        rate = data["Valute"]["USD"]["Value"]
        await redis_client.set("usd_to_rub", rate, ex=3600)
        return Decimal(str(rate))
