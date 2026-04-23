import time
import random
import copy
from sourcecode.blockchain_dsa import Block, Mempool
from sourcecode.blockchain_dsa.test_data import MOCK_10000_TRANSACTIONS, MOCK_4000_TRANSACTIONS
from sourcecode.blockchain_dsa.utils import compute_hash
from sourcecode.blockchain_dsa.merkle_tree import MerkleTree, compute_merkle_root
from sourcecode.blockchain_dsa.merkle_utils import get_merkle_proof, verify_merkle_proof

random.seed(42)

# ============================================================================
# PHẦN 1: CHUẨN BỊ - SETUP MEMPOOL & TRANSACTIONS
# ============================================================================
print("\n" + "="*70)
print("PHẦN 1: CHUẨN BỊ - SETUP MEMPOOL & TRANSACTIONS")
print("="*70 + "\n")

# Nạp Mempool
mempool = Mempool()
mempool.add_transactions_bulk(MOCK_4000_TRANSACTIONS)
mempool.sort_by_fee()

# Lấy top 4000
top_4000 = mempool.get_top_transactions(4000)
print(f"✅ Mempool được khởi tạo với {len(top_4000)} giao dịch")

# ============================================================================
# PHẦN 2: KIỂM TRA GIAO DỊC - TRANSACTION HASHING & UNIQUENESS
# ============================================================================
print("\n" + "="*70)
print("PHẦN 2: KIỂM TRA GIAO DỊC - TRANSACTION HASHING & UNIQUENESS")
print("="*70 + "\n")

print("--- KIỂM TRA TÍNH DUY NHẤT VÀ HIỆU NĂNG HASH ---")

# 1. Kiểm tra tính duy nhất (Uniqueness)
txids = [tx.txid for tx in MOCK_10000_TRANSACTIONS]
unique_txids = set(txids)

print(f"Tổng số giao dịch: {len(txids)}")
print(f"Số lượng TXID duy nhất: {len(unique_txids)}")

if len(txids) == len(unique_txids):
    print("=> Kết quả: Tất cả TXID đều duy nhất. [PASS]")
else:
    print("=> Kết quả: Phát hiện trùng lặp TXID! [FAIL]")

# 2. Kiểm tra hiệu năng (Performance)
start_time = time.perf_counter()
for tx in MOCK_10000_TRANSACTIONS:
    _ = compute_hash(str(tx.__dict__))
duration = time.perf_counter() - start_time

print(f"Thời gian băm 10,000 giao dịch: {duration:.4f} giây")
print(f"Trung bình: {duration / 10000:.8f} giây/hash\n")

# 3. Kiểm tra hiệu ứng lan tỏa (Avalanche Effect)
print("--- KIỂM TRA HIỆU ỨNG LAN TỎA (AVALANCHE EFFECT) ---")

original_tx = MOCK_10000_TRANSACTIONS[0]
original_txid = original_tx.txid

modified_tx = copy.deepcopy(original_tx)
modified_tx.fee += 0.00000001

new_txid = compute_hash(str(modified_tx.__dict__))

print(f"Giao dịch gốc ID:  {original_txid}")
print(f"Giao dịch chỉnh sửa: {new_txid}")

diff_chars = sum(1 for a, b in zip(original_txid, new_txid) if a != b)

print(f"Sự thay đổi dữ liệu: Fee tăng 0.00000001")
print(f"Số ký tự khác biệt trong mã Hash: {diff_chars} / {len(original_txid)}")

if original_txid != new_txid and diff_chars > (len(original_txid) // 2):
    print("=> Kết quả: Mã TXID thay đổi hoàn toàn (Avalanche Effect). [PASS]\n")
else:
    print("=> Kết quả: Mã TXID không thay đổi đủ lớn. [FAIL]\n")

# ============================================================================
# PHẦN 3: KHỞI TẠO BLOCK - BLOCK INITIALIZATION & FINALIZATION
# ============================================================================
print("="*70)
print("PHẦN 3: KHỞI TẠO BLOCK - BLOCK INITIALIZATION & FINALIZATION")
print("="*70 + "\n")

start = time.perf_counter()
block = Block(top_4000)
block.finalize()
duration = time.perf_counter() - start

print(f"⏱️  Block init + finalize: {duration:.6f}s")

assert len(block.transactions) == 4000
assert duration < 0.08

print("✅ Pass!\n")

# ============================================================================
# PHẦN 4: MERKLE TREE - BUILD & VERIFY
# ============================================================================
print("="*70)
print("PHẦN 4: MERKLE TREE - BUILD & VERIFY")
print("="*70 + "\n")

transactions = [f"tx{i}" for i in range(4000)]

start = time.time()
tree = MerkleTree(transactions)
root = tree.get_root()
t_build = time.time() - start
print(f"[1] Build Root:   {t_build:.6f}s | < 0.01s: {'✅' if t_build < 0.01 else '❌'}")

start = time.time()
proof = tree.get_proof(transactions[0])
t_proof = time.time() - start
print(f"[2] Create Proof: {t_proof:.6f}s")

start = time.time()
ok = MerkleTree.verify_proof(transactions[0], proof, root)
t_verify = time.perf_counter() - start
print(f"[3] Verify Proof: {t_verify:.8f}s | Result: {'✅' if ok else '❌'}\n")

assert ok

# ============================================================================
# PHẦN 5: PROOF & SECURITY - MERKLE PROOF VERIFICATION WITH BLOCK
# ============================================================================
print("="*70)
print("PHẦN 5: PROOF & SECURITY - MERKLE PROOF VERIFICATION WITH BLOCK")
print("="*70 + "\n")

block = Block(MOCK_4000_TRANSACTIONS)
txs = block.transactions
target_id = txs[500].txid

print(f"--- KIỂM THỬ HIỆU NĂNG & BẢO MẬT (4000 TXs) ---")

t1 = time.perf_counter()
root = compute_merkle_root(txs)
t_build = time.perf_counter() - t1

t2 = time.perf_counter()
proof = get_merkle_proof(txs, target_id)
t_proof = time.perf_counter() - t2

t3 = time.perf_counter()
is_valid = verify_merkle_proof(target_id, proof, root)
t_verify = time.perf_counter() - t3

print(f"[1] Build Root:   {t_build:.6f}s | < 0.01s: {'✅' if t_build < 0.01 else '❌'}")
print(f"[2] Create Proof: {t_proof:.6f}s")
print(f"[3] Verify Proof: {t_verify:.8f}s")

print(f"\n--- KIỂM TRA TOÀN VẸN ---")
malicious_txs = copy.deepcopy(txs)
malicious_txs[1000].txid = compute_hash(malicious_txs[1000].txid + "malicious")
new_root = compute_merkle_root(malicious_txs)

is_rejected = not verify_merkle_proof(compute_hash(target_id + "fake"), proof, root)

print(f"[*] Avalanche Effect: {'✅' if root != new_root else '❌'}")
print(f"[*] Chặn giả mạo:     {'✅' if is_rejected else '❌'}\n")

# ============================================================================
# PHẦN 6: TÌM KIẾM - BINARY SEARCH
# ============================================================================
print("="*70)
print("PHẦN 6: TÌM KIẾM - BINARY SEARCH (ACCURACY & PERFORMANCE)")
print("="*70 + "\n")

block = Block(MOCK_4000_TRANSACTIONS)

target_tx = MOCK_4000_TRANSACTIONS[1234]
target_id = target_tx.txid

start_time = time.perf_counter()
result_tx = block.search_by_txid(target_id)
duration_exist = time.perf_counter() - start_time

print(f"[Case 1: TXID tồn tại]")
print(f"  - Đang tìm: {target_id}")
if result_tx is not None and result_tx.txid == target_id:
    print(f"  - Kết quả: Tìm thấy đối tượng giao dịch [PASS]")
else:
    print(f"  - Kết quả: Thất bại [FAIL]")
print(f"  - Thời gian xử lý: {duration_exist:.10f} giây")

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

avg_speed = (duration_exist + duration_not_found) / 2
print(f"\n=> Tốc độ trung bình mỗi lượt Binary Search: {avg_speed:.10f} giây\n")

# ============================================================================
# PHẦN 7: CACHE & PAGINATION - SORT VIEWS
# ============================================================================
print("="*70)
print("PHẦN 7: CACHE & PAGINATION - SORT VIEWS")
print("="*70 + "\n")

print("--- TEST CACHE & PAGINATION ---\n")

block = Block(MOCK_4000_TRANSACTIONS)

views = [
    ("Fee DESC", block.get_view_by_fee_desc),
    ("Fee ASC", block.get_view_by_fee_asc),
    ("Time DESC", block.get_view_by_time_desc),
    ("Time ASC", block.get_view_by_time_asc),
]

for name, view_func in views:
    start = time.perf_counter()
    result = view_func(page=1, per_page=10)
    time1 = time.perf_counter() - start

    start = time.perf_counter()
    result_cache = view_func(page=1, per_page=10)
    time2 = time.perf_counter() - start

    print(f"[{name}]")
    print(f"  Lần 1 (sort): {time1:.6f}s")
    print(f"  Lần 2 (cache): {time2:.6f}s")
    print(f"  Trang: {result['page']}/{result['total_pages']}")
    print(f"  Kết quả: {len(result['data'])} txs\n")

    print(f"  PAGE 1:")
    for i, tx in enumerate(result['data'], 1):
        print(f"    {i}. ID={tx.txid}, Fee={tx.fee:.6f}, Amount={tx.amount:.2f}")

    result_page2 = view_func(page=2, per_page=10)
    print(f"\n  PAGE 2:")
    for i, tx in enumerate(result_page2['data'], 1):
        print(f"    {i}. ID={tx.txid}, Fee={tx.fee:.6f}, Amount={tx.amount:.2f}")

    print()

print("="*70)
print("✅ TẤT CẢ CÁC TEST HOÀN TẤT THÀNH CÔNG!")
print("="*70 + "\n")