from fastapi import APIRouter


package_router = APIRouter(
    prefix="/package",
    tags=["Package"]
)


@package_router.get("/types")
async def get_types():
    ...


@package_router.post("/register")
async def create_package():
    ...

