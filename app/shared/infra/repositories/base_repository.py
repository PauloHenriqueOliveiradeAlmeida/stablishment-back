from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from pymongo import MongoClient
from app.settings import settings
from app.shared.domain.entities.base_entity import BaseEntity
from app.shared.domain.value_objects.guid import Guid


T = TypeVar("T", bound=BaseEntity)


class BaseRepository(ABC, Generic[T]):
    __client: MongoClient = MongoClient(settings.database_url)

    def __init__(self, collection: str) -> None:
        self._connection = self.__client[settings.database_collection][collection]

    def create(self, data: T) -> bool:
        id = data.id.value
        dict_data = data.to_dict()
        created = self._connection.insert_one({**dict_data, "_id": id})

        if (created.inserted_id) is None:
            return False

        return True

    def find(self, id: Guid) -> T | None:
        data = self._connection.find_one({"_id": id.value})
        if data is None:
            return None
        return self.build({**data, "id": data["_id"]})

    def getMany(self) -> list[T]:
        items = self._connection.find().to_list(length=None)
        return [self.build({**item, "id": item["_id"]}) for item in items]

    @abstractmethod
    def build(self, data: dict) -> T:
        pass
