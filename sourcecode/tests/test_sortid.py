# tests/test_sortid.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from blockchain_dsa.transaction import Transaction
from blockchain_dsa.block import Block
from blockchain_dsa.search import prepare_block_for_search

##
def test_sort_id():
    """
    Test chức năng sắp xếp theo TXID

    Mục tiêu:
    - Kiểm tra xem danh sách sau khi sort có đúng thứ tự không
    """

    # Tạo dữ liệu giả
    txs = [
        Transaction("A", "B", 10, 0.1),
        Transaction("C", "D", 20, 0.2),
        Transaction("E", "F", 30, 0.3),
    ]

    # Tạo Block
    block = Block(txs)

    # Gọi hàm sort
    sorted_txs, sort_time = prepare_block_for_search(block)

    # Kiểm tra số lượng không đổi
    assert len(sorted_txs) == len(txs)

    # Lấy TXID
    txids = [tx.txid for tx in sorted_txs]

    # Kiểm tra đã được sắp xếp
    assert txids == sorted(txids)

    # Kiểm tra từng cặp (bonus)
    for i in range(len(txids) - 1):
        assert txids[i] <= txids[i + 1]

    print("Sort time:", sort_time)