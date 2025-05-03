from http import HTTPStatus

from fastapi import HTTPException
from app.features.stablishment.dtos.response.count_stablishment_dto import (
    CountStablishmentDto,
)
from app.features.stablishment.infra.repositories.stablishment_repository import (
    StablishmentRepository,
)


class CountStablishmentByRadiusUseCase:
    def __init__(self, stablishment_repository: StablishmentRepository) -> None:
        self.stablishment_repository = stablishment_repository

    def execute(self, id: str, radius: float) -> CountStablishmentDto:
        stablishment = self.stablishment_repository.find(id)
        if stablishment is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Estabelecimento não encontrado",
            )

        count = self.stablishment_repository.countByDistanceRadius(stablishment, radius)
        return CountStablishmentDto(count=count)
