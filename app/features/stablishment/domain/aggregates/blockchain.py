from app.features.stablishment.domain.entities.block import Block
from app.shared.domain.entities.base_entity import BaseEntity
from app.shared.domain.value_objects.guid import Guid


class BlockChain(BaseEntity):
    def __init__(self, difficulty: int = 6):
        super().__init__()
        self.chain: list[Block] = []
        self.difficulty = difficulty
        self.__create_genesis_block()

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data: dict) -> None:
        last_block = self.get_last_block()
        block = Block.mine(
            index=last_block.index + 1,
            data=data,
            previous_hash=last_block.hash,
            difficulty=self.difficulty,
        )
        self.chain.append(block)

    def get_block_by_index(self, index: int) -> Block | None:
        return self.chain[index]

    def get_block_by_stablishment_id(self, id: Guid) -> Block | None:
        for block in self.chain:
            if block.data.get("stablishment_id") == id.value:
                return block
        return None

    def to_dict(self):
        return {
            "chain": [block.to_dict() for block in self.chain],
            "difficulty": self.difficulty,
        }

    @classmethod
    def from_dict(cls, data: dict):
        block_chain = cls()
        block_chain.id = data["id"]
        block_chain.chain = [Block.from_dict(block) for block in data["chain"]]
        block_chain.difficulty = data["difficulty"]
        return block_chain

    def validate_chain(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if not current_block.is_valid(previous_block, self.difficulty):
                return False
        return True

    def __create_genesis_block(self):
        if self.chain:
            return

        genesis_block = Block.mine(
            index=0,
            data={"name": "Genesis Block"},
            previous_hash="0",
            difficulty=self.difficulty,
        )
        self.chain.append(genesis_block)
