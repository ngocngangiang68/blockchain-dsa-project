import time
from sourcecode.blockchain_dsa.block import Block
from sourcecode.blockchain_dsa.mempool import Mempool
from sourcecode.blockchain_dsa.search import sort_transactions_by_txid, binary_search_txid


def test_search_found():
    print("\n===== TEST SEARCH FOUND =====")

    # BƯỚC 1: TẠO MEMPOOL (PHÒNG CHỜ GIAO DỊCH)
    mempool = Mempool()
    # Tạo 1 mempool rỗng (giống nơi user gửi giao dịch vào)
    # mempool sẽ chứa nhiều transaction do user tạo ra
    # Ở đây ta chỉ giữ pipeline đúng (không tạo dữ liệu giả)

    # BƯỚC 2: TẠO BLOCK TỪ MEMPOOL
    block = Block.create_from_mempool(mempool)
    # Lấy top transaction từ mempool → đưa vào block
    # Block là nơi chứa dữ liệu để test

    # BƯỚC 3: SORT TRANSACTION THEO TXID

    sorted_txs = sort_transactions_by_txid(block.transactions)
    # Binary Search yêu cầu dữ liệu phải được sắp xếp trước
    # Nên phải sort trước khi search

    # BƯỚC 4: LẤY TXID CÓ THẬT ĐỂ TEST
    if len(sorted_txs) == 0:
        print("Không có dữ liệu để test")
        return

    target_txid = sorted_txs[0].txid
    # Lấy TXID đầu tiên

    # BƯỚC 5: TÌM KIẾM (BINARY SEARCH)
    result = binary_search_txid(sorted_txs, target_txid)
    # Thuật toán sẽ chia đôi danh sách để tìm nhanh

    # IN KẾT QUẢ
    print("Target:", target_txid)
    print("Found :", result.txid if result else None)

    # KIỂM TRA KẾT QUẢ
    assert result is not None
    # 👉 Phải tìm thấy

    assert result.txid == target_txid
    # 👉 Và phải đúng TXID


def test_search_not_found():
    print("\n===== TEST SEARCH NOT FOUND =====")

    # TẠO BLOCK
    mempool = Mempool()
    block = Block.create_from_mempool(mempool)

    sorted_txs = sort_transactions_by_txid(block.transactions)

    # TẠO TXID KHÔNG TỒN TẠI
    fake_txid = "NOT_EXIST_TXID"

    # SEARCH
    result = binary_search_txid(sorted_txs, fake_txid)

    print("Search:", fake_txid)
    print("Result:", result)

    # KIỂM TRA
    assert result is None
    # Không tồn tại → phải trả về None


def test_performance_search():
    print("\n===== TEST PERFORMANCE =====")

    # TẠO BLOCK
    mempool = Mempool()
    block = Block.create_from_mempool(mempool)

    # ĐO THỜI GIAN SORT
    start_sort = time.time()
    sorted_txs = sort_transactions_by_txid(block.transactions)
    end_sort = time.time()

    # Thời gian sort = end - start
    # Độ phức tạp: O(n log n)

    if len(sorted_txs) == 0:
        print("Không có dữ liệu để test")
        return

    target_txid = sorted_txs[len(sorted_txs)//2].txid
    # Lấy phần tử giữa để test search

    # ĐO THỜI GIAN SEARCH
    start_search = time.time()
    result = binary_search_txid(sorted_txs, target_txid)
    end_search = time.time()
    # Độ phức tạp search: O(log n)

    # IN KẾT QUẢ
    print("Sort time  :", round(end_sort - start_sort, 6))
    print("Search time:", round(end_search - start_search, 6))

    # KIỂM TRA
    assert result is not None