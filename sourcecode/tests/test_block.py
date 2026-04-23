import time
import random
from sourcecode.blockchain_dsa import Block, Mempool
from sourcecode.blockchain_dsa.test_data import MOCK_4000_TRANSACTIONS

random.seed(42)  # Ghim seed để đảm bảo dữ liệu nhất quán

# Nạp Mempool
mempool = Mempool()
mempool.add_transactions_bulk(MOCK_4000_TRANSACTIONS)
mempool.sort_by_fee()

# Lấy top 4000
top_4000 = mempool.get_top_transactions(4000)

# Đo thời gian
start = time.perf_counter()
block = Block(top_4000)
block.finalize()
duration = time.perf_counter() - start

print(f"\n⏱️  Block init + finalize: {duration:.6f}s")

# Kiểm tra
assert len(block.transactions) == 4000
assert duration < 0.08

print("✅ Pass!")
