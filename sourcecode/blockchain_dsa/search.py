# blockchain_dsa/search.py

import time
# Thư viện time dùng để đo thời gian chạy (phục vụ yêu cầu đề bài)


def sort_transactions_by_id(transactions):
    """
    Hàm sắp xếp danh sách giao dịch theo TXID.
    Lưu ý:
    - TXID là chuỗi hash SHA-256 (64 ký tự)
    - sorted() sẽ sắp xếp theo thứ tự từ điển (lexicographic)
    Quan trọng:
    - KHÔNG dùng .sort() vì sẽ làm thay đổi dữ liệu gốc
    - Dùng sorted() để tạo bản sao → đảm bảo Block không bị thay đổi
    Độ phức tạp: O(n log n)
    """
    return sorted(transactions, key=lambda tx: tx.txid)
    # key=lambda tx: tx.txid → tiêu chí sắp xếp là TXID


def binary_search(transactions, target_txid):
    """
    Thuật toán Binary Search để tìm giao dịch theo TXID.
    Điều kiện bắt buộc:
    - Danh sách transactions PHẢI được sort trước theo TXID
    Ý tưởng:
    - So sánh target với phần tử giữa (mid)
    - Nếu nhỏ hơn → tìm bên trái
    - Nếu lớn hơn → tìm bên phải
    Độ phức tạp: O(log n)
    """

    left = 0                      # vị trí đầu danh sách
    right = len(transactions) - 1 # vị trí cuối danh sách

    while left <= right:
        mid = (left + right) // 2   # lấy phần tử giữa

        # So sánh TXID
        if transactions[mid].txid == target_txid:
            return mid  # tìm thấy → trả về vị trí

        elif transactions[mid].txid < target_txid:
            left = mid + 1  # bỏ nửa bên trái

        else:
            right = mid - 1  # bỏ nửa bên phải

    return -1  # không tìm thấy

#
def prepare_block_for_search(block):
    """
    Hàm chuẩn bị dữ liệu từ Block để phục vụ tìm kiếm.
    Bước làm:
    1. Lấy danh sách transactions từ block
    2. Sắp xếp theo TXID
    3. Đo thời gian sắp xếp
    Trả về:
    - sorted_transactions: danh sách đã sắp xếp
    - sort_time: thời gian sắp xếp (giây)
    """

    transactions = block.transactions  # lấy dữ liệu từ Block

    start = time.time()  # bắt đầu đo thời gian

    sorted_transactions = sort_transactions_by_id(transactions)

    end = time.time()  # kết thúc

    sort_time = end - start  # thời gian thực thi

    return sorted_transactions, sort_time


def search_transaction(block, target_txid):
    """
    Hàm thực hiện toàn bộ quy trình tìm kiếm:

    1. Chuẩn bị dữ liệu (sort)
    2. Thực hiện binary search
    3. Đo thời gian

    Trả về:
    - index: vị trí tìm thấy (-1 nếu không có)
    - sort_time: thời gian sắp xếp
    - search_time: thời gian tìm kiếm
    """

    # Bước 1: chuẩn bị dữ liệu
    sorted_txs, sort_time = prepare_block_for_search(block)

    # Bước 2: đo thời gian search
    start = time.time()

    index = binary_search(sorted_txs, target_txid)

    end = time.time()

    search_time = end - start

    return index, sort_time, search_time