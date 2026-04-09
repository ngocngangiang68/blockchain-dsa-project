import time
from sourcecode.blockchain_dsa.block import Block
from sourcecode.blockchain_dsa.test_data import MOCK_4000_TRANSACTIONS

print("--- KIỂM TRA BINARY SEARCH (ACCURACY & PERFORMANCE) ---")

# Khởi tạo block (đã tự động gọi sort_transactions_by_id) [cite: 4]
block = Block(MOCK_4000_TRANSACTIONS)

# 1. Kiểm tra tìm kiếm TXID CÓ tồn tại
target_tx = MOCK_4000_TRANSACTIONS[1234]
target_id = target_tx.txid

start_time = time.perf_counter()
# Hàm search_by_txid trả về đối tượng Transaction hoặc None [cite: 19, 20]
result_tx = block.search_by_txid(target_id)
duration_exist = time.perf_counter() - start_time

print(f"\n[Case 1: TXID tồn tại]")
print(f"  - Đang tìm: {target_id}")
if result_tx is not None and result_tx.txid == target_id:
    print(f"  - Kết quả: Tìm thấy đối tượng giao dịch [PASS]")
else:
    print(f"  - Kết quả: Thất bại [FAIL]")
print(f"  - Thời gian xử lý: {duration_exist:.10f} giây")

# 2. Kiểm tra tìm kiếm TXID KHÔNG tồn tại
fake_id = "tx_non_existent_99999"

start_time = time.perf_counter()
result_none = block.search_by_txid(fake_id)
duration_not_found = time.perf_counter() - start_time

print(f"\n[Case 2: TXID không tồn tại]")
print(f"  - Đang tìm: {fake_id}")
if result_none is None:
    print(f"  - Kết quả: Trả về None chính xác [PASS]")
else:
    print(f"  - Kết quả: Sai (không trả về None) [FAIL]")
print(f"  - Thời gian xử lý: {duration_not_found:.10f} giây")

# 3. Hiệu năng trung bình
avg_speed = (duration_exist + duration_not_found) / 2
print(f"\n=> Tốc độ trung bình mỗi lượt Binary Search: {avg_speed:.10f} giây")