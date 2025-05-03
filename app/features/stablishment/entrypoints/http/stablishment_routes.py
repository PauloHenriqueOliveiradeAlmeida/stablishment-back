from typing import List
from app.features.stablishment.domain.use_cases.count_stablishment_by_radius_use_case import (
    CountStablishmentByRadiusUseCase,
)
from app.features.stablishment.domain.use_cases.list_by_distance_radius_use_case import (
    ListStablishmentByDistanceRadiusUseCase,
)
from app.features.stablishment.domain.use_cases.list_stablishment_use_case import (
    ListStablishmentUseCase,
)
from app.features.stablishment.dtos.response.count_stablishment_dto import (
    CountStablishmentDto,
)
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
list_stablishment_use_case = ListStablishmentUseCase(stablishment_repository)


@stablishment_router.post("/stablishment", response_model=GetStablishmentDto)
def create(create_stablishment_dto: CreateStablishmentDto):
    return create_stablishment_use_case.execute(create_stablishment_dto)


@stablishment_router.get("/stablishment", response_model=List[GetStablishmentDto])
def list():
    return list_stablishment_use_case.execute()


@stablishment_router.get(
    "/stablishment/{id}/count/{radius}", response_model=CountStablishmentDto
)
def count(id: str, radius: float):
    return CountStablishmentByRadiusUseCase(stablishment_repository).execute(id, radius)


@stablishment_router.get(
    "/stablishment/{id}/by-radius/{radius}", response_model=GetStablishmentDto
)
def by_radius(id: str, radius: float):
    return ListStablishmentByDistanceRadiusUseCase(stablishment_repository).execute(
        id, radius
    )
