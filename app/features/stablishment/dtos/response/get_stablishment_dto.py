from fastapi.exceptions import BaseModel


class GetStablishmentDto(BaseModel):
    name: str
    description: str
    address: str
    latitude: float
    longitude: float
