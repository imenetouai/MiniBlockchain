import hashlib
import time

# ---------- 1. Classe Block ----------
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    # ---------- 2. Fonction de hash ----------
    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    # ---------- 4. Proof-of-Work ----------
    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block {self.index} miné : {self.hash}")

# ---------- 3. Classe Blockchain ----------
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4   

    def create_genesis_block(self):
        return Block(0, time.ctime(), "Block Génésis", "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        prev_block = self.get_last_block()
        new_block = Block(len(self.chain), time.ctime(), data, prev_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    # ---------- 5. Validation ----------
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                print(f"Block {current.index} invalide : hash incorrect")
                return False

            if current.previous_hash != previous.hash:
                print(f"Block {current.index} invalide : previous_hash incorrect")
                return False

            if current.hash[:self.difficulty] != "0" * self.difficulty:
                print(f"Block {current.index} invalide : difficulté non respectée")
                return False
        return True

# ---------- Test rapide ----------
if __name__ == "__main__":
    ma_blockchain = Blockchain()
    ma_blockchain.add_block("Transaction 1: Alice -> Bob 50")
    ma_blockchain.add_block("Transaction 2: Bob -> Charlie 20")

    print("\nValidation de la blockchain :", ma_blockchain.is_chain_valid())

    # Modification pour tester l'invalidation
    ma_blockchain.chain[1].data = "Transaction 1: Alice -> Bob 5000"
    print("\nAprès modification, validation :", ma_blockchain.is_chain_valid())
