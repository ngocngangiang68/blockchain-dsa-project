import time
from sourcecode.blockchain_dsa.transaction import Transaction
from sourcecode.blockchain_dsa.block import Block
from sourcecode.blockchain_dsa.utils import generate_mock_transactions
from sourcecode.blockchain_dsa.search import sort_transactions_by_txid, binary_search_txid

# HÀM IN BẢNG
def print_table(headers, rows):
    """
In dữ liệu dạng bảng đẹp
    headers: danh sách tiêu đề cột
    rows: danh sách các dòng dữ liệu
Cách hoạt động:
    - Tính độ rộng lớn nhất của từng cột
    - Dùng ljust() để căn trái cho đều
    """

    # Bước 1: lấy độ dài ban đầu từ header
    col_widths = [len(str(h)) for h in headers]

    # Bước 2: duyệt từng dòng để tìm độ dài lớn nhất cho mỗi cột
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    # Bước 3: in header
    header_row = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_row)

    # In dòng phân cách
    print("-" * len(header_row))

    # Bước 4: in dữ liệu từng dòng
    for row in rows:
        print(" | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))


# TEST 1: SEARCH FOUND

def test_search_found():
    print(" TEST SEARCH FOUND ")

    # BƯỚC 1: TẠO DỮ LIỆU NHỎ

    # Vì class Transaction không có txid trong constructor
    # → ta phải gán thủ công sau khi tạo
    tx1 = Transaction("A", "B", 10, 1, 1); tx1.txid = "TX1"
    tx2 = Transaction("A", "B", 20, 2, 1); tx2.txid = "TX2"
    tx3 = Transaction("A", "B", 30, 3, 1); tx3.txid = "TX3"

    # Tạo block chứa transactions
    block = Block([tx1, tx2, tx3])


    # BƯỚC 2: SORT (BẮT BUỘC TRƯỚC KHI SEARCH)

    # Binary Search chỉ hoạt động đúng khi dữ liệu đã được sắp xếp
    sorted_txs = sort_transactions_by_txid(block.transactions)

    # BƯỚC 3: IN DANH SÁCH SAU KHI SORT

    rows = [[i, tx.txid] for i, tx in enumerate(sorted_txs)]
    print_table(["Index", "TXID"], rows)

    # BƯỚC 4: SEARCH

    result = binary_search_txid(sorted_txs, "TX2")

    # BƯỚC 5: IN KẾT QUẢ

    print("KẾT QUẢ SEARCH:")
    print_table(
        ["Target TXID", "Found"],
        [["TX2", result.txid if result else None]]
    )

    # BƯỚC 6: KIỂM TRA ĐÚNG

    assert result is not None
    assert result.txid == "TX2"


# TEST 2: SEARCH NOT FOUND

def test_search_not_found():
    print("TEST SEARCH NOT FOUND")

    # Tạo dữ liệu nhỏ
    tx1 = Transaction("A", "B", 10, 1, 1); tx1.txid = "TX1"
    tx2 = Transaction("A", "B", 20, 2, 1); tx2.txid = "TX2"

    block = Block([tx1, tx2])

    # Sort trước
    sorted_txs = sort_transactions_by_txid(block.transactions)


    # SEARCH TXID KHÔNG TỒN TẠI

    result = binary_search_txid(sorted_txs, "TX999")

    # In bảng kết quả
    print_table(
        ["Target TXID", "Result"],
        [["TX999", result]]
    )

    # Kết quả phải là None
    assert result is None



# TEST 3: PERFORMANCE

def test_performance_search():
    print(" TEST PERFORMANCE ")

    # BƯỚC 1: TẠO DỮ LIỆU LỚN

    txs = generate_mock_transactions(2000)

    # Đảm bảo tất cả transaction có txid
    for i, tx in enumerate(txs):
        if not hasattr(tx, "txid"):
            tx.txid = f"TX{i}"

    block = Block(txs)


    # BƯỚC 2: ĐO THỜI GIAN SORT

    # Độ phức tạp: O(n log n)
    start_sort = time.time()
    sorted_txs = sort_transactions_by_txid(block.transactions)
    end_sort = time.time()

    # Lấy 1 TXID có thật để test search
    target_txid = sorted_txs[500].txid


    # BƯỚC 3: ĐO THỜI GIAN SEARCH

    # Độ phức tạp: O(log n)
    start_search = time.time()
    result = binary_search_txid(sorted_txs, target_txid)
    end_search = time.time()


    # BƯỚC 4: IN BẢNG KẾT QUẢ

    print_table(
        ["Metric", "Value"],
        [
            ["Target TXID", target_txid],
            ["Found", result.txid if result else None],
            ["Sort Time (O(n log n))", round(end_sort - start_sort, 6)],
            ["Search Time (O(log n))", round(end_search - start_search, 6)],
        ]
    )


    # BƯỚC 5: KIỂM TRA ĐÚNG

    assert result is not None