from app.features.stablishment.entrypoints.http.stablishment_routes import (
    stablishment_router,
)
from fastapi import FastAPI


router = FastAPI()

router.include_router(stablishment_router)
