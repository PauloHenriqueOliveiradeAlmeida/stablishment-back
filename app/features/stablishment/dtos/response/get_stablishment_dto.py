from fastapi.exceptions import BaseModel


class GetStablishmentDto(BaseModel):
    id: str | None
    name: str
    description: str
    address: str
    latitude: float
    longitude: float
