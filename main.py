import uvicorn

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.api.endpoints.parcel import parcel_router
from app.db.database import engine, Base



app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="supersecret")
app.include_router(parcel_router)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
