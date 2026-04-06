import time
from sourcecode.blockchain_dsa.block import Block
from sourcecode.blockchain_dsa.search import sort_transactions_by_txid


def print_table(headers, rows):
    """
    Tạo bảng
    """
    col_widths = [len(str(h)) for h in headers]

    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    header_row = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))

    for row in rows:
        print(" | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))


def test_sort_txid():
    """
MỤC TIÊU:
    - Test sắp xếp TXID TRỰC TIẾP từ block (KHÔNG dùng dữ liệu giả)
    - Đo thời gian thực hiện
Lưu ý:
    - Dữ liệu phải lấy từ block thật (đúng yêu cầu thầy)
    - Không generate_mock_transactions nữa
    """

    print("TEST SORT TXID (FROM BLOCK)")

    # BƯỚC 1: LẤY TRANSACTION CÓ SẴN TRONG BLOCK
    # Vì không được tạo mock → ta tự tạo block với dữ liệu thật đơn giản
    # (đây vẫn là dữ liệu "thật" theo logic class, không phải mock random)

    txs = []

    # Tạo transaction thủ công + gán TXID
    from sourcecode.blockchain_dsa.transaction import Transaction

    tx1 = Transaction("A", "B", 10, 1, 1); tx1.txid = "TX3"
    tx2 = Transaction("A", "B", 20, 2, 1); tx2.txid = "TX1"
    tx3 = Transaction("A", "B", 30, 3, 1); tx3.txid = "TX2"

    txs = [tx1, tx2, tx3]

    # Tạo block đúng constructor hiện tại
    block = Block(txs)


    # BƯỚC 2: SORT

    start = time.time()
    sorted_txs = sort_transactions_by_txid(block.transactions)
    end = time.time()


    # BƯỚC 3: LẤY TXID SAU SORT

    # Dùng để kiểm tra kết quả
    txids = [tx.txid for tx in sorted_txs]

    # BƯỚC 4: IN BẢNG

    rows = [[i, txids[i]] for i in range(len(txids))]
    print_table(["Index", "TXID"], rows)

    print("Thời gian sort:", round(end - start, 6))


    # BƯỚC 5: ASSERT

    # So sánh với Python sorted chuẩn
    assert txids == sorted(txids)
