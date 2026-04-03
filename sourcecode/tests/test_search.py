"""
Test Binary Search trên TXID

Bao gồm:
1. Trường hợp tìm thấy
2. Trường hợp không tìm thấy
3. Đo thời gian sort và search
"""

import time
from blockchain_dsa.utils import generate_mock_transactions
from blockchain_dsa.block import Block
from blockchain_dsa.search import sort_transactions_by_txid, binary_search_txid

def test_search_found():
    # Tạo dữ liệu giả
    txs = generate_mock_transactions(2000)

    # Tạo block (block đã có sẵn, không sửa)
    block = Block(txs)

    # Lấy danh sách transaction từ block
    transactions = block.transactions


    # BƯỚC 1: SORT THEO TXID

    start_sort = time.time()

    sorted_txs = sort_transactions_by_txid(transactions)

    end_sort = time.time()

    # Lấy một TXID có thật trong danh sách
    target_txid = sorted_txs[500].txid

    # BƯỚC 2: BINARY SEARCH

    start_search = time.time()

    result = binary_search_txid(sorted_txs, target_txid)

    end_search = time.time()

    print("[SEARCH FOUND]")
    print("TXID cần tìm:", target_txid[:10], "...")
    print("Kết quả:", result)
    print("Thời gian sort:", end_sort - start_sort)
    print("Thời gian search:", end_search - start_search)

    # Kiểm tra kết quả đúng
    assert result is not None
    assert result.txid == target_txid


def test_search_not_found():
    # Tạo dữ liệu
    txs = generate_mock_transactions(2000)
    block = Block(txs)

    transactions = block.transactions

    # Sort trước khi search
    sorted_txs = sort_transactions_by_txid(transactions)

    # TXID giả (không tồn tại)
    fake_txid = "0" * 64

    start = time.time()

    result = binary_search_txid(sorted_txs, fake_txid)

    end = time.time()

    print("[SEARCH NOT FOUND]")
    print("TXID giả:", fake_txid)
    print("Kết quả:", result)
    print("Thời gian search:", end - start)

    # Kết quả phải là None
    assert result is None