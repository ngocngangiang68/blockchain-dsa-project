import time
from sourcecode.blockchain_dsa.block import Block
from sourcecode.blockchain_dsa.utils import generate_mock_transactions
from sourcecode.blockchain_dsa.search import sort_transactions_by_txid, binary_search_txid


def test_search_found():
    print("\n===== TEST SEARCH FOUND =====")


    # BƯỚC 1: LẤY DỮ LIỆU

    txs = generate_mock_transactions(1000)
    block = Block(txs)

    # BƯỚC 2: SORT

    sorted_txs = sort_transactions_by_txid(block.transactions)

    # Lấy TXID có thật
    target_txid = sorted_txs[100].txid


    # BƯỚC 3: SEARCH

    result = binary_search_txid(sorted_txs, target_txid)

    print("Target:", target_txid)
    print("Found :", result.txid if result else None)

    assert result is not None
    assert result.txid == target_txid


def test_search_not_found():
    print("\n===== TEST SEARCH NOT FOUND =====")

    txs = generate_mock_transactions(1000)
    block = Block(txs)

    sorted_txs = sort_transactions_by_txid(block.transactions)

    fake_txid = "NOT_EXIST_TXID"

    result = binary_search_txid(sorted_txs, fake_txid)

    print("Search:", fake_txid)
    print("Result:", result)

    assert result is None


def test_performance_search():
    print("\n===== TEST PERFORMANCE =====")

    txs = generate_mock_transactions(2000)
    block = Block(txs)

    # SORT
    start_sort = time.time()
    sorted_txs = sort_transactions_by_txid(block.transactions)
    end_sort = time.time()

    target_txid = sorted_txs[500].txid

    # SEARCH
    start_search = time.time()
    result = binary_search_txid(sorted_txs, target_txid)
    end_search = time.time()

    print("Sort time  :", round(end_sort - start_sort, 6))
    print("Search time:", round(end_search - start_search, 6))

    assert result is not None