import time
import random
import copy
import sys
import os

# Thiết lập đường dẫn để Python nhận diện được package sourcecode
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sourcecode.blockchain_dsa import Block, Mempool, Transaction
from sourcecode.blockchain_dsa.test_data import MOCK_10000_TRANSACTIONS, MOCK_4000_TRANSACTIONS
from sourcecode.blockchain_dsa.utils import compute_hash
from sourcecode.blockchain_dsa.merkle_tree import compute_merkle_root
from sourcecode.blockchain_dsa.merkle_utils import get_merkle_proof, verify_merkle_proof

# Ghim seed để dữ liệu đồng nhất
random.seed(42)


def run_unified_tests():
    print("=" * 80)
    print("KIỂM THỬ HỆ THỐNG BLOCKCHAIN DSA".center(80))
    print("=" * 80)

    # -------------------------------------------------------------------------
    # 1. TRANSACTION TEST (Từ test_transaction.py)
    # -------------------------------------------------------------------------
    print("\n[PHẦN 1] KIỂM TRA TRANSACTION & HASHING")
    txids = [tx.txid for tx in MOCK_10000_TRANSACTIONS]
    print(f" - Tổng số giao dịch: {len(txids)}")
    print(f" - Số lượng TXID duy nhất: {len(set(txids))}")
    assert len(txids) == len(set(txids)), "LỖI: Phát hiện trùng lặp TXID!"

    # Test Avalanche Effect
    original_tx = MOCK_10000_TRANSACTIONS[0]
    modified_tx = copy.deepcopy(original_tx)
    modified_tx.fee += 0.00000001
    # Tính lại ID mới dựa trên dữ liệu đã đổi
    new_data = f"{modified_tx.sender}{modified_tx.receiver}{modified_tx.amount}{modified_tx.fee}{modified_tx.timestamp}"
    new_txid = compute_hash(new_data)
    assert original_tx.txid != new_txid, "LỖI: Hash không đổi khi dữ liệu đổi!"
    print(" => Kết quả: [PASS] Transaction ID duy nhất và bảo mật.")

    # -------------------------------------------------------------------------
    # 2. MEMPOOL & BLOCK INIT (Từ test_block.py)
    # -------------------------------------------------------------------------
    print("\n[PHẦN 2] KIỂM TRA MEMPOOL & KHỞI TẠO BLOCK")
    mempool = Mempool()
    mempool.add_transactions_bulk(MOCK_4000_TRANSACTIONS)

    start_time = time.perf_counter()
    mempool.sort_by_fee()  # Sắp xếp theo phí để lấy top
    top_txs = mempool.get_top_transactions(4000)
    block = Block(top_txs)
    block.finalize()
    duration = time.perf_counter() - start_time

    print(f" - Số lượng TX trong Block: {len(block.transactions)}")
    print(f" - Thời gian Init + Finalize (4000 TXs): {duration:.6f}s")
    assert len(block.transactions) == 4000
    print(" => Kết quả: [PASS] Đóng gói Block thành công.")

    # -------------------------------------------------------------------------
    # 3. BINARY SEARCH TEST
    # -------------------------------------------------------------------------
    print("\n[PHẦN 3] KIỂM TRA BINARY SEARCH (Dùng block.search_by_txid)")
    target_tx = block.transactions[1234]
    target_id = target_tx.txid

    start_search = time.perf_counter()
    result_tx = block.search_by_txid(target_id)
    duration_search = time.perf_counter() - start_search

    print(f" - Đang tìm TXID: {target_id}")
    assert result_tx is not None and result_tx.txid == target_id
    print(f" - Kết quả: Tìm thấy đúng giao dịch.")
    print(f" - Thời gian tìm kiếm: {duration_search:.10f}s")
    print(" => Kết quả: [PASS] Binary Search hoạt động chính xác.")

    # -------------------------------------------------------------------------
    # 4. MERKLE TREE & PROOF (Từ test.proof.py)
    # -------------------------------------------------------------------------
    print("\n[PHẦN 4] KIỂM TRA MERKLE ROOT & BẰNG CHỨNG XÁC THỰC")
    root = block.merkle_root
    test_id = block.transactions[500].txid

    # Tạo bằng chứng và xác minh
    proof = get_merkle_proof(block.transactions, test_id)
    is_valid = verify_merkle_proof(test_id, proof, root)

    print(f" - Merkle Root: {root}")
    print(f" - Xác minh Proof (Index 500): {'Thành công' if is_valid else 'Thất bại'}")
    assert is_valid, "LỖI: Merkle Proof không hợp lệ!"
    print(" => Kết quả: [PASS] Hệ thống Merkle hoạt động đúng.")

    # -------------------------------------------------------------------------
    # 5. CACHE & VIEW (Kiểm tra tính cố định của dữ liệu)
    # -------------------------------------------------------------------------
    print("\n[PHẦN 5] KIỂM TRA CACHE & TÍNH CỐ ĐỊNH CỦA DỮ LIỆU")

    # Lần 1: Hệ thống sẽ thực hiện sắp xếp (QuickSort) và lưu vào Cache
    t1_start = time.perf_counter()
    res1 = block.get_view_by_fee_desc(page=1, per_page=5)  # Lấy 5 cái thôi cho dễ nhìn
    t1 = time.perf_counter() - t1_start

    # Lần 2: Hệ thống lấy thẳng từ Dictionary _cached_views
    t2_start = time.perf_counter()
    res2 = block.get_view_by_fee_desc(page=1, per_page=5)
    t2 = time.perf_counter() - t2_start

    print(f" - Thời gian Lần 1 (Sắp xếp): {t1:.6f}s")
    print(f" - Thời gian Lần 2 (Cache):   {t2:.6f}s")

    # --- PHẦN IN RA ĐỂ SO SÁNH ---
    print("\n👉 SO SÁNH DỮ LIỆU GIỮA 2 LẦN CHẠY:")
    print(f"{'STT':<5} | {'TXID Lần 1 (Sắp xếp)':<35} | {'TXID Lần 2 (Từ Cache)':<35}")
    print("-" * 80)

    for i in range(len(res1['data'])):
        id1 = res1['data'][i].txid[:30] + "..."  # Rút gọn ID cho dễ nhìn table
        id2 = res2['data'][i].txid[:30] + "..."
        print(f"{i + 1:<5} | {id1:<35} | {id2:<35}")

    # Kiểm tra bằng code (Deep comparison)
    is_identical = all(res1['data'][i].txid == res2['data'][i].txid for i in range(len(res1['data'])))

    if is_identical:
        print("\n✅ XÁC NHẬN: Giao dịch hoàn toàn cố định và chính xác giữa các lần truy xuất!")
    else:
        print("\n❌ CẢNH BÁO: Dữ liệu bị sai lệch giữa 2 lần chạy!")

    assert t2 <= t1
    assert is_identical
    print(" => Kết quả: [PASS] Cache và View hoạt động tối ưu.")

if __name__ == "__main__":
    try:
        run_unified_tests()
    except Exception as e:
        print(f"\n❌ DỪNG TEST DO LỖI: {e}")