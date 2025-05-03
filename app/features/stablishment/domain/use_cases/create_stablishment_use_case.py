from fastapi import HTTPException
from app.features.stablishment.domain.entities.stablishment_entity import (
    StablishmentEntity,
)
from app.features.stablishment.infra.repositories.stablishment_repository import (
    StablishmentRepository,
)
from app.features.stablishment.dtos.request.create_stablishment_dto import (
    CreateStablishmentDto,
)
from http import HTTPStatus


class CreateStablishmentUseCase:
    def __init__(self, stablishment_repository: StablishmentRepository) -> None:
        self.stablishment_repository = stablishment_repository

    def execute(self, dto: CreateStablishmentDto) -> StablishmentEntity:
        stablishments = self.stablishment_repository.findByDistance(dto, 2000)
        if len(stablishments) > 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Os estabelecimentos devem ter uma distância de, pelo menos 2000km",
            )
        return self.stablishment_repository.create(dto)
