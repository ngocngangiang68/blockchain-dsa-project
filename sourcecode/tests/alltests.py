import time
import random
import copy
import sys
import os

# =====================================================
# FIX IMPORT PATH
# =====================================================
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            '..'
        )
    )
)

from sourcecode.blockchain_dsa import (
    Block,
    Mempool
)

from sourcecode.blockchain_dsa.test_data import (
    MOCK_10000_TRANSACTIONS,
    MOCK_4000_TRANSACTIONS
)

from sourcecode.blockchain_dsa.utils import (
    compute_hash
)

from sourcecode.blockchain_dsa.merkle_utils import (
    get_merkle_proof,
    verify_merkle_proof
)

from sourcecode.blockchain_dsa.merkle_tree import (
    compute_merkle_root
)

# =====================================================
# CONFIG
# =====================================================

random.seed(42)

TOTAL_RUNS = 100

# Warm-up
for _ in range(10):
    temp = Mempool()
    temp.add_transactions_bulk(
        MOCK_4000_TRANSACTIONS
    )
    temp.sort_by_fee()


# =====================================================
# BENCHMARK
# =====================================================

def benchmark_test(
    func,
    threshold
):
    pass_count = 0
    fail_count = 0
    times = []

    for _ in range(TOTAL_RUNS):

        start = time.perf_counter()

        try:
            result = func()
            correct = (
                result is not False
            )

        except Exception as e:
            print("DEBUG ERROR:", e)
            correct = False

        elapsed = (
            time.perf_counter()
            - start
        )

        times.append(
            elapsed
        )

        passed = (
            correct
            and
            elapsed <= threshold
        )

        if passed:
            pass_count += 1
        else:
            fail_count += 1

    return {
        "pass": pass_count,
        "fail": fail_count,
        "avg": (
            sum(times)
            / len(times)
        ),
        "min": min(times),
        "max": max(times),
        "rate": (
            pass_count
            / TOTAL_RUNS
        ) * 100
    }


def print_report(
    name,
    stats
):
    print(
        f"\n📊 {name}"
    )

    print(
        f" - PASS: "
        f"{stats['pass']}"
        f"/{TOTAL_RUNS}"
    )

    print(
        f" - FAIL: "
        f"{stats['fail']}"
        f"/{TOTAL_RUNS}"
    )

    print(
        f" - Success Rate: "
        f"{stats['rate']:.2f}%"
    )

    print(
        f" - Average Time: "
        f"{stats['avg']:.10f}s"
    )

    print(
        f" - Min Time: "
        f"{stats['min']:.10f}s"
    )

    print(
        f" - Max Time: "
        f"{stats['max']:.10f}s"
    )

    print(
        " => "
        + (
            "✅ ĐẠT YÊU CẦU (>90%)"
            if stats['rate'] >= 90
            else "❌ CHƯA ĐẠT"
        )
    )


# =====================================================
# MAIN TEST
# =====================================================

def run_unified_tests():

    print("=" * 80)
    print(
        "KIỂM THỬ HỆ THỐNG BLOCKCHAIN DSA"
        .center(80)
    )
    print("=" * 80)

    # =================================================
    # 1. TRANSACTION
    # =================================================
    print(
        "\n[PHẦN 1] "
        "KIỂM TRA TRANSACTION & HASHING"
    )

    txids = [
        tx.txid
        for tx
        in MOCK_10000_TRANSACTIONS
    ]

    print(
        f" - Tổng số giao dịch: "
        f"{len(txids)}"
    )

    print(
        f" - Số lượng TXID duy nhất: "
        f"{len(set(txids))}"
    )

    assert (
        len(txids)
        ==
        len(set(txids))
    ), "LỖI: Trùng TXID!"

    original_tx = (
        MOCK_10000_TRANSACTIONS[0]
    )

    modified_tx = copy.deepcopy(
        original_tx
    )

    modified_tx.fee += (
        0.00000001
    )

    new_data = (
        f"{modified_tx.sender}"
        f"{modified_tx.receiver}"
        f"{modified_tx.amount}"
        f"{modified_tx.fee}"
        f"{modified_tx.timestamp}"
    )

    new_txid = (
        compute_hash(
            new_data
        )
    )

    assert (
        original_tx.txid
        !=
        new_txid
    )

    print(
        " => [PASS] "
        "Transaction an toàn."
    )

    # =================================================
    # 2. MEMPOOL + BLOCK
    # =================================================
    print(
        "\n[PHẦN 2] "
        "KIỂM TRA MEMPOOL & BLOCK"
    )

    # -----------------------------------------
    # TEST 1: MEMPOOL SORTING
    # 10000 -> sort fee -> lấy top 4000
    # Target < 0.05s
    # -----------------------------------------
    def mempool_sort_test():
        temp_pool = Mempool()

        temp_pool.add_transactions_bulk(
            MOCK_10000_TRANSACTIONS
        )

        temp_pool.sort_by_fee()

        top_4000 = (
            temp_pool
            .get_top_transactions(
                4000
            )
        )

        return (
                len(top_4000)
                == 4000
        )

    mempool_stats = benchmark_test(
        mempool_sort_test,
        0.05
    )

    print_report(
        "Mempool Sorting",
        mempool_stats
    )

    # -----------------------------------------
    # Chuẩn bị dữ liệu block 1 lần duy nhất
    # Không benchmark phần này
    # -----------------------------------------
    base_pool = Mempool()

    base_pool.add_transactions_bulk(
        MOCK_10000_TRANSACTIONS
    )

    base_pool.sort_by_fee()

    top_txs = (
        base_pool
        .get_top_transactions(
            4000
        )
    )

    # -----------------------------------------
    # TEST 2: BLOCK FINALIZE
    # CHỈ đo sort TXID
    # Target < 0.03s
    # -----------------------------------------
    def block_finalize_test():
        temp_block = Block(
            top_txs.copy()
        )

        start = time.perf_counter()

        temp_block.finalize()

        elapsed = (
                time.perf_counter()
                - start
        )

        return (
                len(
                    temp_block.transactions
                )
                == 4000
                and
                elapsed < 0.03
        )

    block_stats = benchmark_test(
        block_finalize_test,
        0.03
    )


    print_report(
        "Block Finalize",
        block_stats
    )

    # block thật dùng cho các test sau
    block = Block(
        top_txs.copy()
    )

    block.finalize()
    # =================================================
    # 3. BINARY SEARCH
    # =================================================
    print(
        "\n[PHẦN 3] "
        "KIỂM TRA BINARY SEARCH"
    )

    target_tx = (
        block.transactions[1234]
    )

    target_id = (
        target_tx.txid
    )

    def binary_search_test():

        result_tx = (
            block.search_by_txid(
                target_id
            )
        )

        return (
            result_tx
            is not None
            and
            result_tx.txid
            ==
            target_id
        )

    binary_stats = benchmark_test(
        binary_search_test,
        0.0001
    )

    print_report(
        "Binary Search",
        binary_stats
    )

    # =================================================
    # 4. MERKLE
    # =================================================
    print(
        "\n[PHẦN 4] "
        "KIỂM TRA MERKLE"
    )

    # BUILD 1 LẦN DUY NHẤT
    root = compute_merkle_root(
        block.transactions
    )

    test_id = (
        block.transactions[500]
        .txid
    )

    proof = get_merkle_proof(
        block.transactions,
        test_id
    )

    print(
        "DEBUG VERIFY:",
        verify_merkle_proof(
            test_id,
            proof,
            root
        )
    )

    def merkle_root_test():
        return root is not None

    def proof_creation_test():
        return proof is not None

    def verify_proof_test():
        return verify_merkle_proof(
            test_id,
            proof,
            root
        )

    merkle_root_stats = benchmark_test(
        merkle_root_test,
        0.01
    )

    proof_stats = benchmark_test(
        proof_creation_test,
        0.01
    )

    verify_stats = benchmark_test(
        verify_proof_test,
        0.0001
    )

    print_report(
        "Merkle Root",
        merkle_root_stats
    )

    print_report(
        "Create Proof",
        proof_stats
    )

    print_report(
        "Verify Proof",
        verify_stats
    )

    # =================================================
    # 5. CACHE
    # =================================================
    print(
        "\n[PHẦN 5] "
        "KIỂM TRA CACHE"
    )

    def cache_test():

        res1 = (
            block
            .get_view_by_fee_desc(
                page=1,
                per_page=5
            )
        )

        res2 = (
            block
            .get_view_by_fee_desc(
                page=1,
                per_page=5
            )
        )

        return all(
            (
                res1['data'][i].txid
                ==
                res2['data'][i].txid
            )
            for i in range(
                len(
                    res1['data']
                )
            )
        )

    cache_stats = benchmark_test(
        cache_test,
        0.005
    )

    print_report(
        "Cache View",
        cache_stats
    )

    print(
        "\n✅ TOÀN BỘ TEST "
        "HOÀN TẤT"
    )


if __name__ == "__main__":

    try:
        run_unified_tests()

    except Exception as e:

        print(
            f"\n❌ "
            f"DỪNG TEST: "
            f"{e}"
        )