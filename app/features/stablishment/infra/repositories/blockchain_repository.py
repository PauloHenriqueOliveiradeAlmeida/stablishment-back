from app.features.stablishment.domain.aggregates.blockchain import BlockChain
from app.shared.infra.repositories.base_repository import BaseRepository


class BlockChainRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__("blockchain")

    def create(self, data: BlockChain) -> bool:
        dict_blockchain = data.to_dict()
        created = self._connection.insert_one(
            {"type": "blockchain", "data": dict_blockchain}
        )

        if (created.inserted_id) is None:
            return False

        return True

    def update(self, blockchain: BlockChain) -> None:
        dict_blockchain = blockchain.to_dict()
        self._connection.update_one(
            {"type": "blockchain"},
            {"$set": {"type": "blockchain", "data": dict_blockchain}},
        )

    def get(self) -> BlockChain | None:
        block_chain = self._connection.find_one({"type": "blockchain"})
        if block_chain is None:
            return None
        return BlockChain.from_dict({**block_chain["data"], "id": block_chain["_id"]})

    def build(self, data: dict) -> BlockChain:
        return BlockChain.from_dict(data)
