import uvicorn

from fastapi import FastAPI
from app.api.endpoints.parcel import package_router
from app.db.database import engine, Base

app = FastAPI()

app.include_router(package_router)


# @app.on_event("startup")
# async def init_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
