"""
Module search
CHỨC NĂNG:
- Sắp xếp transaction theo TXID
- Tìm kiếm transaction bằng Binary Search
LIÊN KẾT HỆ THỐNG:
Mempool → Block → block.transactions → search
Ý tưởng:
- Transaction trong block KHÔNG được sắp xếp theo TXID
- Muốn dùng Binary Search → bắt buộc phải SORT trước
"""
# 1. SORT TRANSACTIONS

def sort_transactions_by_txid(transactions):
    """
MỤC ĐÍCH:
    - Sắp xếp danh sách transaction theo TXID tăng dần
INPUT:
    - transactions: list[Transaction]
OUTPUT:
    - list[Transaction] đã được sắp xếp
GIẢI THÍCH:
    - Sử dụng sorted() của Python (Timsort)
    - Độ phức tạp: O(n log n)
    - key=lambda tx: tx.txid → so sánh theo TXID
QUAN TRỌNG:
    - Đây là bước bắt buộc trước khi dùng Binary Search
    """

    return sorted(transactions, key=lambda tx: tx.txid)

# 2. BINARY SEARCH
def binary_search_txid(transactions, target_txid):
    """
    MỤC ĐÍCH:
    - Tìm transaction theo TXID bằng Binary Search
INPUT:
    - transactions: list đã SORT
    - target_txid: TXID cần tìm
 OUTPUT:
    - Transaction nếu tìm thấy
    - None nếu không tồn tại
ĐỘ PHỨC TẠP:
    - O(log n)
NGUYÊN LÝ:
    - Mỗi lần lặp chia đôi không gian tìm kiếm
    """

    left, right = 0, len(transactions) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_txid = transactions[mid].txid

        # Trường hợp tìm thấy
        if mid_txid == target_txid:
            return transactions[mid]

        # Tìm bên phải
        elif mid_txid < target_txid:
            left = mid + 1

        # Tìm bên trái
        else:
            right = mid - 1

    # Không tìm thấy
    return None


# ==============================
# 3. PIPELINE CHÍNH
# ==============================

def search_transaction(block, target_txid):
    """
MỤC ĐÍCH:
    - Tìm transaction trong block
FLOW:
    Block → transactions → sort → binary search
INPUT:
    - block: Block object
    - target_txid: TXID cần tìm
OUTPUT:
    - Transaction hoặc None
    """

    # Lấy danh sách transaction từ block
    transactions = block.transactions

    # Bước 1: Sort theo TXID
    sorted_txs = sort_transactions_by_txid(transactions)

    # Bước 2: Binary Search
    return binary_search_txid(sorted_txs, target_txid)

def prepare_block_for_search(block):
    """
    Chuẩn bị transaction từ block để search
    (phục vụ import trong __init__.py)
    """

    return sort_transactions_by_txid(block.transactions)

def binary_search(transactions, target_txid):
    """
    Wrapper cho binary_search_txid
    (phục vụ import từ __init__.py)
    """
    return binary_search_txid(transactions, target_txid)