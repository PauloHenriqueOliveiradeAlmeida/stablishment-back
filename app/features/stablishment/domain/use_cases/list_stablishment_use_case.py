from http import HTTPStatus
from typing import List

from fastapi import HTTPException

from app.features.stablishment.domain.entities.blockchain import Block
from app.features.stablishment.domain.entities.stablishment_entity import (
    StablishmentEntity,
)
from app.features.stablishment.infra.repositories.stablishment_repository import (
    StablishmentRepository,
)
from app.shared.infra.repositories.base_repository import BaseRepository


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
    
    def get_and_validate_blockchain(self) -> bool:
        blockchain_is_valid = self.stablishment_repository.is_chain_valid()
        return blockchain_is_valid


class GetBlockByStablishmentIdUseCase:
    def __init__(self, blockchain_repository: BaseRepository):
        self.blockchain_repository = blockchain_repository

    def execute(self, establishment_id: str) -> dict:
        block: Block = self.blockchain_repository.get_block_by_establishment_id(
            establishment_id
        )
        if block is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Block not found")
        is_valid = self.blockchain_repository.is_chain_valid()
        return {"block": block, "is_valid": is_valid}
