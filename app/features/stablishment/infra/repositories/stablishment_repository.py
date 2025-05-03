from typing import List
from .....shared.infra.repositories.base_repository import BaseRepository
from ...domain.entities.stablishment_entity import StablishmentEntity


class StablishmentRepository(BaseRepository[StablishmentEntity]):
    def __init__(self) -> None:
        super().__init__("stablishments")

    def findByDistance(
        self, stablishment: StablishmentEntity, distance: float
    ) -> List[StablishmentEntity]:
        stablishments = self._connection.aggregate([
            {
                "$geoNear": {
                    "near": {
                        "type": "Point",
                        "coordinates": [stablishment.longitude, stablishment.latitude],
                    },
                    "distanceField": "distance",
                    "maxDistance": distance,
                    "spherical": True,
                }
            }
        ]).to_list()

        return stablishments

    def countByDistanceRadius(
        self, stablishment: StablishmentEntity, radius: float
    ) -> int:
        return (
            self._connection.aggregate([
                {
                    "$geoNear": {
                        "near": {
                            "type": "Point",
                            "coordinates": [
                                stablishment["longitude"],
                                stablishment["latitude"],
                            ],
                        },
                        "distanceField": "distance",
                        "maxDistance": radius,
                        "spherical": True,
                    }
                }
            ])
            .to_list()
            .__len__()
        )

    def listWithDistanceRadius(
        self, stablishment: StablishmentEntity, radius: float
    ) -> List[StablishmentEntity]:
        return self._connection.aggregate([
            {
                "$geoNear": {
                    "near": {
                        "type": "Point",
                        "coordinates": [
                            stablishment.longitude,
                            stablishment.latitude,
                        ],
                    },
                    "distanceField": "distance",
                    "maxDistance": radius,
                    "spherical": True,
                }
            }
        ]).to_list()
