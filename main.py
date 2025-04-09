import uvicorn
from fastapi import FastAPI
from app.api.endpoints.package import package_router


app = FastAPI()

app.include_router(package_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
