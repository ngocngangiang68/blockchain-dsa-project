from .block import Block

class Blockchain:
    def __init__(self):
        # Danh sách các block trong chuỗi
        self.chain = []
        # Tạo block gốc (genesis block)
        genesis_block = Block(index=0, transactions=[], prev_hash="0")
        self.chain.append(genesis_block)

    def add_block(self, block):
        self.chain.append(block)

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].previous_hash != self.chain[i-1].hash:
                return False
        return True

    def search_transaction(self, txid):
        for block in self.chain:
            for tx in block.transactions:
                if tx.txid == txid:
                    return tx
        return None


    def __init__(self):
        self.chain = []

    def total_transactions(self):
        return sum(len(block.transactions) for block in self.chain)

    def avg_fee(self):
        fees = [tx.fee for block in self.chain for tx in block.transactions]
        return sum(fees)/len(fees) if fees else None
