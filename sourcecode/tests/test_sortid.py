# tests/test_sortid.py
try:
    # chạy khi đứng trong sourcecode
    from blockchain_dsa import Transaction, Mempool, Block, prepare_block_for_search
except ModuleNotFoundError:
    # chạy khi đứng ở root project
    from sourcecode.blockchain_dsa import Transaction, Mempool, Block, prepare_block_for_search

##
def test_sort_id():
    """
    Test chức năng sắp xếp theo TXID

    Mục tiêu:
    - Kiểm tra xem danh sách sau khi sort có đúng thứ tự không
    Test sắp xếp TXID theo luồng:
        mempool → block → search
        """

    # 1. Tạo mempool
    mempool = Mempool()

    # 2. Tạo dữ liệu
    txs = [
        Transaction("A", "B", 10, 0.1),
        Transaction("C", "D", 20, 0.2),
        Transaction("E", "F", 30, 0.3),
    ]

    # 3. Đưa vào mempool
    mempool.add_transactions_bulk(txs)

    # 4. Sort theo fee (logic blockchain)
    mempool.sort_by_fee()

    # 5. Tạo block
    block = Block.create_from_mempool(mempool)

    # 6. Sort theo TXID
    sorted_txs, sort_time = prepare_block_for_search(block)

    # 7. Kiểm tra số lượng
    assert len(sorted_txs) == len(block.transactions)

    # 8. Kiểm tra sort
    txids = [tx.txid for tx in sorted_txs]
    assert txids == sorted(txids)

    # 9. Kiểm tra từng cặp
    for i in range(len(txids) - 1):
        assert txids[i] <= txids[i + 1]

    print("Sort time:", sort_time)