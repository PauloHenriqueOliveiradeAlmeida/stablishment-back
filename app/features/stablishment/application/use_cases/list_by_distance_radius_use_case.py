from http import HTTPStatus
from typing import List

from fastapi import HTTPException

from app.features.stablishment.dtos.response.get_stablishment_dto import (
    GetStablishmentDto,
)
from app.features.stablishment.infra.repositories.stablishment_repository import (
    StablishmentRepository,
)
from app.shared.domain.value_objects.guid import Guid


class ListStablishmentByDistanceRadiusUseCase:
    def __init__(self, stablishment_repository: StablishmentRepository) -> None:
        self.stablishment_repository = stablishment_repository

    def execute(self, id: Guid, radius: float) -> List[GetStablishmentDto]:
        stablishment = self.stablishment_repository.find(id)
        if stablishment is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Estabelecimento não encontrado",
            )

        stablishments = self.stablishment_repository.listWithDistanceRadius(
            stablishment, radius
        )

        return [
            GetStablishmentDto(
                id=stablishment.id.value,
                name=stablishment.name,
                description=stablishment.description,
                address=stablishment.address,
                latitude=stablishment.latitude,
                longitude=stablishment.longitude,
            )
            for stablishment in stablishments
        ]
