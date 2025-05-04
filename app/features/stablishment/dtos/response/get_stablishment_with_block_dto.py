from pydantic import BaseModel

from app.features.stablishment.dtos.response.get_block_dto import GetBlockDto
from app.features.stablishment.dtos.response.get_stablishment_dto import (
    GetStablishmentDto,
)


class GetStablishmentWithBlockDto(BaseModel):
    block: GetBlockDto
    stablishment: GetStablishmentDto
    is_valid_block: bool
