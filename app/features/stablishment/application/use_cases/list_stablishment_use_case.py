from http import HTTPStatus
from typing import List

from fastapi import HTTPException

from app.features.stablishment.dtos.response.get_stablishment_dto import (
    GetStablishmentDto,
)
from app.features.stablishment.infra.repositories.stablishment_repository import (
    StablishmentRepository,
)


class ListStablishmentUseCase:
    def __init__(self, stablishment_repository: StablishmentRepository) -> None:
        self.stablishment_repository = stablishment_repository

    def execute(self) -> List[GetStablishmentDto]:
        stablishments = self.stablishment_repository.getMany()
        if len(stablishments) == 0:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Nenhum estabelecimento cadastrado",
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
