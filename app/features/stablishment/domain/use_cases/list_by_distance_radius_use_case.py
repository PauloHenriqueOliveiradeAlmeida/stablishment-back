from http import HTTPStatus
from typing import List

from fastapi import HTTPException
from app.features.stablishment.domain.entities.stablishment_entity import (
    StablishmentEntity,
)
from app.features.stablishment.infra.repositories.stablishment_repository import (
    StablishmentRepository,
)


class ListStablishmentByDistanceRadiusUseCase:
    def __init__(self, stablishment_repository: StablishmentRepository) -> None:
        self.stablishment_repository = stablishment_repository

    def execute(self, id: str, radius: float) -> List[StablishmentEntity]:
        stablishment = self.stablishment_repository.find(id)
        print(stablishment)
        if stablishment is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Estabelecimento não encontrado",
            )

        stablishments = self.stablishment_repository.listWithDistanceRadius(
            stablishment, radius
        )

        return stablishments
