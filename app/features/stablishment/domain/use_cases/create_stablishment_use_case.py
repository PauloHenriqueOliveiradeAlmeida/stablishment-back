from fastapi import HTTPException
from app.features.stablishment.domain.entities.stablishment_entity import (
    StablishmentEntity,
)
from app.features.stablishment.domain.entities.blockchain import (
    BlockChain
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
        self.blockchain = BlockChain()

    def execute(self, dto: CreateStablishmentDto) -> StablishmentEntity:
        stablishments = self.stablishment_repository.findByDistance(dto, 2000)
        if len(stablishments) > 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Os estabelecimentos devem ter uma distância de, pelo menos 2000km",
            )
        stablishment = self.stablishment_repository.create(dto)
        self.blockchain.add_block(data={"establishment_id": stablishment.id})
        
        return stablishment
