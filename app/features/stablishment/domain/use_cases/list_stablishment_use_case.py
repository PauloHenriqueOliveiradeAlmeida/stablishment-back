from http import HTTPStatus
from typing import List

from fastapi import HTTPException
from app.features.stablishment.domain.entities.stablishment_entity import (
    StablishmentEntity,
)
from app.features.stablishment.infra.repositories.stablishment_repository import (
    StablishmentRepository,
)


class ListStablishmentUseCase:
    def __init__(self, stablishment_repository: StablishmentRepository) -> None:
        self.stablishment_repository = stablishment_repository

    def execute(self) -> List[StablishmentEntity]:
        stablishments = self.stablishment_repository.list()
        if len(stablishments) == 0:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Nenhum estabelecimento cadastrado",
            )

        return stablishments
