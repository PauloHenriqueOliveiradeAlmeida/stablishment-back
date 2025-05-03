from app.features.stablishment.entrypoints.http.stablishment_routes import (
    stablishment_router,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

router = FastAPI(title="Estabelecimentos", version="1.0.0")
router.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

router.include_router(stablishment_router)
