from app.features.stablishment.domain.aggregates.blockchain import BlockChain
from app.features.stablishment.domain.entities.stablishment import Stablishment
from app.features.stablishment.dtos.response.get_stablishment_dto import (
    GetStablishmentDto,
)
from app.features.stablishment.infra.repositories.blockchain_repository import (
    BlockChainRepository,
)
from app.features.stablishment.infra.repositories.stablishment_repository import (
    StablishmentRepository,
)
from app.features.stablishment.dtos.request.create_stablishment_dto import (
    CreateStablishmentDto,
)
from http import HTTPStatus
from fastapi import HTTPException

from app.settings import settings


class CreateStablishmentUseCase:
    def __init__(
        self,
        stablishment_repository: StablishmentRepository,
        blockchain_repository: BlockChainRepository,
    ) -> None:
        self.stablishment_repository = stablishment_repository
        self.blockchain_repository = blockchain_repository

    def execute(self, dto: CreateStablishmentDto) -> GetStablishmentDto:
        stablishment = Stablishment(
            name=dto.name,
            description=dto.description,
            address=dto.address,
            latitude=dto.latitude,
            longitude=dto.longitude,
        )

        MIN_DISTANCE = 2000
        stablishments = self.stablishment_repository.findByDistance(
            stablishment, MIN_DISTANCE
        )

        if len(stablishments) > 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Os estabelecimentos devem ter uma distância de, pelo menos 2000km",
            )

        created = self.stablishment_repository.create(stablishment)
        if not created:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Erro ao criar estabelecimento",
            )

        blockchain = self.blockchain_repository.get()
        if blockchain is None:
            blockchain = BlockChain(difficulty=settings.blockchain_difficulty)
            self.blockchain_repository.create(blockchain)

        blockchain.add_block({"stablishment_id": stablishment.id.value})
        self.blockchain_repository.update(blockchain)

        return GetStablishmentDto(
            id=stablishment.id.value,
            name=stablishment.name,
            description=stablishment.description,
            address=stablishment.address,
            latitude=stablishment.latitude,
            longitude=stablishment.longitude,
        )
