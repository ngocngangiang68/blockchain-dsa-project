"""
Test việc sắp xếp transaction theo TXID

Mục tiêu:
- Kiểm tra sắp xếp đúng
- Đo thời gian thực hiện
"""

import time
from blockchain_dsa.utils import generate_mock_transactions
from blockchain_dsa.search import sort_transactions_by_txid


def test_sort_txid():
    # Tạo 1000 transaction giả lập
    txs = generate_mock_transactions(1000)

    # Bắt đầu đo thời gian
    start = time.time()

    # Gọi hàm sắp xếp
    sorted_txs = sort_transactions_by_txid(txs)

    # Kết thúc đo thời gian
    end = time.time()

    # Lấy danh sách TXID sau khi sort
    txids = [tx.txid for tx in sorted_txs]

    # Kiểm tra xem danh sách đã được sắp xếp đúng chưa
    assert txids == sorted(txids)

    print("[TEST SORT TXID]")
    print("5 TXID đầu:", txids[:5])
    print("Thời gian sắp xếp:", end - start)