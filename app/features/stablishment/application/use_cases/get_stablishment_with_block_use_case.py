from http import HTTPStatus

from fastapi import HTTPException
from app.features.stablishment.dtos.response.get_block_dto import GetBlockDto
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


class GetStablishmentWithBlockUseCase:
    def __init__(
        self,
        stablishment_repository: StablishmentRepository,
        blockchain_repository: BlockChainRepository,
    ) -> None:
        self.stablishment_repository = stablishment_repository
        self.blockchain_repository = blockchain_repository

    def execute(self, id: Guid) -> GetStablishmentWithBlockDto:
        stablishment = self.stablishment_repository.find(id)
        if stablishment is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Estabelecimento não encontrado",
            )

        blockchain = self.blockchain_repository.get()
        if blockchain is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Blockchain não encontrada",
            )

        block = blockchain.get_block_by_stablishment_id(id)
        if block is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Bloco não encontrado",
            )

        previous_block = blockchain.get_block_by_index(block.index - 1)
        if previous_block is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Bloco anterior não encontrado",
            )

        return GetStablishmentWithBlockDto(
            stablishment=GetStablishmentDto(
                id=stablishment.id.value,
                name=stablishment.name,
                description=stablishment.description,
                address=stablishment.address,
                latitude=stablishment.latitude,
                longitude=stablishment.longitude,
            ),
            block=GetBlockDto(
                data=block.data,
                index=block.index,
                timestamp=block.timestamp.formatted_value,
                previous_hash=block.previous_hash,
                hash=block.hash,
                nonce=block.nonce,
            ),
            is_valid_block=block.is_valid(previous_block, blockchain.difficulty),
        )
