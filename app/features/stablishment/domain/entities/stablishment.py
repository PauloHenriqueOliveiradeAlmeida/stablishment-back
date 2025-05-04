from app.shared.domain.entities.base_entity import BaseEntity


class Stablishment(BaseEntity):
    def __init__(
        self,
        name: str,
        description: str,
        address: str,
        latitude: float,
        longitude: float,
        id: str | None = None,
    ):
        super().__init__(id)
        self.name = name
        self.description = description
        self.address = address
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data["name"],
            data["description"],
            data["address"],
            data["latitude"],
            data["longitude"],
            data["id"],
        )
