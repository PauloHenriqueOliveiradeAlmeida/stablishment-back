from typing import TypeVar
from pymongo import MongoClient

T = TypeVar("T")


class BaseRepository[T]:
    __client: MongoClient = MongoClient(
        ""
    )

    def __init__(self, collection: str) -> None:
        self._connection = self.__client[""][collection]

    def create(self, data: T) -> T | None:
        id = self._connection.insert_one(data.__dict__).inserted_id
        return self._connection.find_one({"_id": id})

    def find(self, data: T) -> T | None:
        return self._connection.find_one(data)
