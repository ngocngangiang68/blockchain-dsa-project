import time
from sourcecode.blockchain_dsa.utils import generate_mock_transactions
from sourcecode.blockchain_dsa.block import Block
from sourcecode.blockchain_dsa.search import sort_transactions_by_txid


def print_table(headers, rows):
    """
Hàm in bảng dữ liệu đẹp trong terminal

    headers: danh sách tên cột
    rows: danh sách các dòng dữ liệu
Ý tưởng:
    - Tính độ rộng lớn nhất của từng cột
    - Căn lề (ljust) để các cột thẳng hàng
    """

    # Bước 1: Lấy độ dài ban đầu từ header
    col_widths = [len(str(h)) for h in headers]

    # Bước 2: Cập nhật độ rộng theo dữ liệu trong từng dòng
    for row in rows:
        for i, cell in enumerate(row):
            # Lấy độ dài lớn nhất giữa header và dữ liệu
            col_widths[i] = max(col_widths[i], len(str(cell)))

    # Bước 3: In header
    header_row = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_row)

    # In dòng phân cách
    print("-" * len(header_row))

    # Bước 4: In từng dòng dữ liệu
    for row in rows:
        print(" | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))


def test_sort_txid():
    """
    MỤC TIÊU:
    - Kiểm tra việc sắp xếp transaction theo TXID
    - Đo thời gian thực hiện (hiệu năng)
Quy trình:
    1. Tạo dữ liệu giả (1000 transactions)
    2. Đảm bảo mỗi transaction có txid
    3. Đưa vào block
    4. Sắp xếp theo TXID
    5. Kiểm tra đúng
    6. In kết quả dạng bảng
    """

    print("TEST SORT TXID")

    # BƯỚC 1: TẠO DỮ LIỆU
    # generate_mock_transactions tạo ra danh sách transaction giả
    txs = generate_mock_transactions(1000)

    # BƯỚC 2: ĐẢM BẢO CÓ TXID

    # Vì Binary Search và Sort đều dựa vào txid
    # nên cần đảm bảo mỗi transaction có thuộc tính này
    for i, tx in enumerate(txs):
        if not hasattr(tx, "txid"):
            tx.txid = f"TX{i}"   # Gán TXID dạng TX0, TX1, TX2,...

    # BƯỚC 3: TẠO BLOCK

    # Block của project chỉ nhận danh sách transactions
    block = Block(txs)

    # BƯỚC 4: ĐO THỜI GIAN SORT

    start = time.time()

    # Gọi hàm sort theo TXID (tăng dần)
    sorted_txs = sort_transactions_by_txid(block.transactions)

    end = time.time()

    # BƯỚC 5: LẤY DANH SÁCH TXID

    # Dùng để kiểm tra kết quả sau khi sort
    txids = [tx.txid for tx in sorted_txs]

    # BƯỚC 6: IN BẢNG (10 PHẦN TỬ ĐẦU)

    # Giúp dễ quan sát kết quả
    rows = [[i, txids[i]] for i in range(10)]

    print_table(["Index", "TXID"], rows)

    # BƯỚC 7: IN THỜI GIAN

    print("Thời gian sort:", round(end - start, 6))

    # BƯỚC 8: KIỂM TRA ĐÚNG
    # So sánh với kết quả sort chuẩn của Python
    assert txids == sorted(txids)