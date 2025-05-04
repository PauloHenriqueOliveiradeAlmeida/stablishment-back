from typing import List
from app.features.stablishment.domain.entities.stablishment import Stablishment
from app.shared.infra.repositories.base_repository import BaseRepository


class StablishmentRepository(BaseRepository[Stablishment]):
    def __init__(self) -> None:
        super().__init__("stablishments")

    def findByDistance(
        self, stablishment: Stablishment, distance: float
    ) -> List[Stablishment]:
        stablishments = self._connection.aggregate(
            [
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
                        "maxDistance": distance,
                        "spherical": True,
                    }
                }
            ]
        ).to_list()

        return stablishments

    def countByDistanceRadius(self, stablishment: Stablishment, radius: float) -> int:
        return (
            self._connection.aggregate(
                [
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
                ]
            )
            .to_list()
            .__len__()
        )

    def listWithDistanceRadius(
        self, stablishment: Stablishment, radius: float
    ) -> List[Stablishment]:
        data = self._connection.aggregate(
            [
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
            ]
        ).to_list()

        return [self.build({**item, "id": item["_id"]}) for item in data]

    def build(self, data: dict) -> Stablishment:
        return Stablishment.from_dict(data)
