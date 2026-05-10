import time
import random
import copy
import sys
import os
import gc

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sourcecode.blockchain_dsa import Block, Mempool, Transaction
from sourcecode.blockchain_dsa.test_data import MOCK_10000_TRANSACTIONS, MOCK_4000_TRANSACTIONS
from sourcecode.blockchain_dsa.utils import compute_hash
from sourcecode.blockchain_dsa.merkle_tree import compute_merkle_root
from sourcecode.blockchain_dsa.merkle_utils import get_merkle_proof, verify_merkle_proof

random.seed(42)


def run_unified_tests():
    print("=" * 80)
    print("KIỂM THỬ HỆ THỐNG BLOCKCHAIN DSA".center(80))
    print("=" * 80)

    # -------------------------------------------------------------------------
    # 1. TRANSACTION TEST
    # -------------------------------------------------------------------------
    print("\n[PHẦN 1] KIỂM TRA TRANSACTION & HASHING")
    txids = [tx.txid for tx in MOCK_10000_TRANSACTIONS]
    print(f" - Tổng số giao dịch: {len(txids)}")
    print(f" - Số lượng TXID duy nhất: {len(set(txids))}")
    assert len(txids) == len(set(txids)), "LỖI: Phát hiện trùng lặp TXID!"

    original_tx = MOCK_10000_TRANSACTIONS[0]
    modified_tx = copy.deepcopy(original_tx)
    modified_tx.fee += 0.00000001
    new_data = f"{modified_tx.sender}{modified_tx.receiver}{modified_tx.amount}{modified_tx.fee}{modified_tx.timestamp}"
    new_txid = compute_hash(new_data)
    assert original_tx.txid != new_txid, "LỖI: Hash không đổi khi dữ liệu đổi!"
    print(" => Kết quả: [PASS] Transaction ID duy nhất và bảo mật.")

    # -------------------------------------------------------------------------
    # 2. MEMPOOL & BLOCK INIT
    # -------------------------------------------------------------------------
    print("\n[PHẦN 2] KIỂM TRA MEMPOOL & KHỞI TẠO BLOCK")
    mempool = Mempool()
    mempool.add_transactions_bulk(MOCK_4000_TRANSACTIONS)

    start_sort_mempool = time.perf_counter()
    mempool.sort_by_fee()
    t_sort_mempool = time.perf_counter() - start_sort_mempool

    top_txs = mempool.get_top_transactions(4000)

    start_time = time.perf_counter()
    block = Block(top_txs)
    block.finalize()
    duration = time.perf_counter() - start_time

    print(f" - Số lượng TX trong Block: {len(block.transactions)}")
    print(f" - Thời gian Init + Finalize (4000 TXs): {duration:.6f}s")
    print(f" 👉 Sắp xếp Mempool (< 0.05s): {t_sort_mempool:.6f}s -> {'✅ ĐẠT' if t_sort_mempool < 0.05 else '❌ CHƯA ĐẠT'}")
    print(f" 👉 Sắp xếp trong Block (< 0.03s): {duration:.6f}s -> {'✅ ĐẠT' if duration < 0.03 else '❌ CHƯA ĐẠT'}")
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
    print(f" 👉 Binary Search (< 0.0001s): {duration_search:.6f}s -> {'✅ ĐẠT' if duration_search < 0.0001 else '❌ CHƯA ĐẠT'}")
    print(" => Kết quả: [PASS] Binary Search hoạt động chính xác.")

    # -------------------------------------------------------------------------
    # 4. MERKLE TREE & PROOF
    # -------------------------------------------------------------------------
    print("\n[PHẦN 4] KIỂM TRA MERKLE ROOT & BẰNG CHỨNG XÁC THỰC")

    # Xây Merkle Root trực tiếp từ hàm, không qua thuộc tính cache của block
    start_merkle = time.perf_counter()
    root = compute_merkle_root(block.transactions)
    t_merkle_tree = time.perf_counter() - start_merkle

    test_id = block.transactions[500].txid

    start_proof = time.perf_counter()
    proof = get_merkle_proof(block.transactions, test_id)
    t_create_proof = time.perf_counter() - start_proof

    start_verify = time.perf_counter()
    is_valid = verify_merkle_proof(test_id, proof, root)
    t_verify_proof = time.perf_counter() - start_verify

    print(f" - Merkle Root: {root}")
    print(f" - Xác minh Proof (Index 500): {'Thành công' if is_valid else 'Thất bại'}")
    print(f" 👉 Xây dựng Merkle Tree (< 0.01s): {t_merkle_tree:.6f}s -> {'✅ ĐẠT' if t_merkle_tree < 0.01 else '❌ CHƯA ĐẠT'}")
    print(f" 👉 Tạo Merkle Proof (< 0.01s): {t_create_proof:.6f}s -> {'✅ ĐẠT' if t_create_proof < 0.01 else '❌ CHƯA ĐẠT'}")
    print(f" 👉 Xác thực Merkle Proof (< 0.0001s): {t_verify_proof:.6f}s -> {'✅ ĐẠT' if t_verify_proof < 0.0001 else '❌ CHƯA ĐẠT'}")
    assert is_valid, "LỖI: Merkle Proof không hợp lệ!"
    print(" => Kết quả: [PASS] Hệ thống Merkle hoạt động đúng.")

    # -------------------------------------------------------------------------
    # 5. CACHE & VIEW
    # -------------------------------------------------------------------------
    print("\n[PHẦN 5] KIỂM TRA CACHE & TÍNH CỐ ĐỊNH CỦA DỮ LIỆU")

    t1_start = time.perf_counter()
    res1 = block.get_view_by_fee_desc(page=1, per_page=5)
    t1 = time.perf_counter() - t1_start

    t2_start = time.perf_counter()
    res2 = block.get_view_by_fee_desc(page=1, per_page=5)
    t2 = time.perf_counter() - t2_start

    print(f" - Thời gian Lần 1 (Sắp xếp): {t1:.6f}s")
    print(f" - Thời gian Lần 2 (Cache):   {t2:.6f}s")

    print("\n👉 SO SÁNH DỮ LIỆU GIỮA 2 LẦN CHẠY:")
    print(f"{'STT':<5} | {'TXID Lần 1 (Sắp xếp)':<35} | {'TXID Lần 2 (Từ Cache)':<35}")
    print("-" * 80)
    for i in range(len(res1['data'])):
        id1 = res1['data'][i].txid[:30] + "..."
        id2 = res2['data'][i].txid[:30] + "..."
        print(f"{i + 1:<5} | {id1:<35} | {id2:<35}")


    is_identical = all(res1['data'][i].txid == res2['data'][i].txid for i in range(len(res1['data'])))
    if is_identical:
        print("\n✅ XÁC NHẬN: Giao dịch hoàn toàn cố định và chính xác giữa các lần truy xuất!")
    else:
        print("\n❌ CẢNH BÁO: Dữ liệu bị sai lệch giữa 2 lần chạy!")

    assert t2 <= t1
    assert is_identical
    print(" => Kết quả: [PASS] Cache và View hoạt động tối ưu.")


if __name__ == "__main__":

    TOTAL_RUNS = 100
    TOLERANCE = 1.3

    stats = {
        "Transaction & Hashing": [],
        "Mempool Sorting": [],
        "Block Finalize": [],
        "Binary Search": [],
        "Merkle Root": [],
        "Create Proof": [],
        "Verify Proof": [],
    }

    print("\n" + "=" * 80)
    print("KIỂM THỬ HỆ THỐNG BLOCKCHAIN DSA".center(80))
    print("=" * 80)

    print("🔥 Warm-up hệ thống...")
    for _ in range(5):
        _mp = Mempool()
        _mp.add_transactions_bulk(MOCK_4000_TRANSACTIONS)
        _mp.sort_by_fee()
        _txs = _mp.get_top_transactions(4000)
        _blk = Block(_txs)
        _blk.finalize()
        _ = _blk.search_by_txid(_blk.transactions[100].txid)
        _r = compute_merkle_root(_blk.transactions)
        _ = get_merkle_proof(_blk.transactions, _blk.transactions[500].txid)
    print("✅ Warm-up hoàn tất\n")

    gc.disable()

    for run in range(1, TOTAL_RUNS + 1):

        # ---------- 1. Transaction & Hashing ----------
        try:
            txids = [tx.txid for tx in MOCK_10000_TRANSACTIONS]
            original_tx = MOCK_10000_TRANSACTIONS[0]
            modified_tx = copy.deepcopy(original_tx)
            modified_tx.fee += 0.00000001
            new_data = f"{modified_tx.sender}{modified_tx.receiver}{modified_tx.amount}{modified_tx.fee}{modified_tx.timestamp}"
            new_txid = compute_hash(new_data)
            tx_pass = len(txids) == len(set(txids)) and original_tx.txid != new_txid
        except Exception:
            tx_pass = False
        stats["Transaction & Hashing"].append(tx_pass)

        # ---------- 2. Mempool Sorting ----------
        mempool = Mempool()
        mempool.add_transactions_bulk(MOCK_4000_TRANSACTIONS)

        start_sort = time.perf_counter()
        mempool.sort_by_fee()
        t_sort = time.perf_counter() - start_sort
        mempool_pass = t_sort < 0.05 * TOLERANCE
        stats["Mempool Sorting"].append((mempool_pass, t_sort))

        # ---------- 3. Block Finalize ----------
        top_txs = mempool.get_top_transactions(4000)

        start_block = time.perf_counter()
        block = Block(top_txs)
        block.finalize()
        t_block = time.perf_counter() - start_block
        block_pass = t_block < 0.03 * TOLERANCE
        stats["Block Finalize"].append((block_pass, t_block))

        # ---------- 4. Binary Search ----------
        target_tx = block.transactions[1234]

        start_search = time.perf_counter()
        result_tx = block.search_by_txid(target_tx.txid)
        t_search = time.perf_counter() - start_search
        binary_pass = (
            result_tx is not None
            and result_tx.txid == target_tx.txid
            and t_search < 0.0001 * TOLERANCE
        )
        stats["Binary Search"].append((binary_pass, t_search))

        # ---------- 5. Merkle Root (NO cache – gọi compute_merkle_root trực tiếp) ----------
        start_merkle = time.perf_counter()
        root = compute_merkle_root(block.transactions)
        t_merkle = time.perf_counter() - start_merkle
        merkle_root_pass = t_merkle < 0.01 * TOLERANCE
        stats["Merkle Root"].append((merkle_root_pass, t_merkle))

        # ---------- 6. Create Proof ----------
        test_tx = block.transactions[500]

        start_proof = time.perf_counter()
        proof = get_merkle_proof(block.transactions, test_tx.txid)
        t_proof = time.perf_counter() - start_proof
        create_proof_pass = t_proof < 0.01 * TOLERANCE
        stats["Create Proof"].append((create_proof_pass, t_proof))

        # ---------- 7. Verify Proof ----------
        start_verify = time.perf_counter()
        is_valid = verify_merkle_proof(test_tx.txid, proof, root)
        t_verify = time.perf_counter() - start_verify
        verify_pass = is_valid and t_verify < 0.0001 * TOLERANCE
        stats["Verify Proof"].append((verify_pass, t_verify))

    gc.enable()

    # =========================================================
    # IN BÁO CÁO
    # =========================================================
    print("\n[PHẦN 1] KIỂM TRA TRANSACTION & HASHING")
    tx_pass_list = stats["Transaction & Hashing"]
    total_pass = sum(tx_pass_list)
    print(f" - Tổng số giao dịch: 10000")
    print(f" - Số lần PASS: {total_pass}/{TOTAL_RUNS}")
    print(f" - Success Rate: {total_pass / TOTAL_RUNS * 100:.2f}%")
    print(f" => [{'PASS' if total_pass / TOTAL_RUNS > 0.9 else 'FAIL'}] Transaction an toàn.\n")

    section_labels = {
        "Mempool Sorting":  ("PHẦN 2", "KIỂM TRA MEMPOOL SORTING"),
        "Block Finalize":   ("PHẦN 3", "KIỂM TRA BLOCK FINALIZE"),
        "Binary Search":    ("PHẦN 4", "KIỂM TRA BINARY SEARCH"),
        "Merkle Root":      ("PHẦN 5", "KIỂM TRA MERKLE ROOT"),
        "Create Proof":     ("PHẦN 6", "KIỂM TRA TẠO MERKLE PROOF"),
        "Verify Proof":     ("PHẦN 7", "KIỂM TRA XÁC THỰC MERKLE PROOF"),
    }

    for func, (section, label) in section_labels.items():
        results = stats[func]
        passes = sum(r[0] for r in results)
        times = [r[1] for r in results]
        avg_t = sum(times) / len(times)
        min_t = min(times)
        max_t = max(times)
        rate = passes / TOTAL_RUNS

        print(f"[{section}] {label}")
        print(f" - PASS: {passes}/{TOTAL_RUNS}")
        print(f" - FAIL: {TOTAL_RUNS - passes}/{TOTAL_RUNS}")
        print(f" - Success Rate: {rate * 100:.2f}%")
        print(f" - Average Time: {avg_t:.10f}s")
        print(f" - Min Time:     {min_t:.10f}s")
        print(f" - Max Time:     {max_t:.10f}s")
        print(f" => {'✅ ĐẠT YÊU CẦU (>90%)' if rate >= 0.9 else '❌ CHƯA ĐẠT'}\n")

    print("✅ TOÀN BỘ TEST HOÀN TẤT")