# not final
from sourcecode.blockchain_dsa.utils import generate_mock_transactions
from sourcecode.blockchain_dsa.mempool import Mempool
from sourcecode.blockchain_dsa.block import Block

# 1. Generate mock transactions (random)
transactions = generate_mock_transactions(n=10000)

# 2. Nạp vào mempool
mempool = Mempool()
mempool.add_transactions_bulk(transactions)
mempool.sort_by_fee()

# 3. Tạo block
block = Block.create_from_mempool(mempool)

# 4. Đóng gói
block.finalize()


def print_transactions(txs, label, limit=10):
    """In ra transactions với giới hạn số lượng"""
    print(f"\n{label}:")
    for i, tx in enumerate(txs[:limit]):
        print(f"  {i + 1}. {tx}")
    if len(txs) > limit:
        print(f"  ... và {len(txs) - limit} giao dịch khác")


# 5. Xem các view
print_transactions(block.get_view_by_fee_desc(), "View theo phí (cao → thấp)")
print_transactions(block.get_view_by_time_desc(), "View theo timestamp (mới → cũ)")

# 6. Binary search
result = block.search_by_txid(transactions[0].txid)
print("Tìm thấy:", result)
#test pull request