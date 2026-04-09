import time
from sourcecode.blockchain_dsa.block import Block
from sourcecode.blockchain_dsa.utils import generate_mock_transactions
from sourcecode.blockchain_dsa.search import sort_transactions_by_txid, binary_search_txid


def test_search_found():
    print("\n===== TEST SEARCH FOUND =====")

    # BƯỚC 1: TẠO DỮ LIỆU CHO BLOCK
    # generate_mock_transactions(1000):
    # → tạo 1000 transaction hợp lệ (có txid, fee, timestamp,...)
    # → dùng để mô phỏng block thực tế
    txs = generate_mock_transactions(1000)

    # Block KHÔNG tự tạo transaction → phải truyền vào
    block = Block(txs)

    # BƯỚC 2: SẮP XẾP THEO TXID
    # Binary Search yêu cầu dữ liệu phải được sắp xếp trước
    sorted_txs = sort_transactions_by_txid(block.transactions)

    # Lấy 1 TXID chắc chắn tồn tại trong danh sách
    target_txid = sorted_txs[100].txid

    # BƯỚC 3: TÌM KIẾM (BINARY SEARCH)

    result = binary_search_txid(sorted_txs, target_txid)

    # In kết quả để kiểm tra trực quan
    print("Target TXID:", target_txid)
    print("Found TXID :", result.txid if result else None)

    # Kiểm tra thuật toán đúng
    assert result is not None
    assert result.txid == target_txid


def test_search_not_found():
    print("\n===== TEST SEARCH NOT FOUND =====")

    # Tạo dữ liệu cho block
    txs = generate_mock_transactions(1000)
    block = Block(txs)

    # Sort trước khi search
    sorted_txs = sort_transactions_by_txid(block.transactions)

    # TXID không tồn tại trong block
    fake_txid = "NOT_EXIST_TXID"

    # Tìm kiếm
    result = binary_search_txid(sorted_txs, fake_txid)

    print("Search TXID:", fake_txid)
    print("Result     :", result)

    # Nếu không tìm thấy → phải trả về None
    assert result is None


def test_performance_search():
    print("\n===== TEST PERFORMANCE =====")

    # BƯỚC 1: TẠO DATA
    # 2000 transaction để test hiệu năng
    txs = generate_mock_transactions(2000)
    block = Block(txs)

    # BƯỚC 2: ĐO THỜI GIAN SORT

    start_sort = time.time()
    sorted_txs = sort_transactions_by_txid(block.transactions)
    end_sort = time.time()

    # Lấy TXID có thật
    target_txid = sorted_txs[500].txid

    # BƯỚC 3: ĐO THỜI GIAN SEARCH

    start_search = time.time()
    result = binary_search_txid(sorted_txs, target_txid)
    end_search = time.time()

    # IN KẾT QUẢ
    print("\n--- PERFORMANCE RESULT ---")
    print("Sort time  (O(n log n)):", round(end_sort - start_sort, 6))
    print("Search time(O(log n)) :", round(end_search - start_search, 6))

    # Kiểm tra đúng
    assert result is not None