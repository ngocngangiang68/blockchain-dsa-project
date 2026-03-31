# tests/test_search.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from blockchain_dsa.transaction import Transaction
from blockchain_dsa.mempool import Mempool
from blockchain_dsa.block import Block
from blockchain_dsa.search import search_transaction

#
def test_search_found():
    """
    Test trường hợp tìm thấy TXID
    """

    # Tạo mempool
    mempool = Mempool()

    # Tạo dữ liệu giao dịch giả
    txs = [
        Transaction("A", "B", 10, 0.5),
        Transaction("C", "D", 20, 0.2),
        Transaction("E", "F", 30, 0.8),
    ]

    # Đưa vào mempool
    mempool.add_transactions_bulk(txs)

    # Sắp xếp theo phí (logic blockchain)
    mempool.sort_by_fee()

    # Tạo block từ mempool
    block = Block.create_from_mempool(mempool)

    # Lấy 1 TXID chắc chắn tồn tại
    target = block.transactions[0].txid

    # Gọi search
    index, sort_time, search_time = search_transaction(block, target)

    print("Sort time:", sort_time)
    print("Search time:", search_time)

    # Kiểm tra tìm thấy
    assert index != -1


def test_search_not_found():
    """
    Test trường hợp KHÔNG tìm thấy TXID
    """

    mempool = Mempool()

    txs = [
        Transaction("A", "B", 10, 0.5),
        Transaction("C", "D", 20, 0.2),
    ]

    mempool.add_transactions_bulk(txs)
    mempool.sort_by_fee()

    block = Block.create_from_mempool(mempool)

    # TXID giả
    index, _, _ = search_transaction(block, "fake_txid_123")

    # Kiểm tra không tìm thấy
    assert index == -1