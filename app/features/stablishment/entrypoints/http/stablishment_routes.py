from ...infra.repositories.stablishment_repository import StablishmentRepository
from ...domain.use_cases.create_stablishment_use_case import (
    CreateStablishmentUseCase,
)
from ...dtos.response.get_stablishment_dto import GetStablishmentDto
from ...dtos.request.create_stablishment_dto import CreateStablishmentDto

from fastapi import APIRouter

stablishment_router = APIRouter()

stablishment_repository = StablishmentRepository()
create_stablishment_use_case = CreateStablishmentUseCase(stablishment_repository)


@stablishment_router.post("/stablishment", response_model=GetStablishmentDto)
def create(create_stablishment_dto: CreateStablishmentDto):
    return create_stablishment_use_case.execute(create_stablishment_dto)
