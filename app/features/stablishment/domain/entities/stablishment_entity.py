class StablishmentEntity:
    def __init__(
        self,
        name: str,
        description: str,
        address: str,
        latitude: float,
        longitude: float,
    ):
        self.name = name
        self.description = description
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
