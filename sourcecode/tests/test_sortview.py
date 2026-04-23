import time
import random
from sourcecode.blockchain_dsa import Block
from sourcecode.blockchain_dsa.test_data import MOCK_4000_TRANSACTIONS
random.seed(42)

print("\n--- TEST CACHE & PAGINATION ---\n")

block = Block(MOCK_4000_TRANSACTIONS)

views = [
    ("Fee DESC", block.get_view_by_fee_desc),
    ("Fee ASC", block.get_view_by_fee_asc),
    ("Time DESC", block.get_view_by_time_desc),
    ("Time ASC", block.get_view_by_time_asc),
]

for name, view_func in views:
    # Lần 1: Sort
    start = time.perf_counter()
    result = view_func(page=1, per_page=10)
    time1 = time.perf_counter() - start

    # Lần 2: Cache
    start = time.perf_counter()
    result_cache = view_func(page=1, per_page=10)
    time2 = time.perf_counter() - start

    print(f"[{name}]")
    print(f"  Lần 1 (sort): {time1:.6f}s")
    print(f"  Lần 2 (cache): {time2:.6f}s")
    print(f"  Trang: {result['page']}/{result['total_pages']}")
    print(f"  Kết quả: {len(result['data'])} txs\n")

    # In chi tiết 10 giao dịch
    print(f"  PAGE 1:")
    for i, tx in enumerate(result['data'], 1):
        print(f"    {i}. ID={tx.txid}, Fee={tx.fee:.6f}, Amount={tx.amount:.2f}")

    # Lấy trang tiếp theo (page 2)
    result_page2 = view_func(page=2, per_page=10)
    print(f"\n  PAGE 2:")
    for i, tx in enumerate(result_page2['data'], 1):
        print(f"    {i}. ID={tx.txid}, Fee={tx.fee:.6f}, Amount={tx.amount:.2f}")

    print()

print("✅ Pass!")
