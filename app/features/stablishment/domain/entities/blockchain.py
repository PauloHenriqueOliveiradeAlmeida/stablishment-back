import hashlib
import time
import json

class Block:
    def __init__(self, index, timestamp, data, previous_hash, hash, nonce):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = hash
        self.nonce = nonce

class BlockChain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
        self.difficulty = 6

    def is_valid_proof(self, hash, difficulty):
      return hash[:difficulty] == '0'*difficulty

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0", self.calculate_hash(0, time.time(), "Genesis Block", "0", 0), 0)
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def calculate_hash(self, index, timestamp, data, previous_hash, nonce):
        value = str(index) + str(timestamp) + str(data) + str(previous_hash) + str(nonce)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def mine_block(self, data):
        previous_block = self.get_last_block()
        index = previous_block.index + 1
        timestamp = time.time()
        previous_hash = previous_block.hash
        nonce = 0
        hash = self.calculate_hash(index, timestamp, data, previous_hash, nonce)
        while not self.is_valid_proof(hash, self.difficulty):
            nonce += 1
            hash = self.calculate_hash(index, timestamp, data, previous_hash, nonce)
        return Block(index, timestamp, data, previous_hash, hash, nonce)

    def add_block(self, block):
        if self.is_valid_new_block(block, self.get_last_block()):
          self.chain.append(block)

    def is_valid_new_block(self, new_block, previous_block):
      if previous_block.index + 1 != new_block.index:
        return False
      elif previous_block.hash != new_block.previous_hash:
          return False
      elif self.calculate_hash(new_block.index, new_block.timestamp, new_block.data, new_block.previous_hash, new_block.nonce) != new_block.hash:
        return False
      elif not self.is_valid_proof(new_block.hash, self.difficulty):
        return False
      return True
    
    def is_chain_valid(self):
      for i in range(1, len(self.chain)):
        current_block = self.chain[i]
        previous_block = self.chain[i-1]
        if not self.is_valid_new_block(current_block, previous_block):
          return False
      return True
    
    def get_block_by_establishment_id(self, establishment_id):
      for block in self.chain:
        try:
          data = json.loads(block.data)
          if data.get("establishment_id") == establishment_id:
            return block
        except json.JSONDecodeError:
          pass
      return None