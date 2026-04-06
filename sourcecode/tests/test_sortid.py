import time
from sourcecode.blockchain_dsa.block import Block
from sourcecode.blockchain_dsa.utils import generate_mock_transactions
from sourcecode.blockchain_dsa.search import sort_transactions_by_txid


def test_sort_txid():
    print("\n===== TEST SORT TXID =====")


    # BƯỚC 1: LẤY DATA THỰC

    txs = generate_mock_transactions(1000)

    block = Block(txs)


    # BƯỚC 2: SORT

    start = time.time()
    sorted_txs = sort_transactions_by_txid(block.transactions)
    end = time.time()

    txids = [tx.txid for tx in sorted_txs]


    # BƯỚC 3: CHECK ĐÚNG

    assert txids == sorted(txids)

    print("5 TXID đầu:", txids[:5])
    print("Thời gian:", round(end - start, 6))