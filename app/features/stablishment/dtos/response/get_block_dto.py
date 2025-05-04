from pydantic import BaseModel


class GetBlockDto(BaseModel):
    index: int
    timestamp: str
    data: dict
    previous_hash: str
    hash: str
    nonce: int
