from typing import List

from app.features.stablishment.application.use_cases.create_stablishment_use_case import (
    CreateStablishmentUseCase,
)
from app.features.stablishment.application.use_cases.get_stablishment_with_block_use_case import (
    GetStablishmentWithBlockUseCase,
)
from app.features.stablishment.application.use_cases.list_by_distance_radius_use_case import (
    ListStablishmentByDistanceRadiusUseCase,
)
from app.features.stablishment.application.use_cases.list_stablishment_use_case import (
    ListStablishmentUseCase,
)
from app.features.stablishment.dtos.request.create_stablishment_dto import (
    CreateStablishmentDto,
)
from app.features.stablishment.dtos.response.count_stablishment_dto import (
    CountStablishmentDto,
)

from app.features.stablishment.application.use_cases.count_stablishment_by_radius_use_case import (
    CountStablishmentByRadiusUseCase,
)

from fastapi import APIRouter

from app.features.stablishment.dtos.response.get_stablishment_dto import (
    GetStablishmentDto,
)
from app.features.stablishment.dtos.response.get_stablishment_with_block_dto import (
    GetStablishmentWithBlockDto,
)
from app.features.stablishment.infra.repositories.blockchain_repository import (
    BlockChainRepository,
)
from app.features.stablishment.infra.repositories.stablishment_repository import (
    StablishmentRepository,
)
from app.shared.domain.value_objects.guid import Guid

stablishment_router = APIRouter()

stablishment_repository = StablishmentRepository()
blockChainRepository = BlockChainRepository()
create_stablishment_use_case = CreateStablishmentUseCase(
    stablishment_repository,
    blockChainRepository,
)
list_stablishment_use_case = ListStablishmentUseCase(stablishment_repository)


@stablishment_router.post("/stablishment", response_model=GetStablishmentDto)
def create(create_stablishment_dto: CreateStablishmentDto):
    return create_stablishment_use_case.execute(create_stablishment_dto)


@stablishment_router.get("/stablishment", response_model=List[GetStablishmentDto])
def list():
    return list_stablishment_use_case.execute()


@stablishment_router.get(
    "/stablishment-with-block/{id}", response_model=GetStablishmentWithBlockDto
)
def get_with_block(id: str):
    return GetStablishmentWithBlockUseCase(
        stablishment_repository, blockChainRepository
    ).execute(Guid(id))


@stablishment_router.get(
    "/stablishment/{id}/count/{radius}", response_model=CountStablishmentDto
)
def count(id: str, radius: float):
    return CountStablishmentByRadiusUseCase(stablishment_repository).execute(
        Guid(id), radius
    )


@stablishment_router.get(
    "/stablishment/{id}/by-radius/{radius}", response_model=List[GetStablishmentDto]
)
def by_radius(id: str, radius: float):
    return ListStablishmentByDistanceRadiusUseCase(stablishment_repository).execute(
        Guid(id), radius
    )
