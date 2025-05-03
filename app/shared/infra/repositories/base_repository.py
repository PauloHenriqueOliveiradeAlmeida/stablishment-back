from typing import TypeVar
from pymongo import MongoClient
from bson.objectid import ObjectId

T = TypeVar("T")


class BaseRepository[T]:
    __client: MongoClient = MongoClient(
        "mongodb+srv://paulo:Ptdk1282@uniso.wvwnctm.mongodb.net/?retryWrites=true&w=majority&appName=uniso"
    )

    def __init__(self, collection: str) -> None:
        self._connection = self.__client["stablishments_app"][collection]

    def create(self, data: T) -> T | None:
        id = self._connection.insert_one(data.__dict__).inserted_id
        return {**self._connection.find_one({"_id": ObjectId(id)}), "id": id.__str__()}

    def find(self, id: str) -> T | None:
        return self._connection.find_one({"_id": ObjectId(id)})

    def list(self) -> list[T]:
        items = self._connection.find().to_list(length=None)
        return [{**item, "id": item["_id"].__str__()} for item in items]
