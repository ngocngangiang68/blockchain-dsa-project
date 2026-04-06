import time
from sourcecode.blockchain_dsa.transaction import Transaction
from sourcecode.blockchain_dsa.block import Block
from sourcecode.blockchain_dsa.search import sort_transactions_by_txid, binary_search_txid


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



# TEST 1: SEARCH FOUND
def test_search_found():
    """
    Test tìm thấy TXID TRONG BLOCK
    """

    print("TEST SEARCH FOUND (FROM BLOCK)")

    # Tạo transaction thật
    tx1 = Transaction("A", "B", 10, 1, 1); tx1.txid = "TX1"
    tx2 = Transaction("A", "B", 20, 2, 1); tx2.txid = "TX2"
    tx3 = Transaction("A", "B", 30, 3, 1); tx3.txid = "TX3"

    block = Block([tx1, tx2, tx3])

    # Sort trước (điều kiện của Binary Search)
    sorted_txs = sort_transactions_by_txid(block.transactions)

    # In dữ liệu block
    print_table(
        ["Index", "TXID"],
        [[i, tx.txid] for i, tx in enumerate(sorted_txs)]
    )

    # Search TXID có tồn tại
    result = binary_search_txid(sorted_txs, "TX2")

    print("\nKẾT QUẢ:")
    print_table(
        ["Target", "Found"],
        [["TX2", result.txid if result else None]]
    )

    assert result is not None
    assert result.txid == "TX2"

# TEST 2: SEARCH NOT FOUND

def test_search_not_found():
    """
    Test không tìm thấy TXID trong block
    """

    print("TEST SEARCH NOT FOUND")

    tx1 = Transaction("A", "B", 10, 1, 1); tx1.txid = "TX1"
    tx2 = Transaction("A", "B", 20, 2, 1); tx2.txid = "TX2"

    block = Block([tx1, tx2])

    sorted_txs = sort_transactions_by_txid(block.transactions)

    result = binary_search_txid(sorted_txs, "TX999")

    print_table(
        ["Target", "Result"],
        [["TX999", result]]
    )

    assert result is None



# TEST 3: PERFORMANCE

def test_performance_search():
    """
    Test hiệu năng (trên block tự tạo, không mock random)
    """

    print("TEST PERFORMANCE")

    # Tạo nhiều transaction thủ công (không dùng mock)
    txs = []
    for i in range(1000):
        tx = Transaction("A", "B", i, i, 1)
        tx.txid = f"TX{i}"
        txs.append(tx)

    block = Block(txs)

    # ĐO SORT
    start_sort = time.time()
    sorted_txs = sort_transactions_by_txid(block.transactions)
    end_sort = time.time()

    target_txid = sorted_txs[500].txid

    # ĐO SEARCH
    start_search = time.time()
    result = binary_search_txid(sorted_txs, target_txid)
    end_search = time.time()

    print_table(
        ["Metric", "Value"],
        [
            ["Target TXID", target_txid],
            ["Found", result.txid if result else None],
            ["Sort Time", round(end_sort - start_sort, 6)],
            ["Search Time", round(end_search - start_search, 6)],
        ]
    )

    assert result is not None