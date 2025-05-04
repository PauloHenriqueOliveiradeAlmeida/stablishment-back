import hashlib

from app.features.stablishment.domain.value_objects.timestamp import Timestamp


class Block:
    index: int
    timestamp: Timestamp
    data: dict
    previous_hash: str
    hash: str
    nonce: int

    def __init__(
        self,
    ) -> None:
        raise TypeError("Use Block.mine method instead")

    @classmethod
    def mine(cls, index: int, data: dict, previous_hash: str, difficulty: int):
        timestamp = Timestamp()
        nonce = 0
        while not cls.__is_valid_proof(
            index, timestamp, data, previous_hash, nonce, difficulty
        ):
            nonce += 1
        return cls.__create(index, timestamp, data, previous_hash, nonce)

    def is_valid(self, previous_block: "Block", difficulty: int) -> bool:
        if self.previous_hash != previous_block.hash:
            return False
        if self.index != previous_block.index + 1:
            return False
        if self.hash != self.__calculate_hash(
            self.index, self.timestamp, self.data, self.previous_hash, self.nonce
        ):
            return False
        if not self.__is_valid_proof(
            self.index,
            self.timestamp,
            self.data,
            self.previous_hash,
            self.nonce,
            difficulty,
        ):
            return False

        return True

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp.raw_value,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls.__create(
            data["index"],
            Timestamp(data["timestamp"]),
            data["data"],
            data["previous_hash"],
            data["nonce"],
        )

    @classmethod
    def __create(
        cls,
        index: int,
        timestamp: Timestamp,
        data: dict,
        previous_hash: str,
        nonce: int,
    ):
        block = cls.__new__(cls)
        block.index = index
        block.timestamp = timestamp
        block.data = data
        block.previous_hash = previous_hash
        block.hash = cls.__calculate_hash(index, timestamp, data, previous_hash, nonce)
        block.nonce = nonce
        return block

    @staticmethod
    def __is_valid_proof(
        index: int,
        timestamp: Timestamp,
        data: dict,
        previous_hash: str,
        nonce: int,
        difficulty: int,
    ) -> bool:
        return Block.__calculate_hash(
            index, timestamp, data, previous_hash, nonce
        ).startswith("0" * difficulty)

    @staticmethod
    def __calculate_hash(
        index: int, timestamp: Timestamp, data: dict, previous_hash: str, nonce: int
    ) -> str:
        value = f"{str(index)}{str(timestamp.raw_value)}{str(data)}{str(previous_hash)}{str(nonce)}"

        return hashlib.sha256(value.encode("utf-8")).hexdigest()
