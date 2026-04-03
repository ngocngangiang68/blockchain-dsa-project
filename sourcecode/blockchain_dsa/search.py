"""
Module search:
- Sắp xếp transaction theo TXID
- Tìm kiếm bằng Binary Search
"""

# ==============================
# 1. SORT TRANSACTIONS
# ==============================

def sort_transactions_by_txid(transactions):
    """
    Sắp xếp transaction theo TXID (tăng dần)
    """
    return sorted(transactions, key=lambda tx: tx.txid)


# ==============================
# 2. BINARY SEARCH
# ==============================

def binary_search_txid(transactions, target_txid):
    """
    Tìm transaction bằng Binary Search theo TXID
    """
    left, right = 0, len(transactions) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_txid = transactions[mid].txid

        if mid_txid == target_txid:
            return transactions[mid]
        elif mid_txid < target_txid:
            left = mid + 1
        else:
            right = mid - 1

    return None


# ==============================
# 3. WRAPPER (CHO TEST)
# ==============================

def prepare_block_for_search(block):
    """
    Lấy transactions từ block và sắp xếp
    """
    return sort_transactions_by_txid(block.transactions)


def binary_search(transactions, target_txid):
    """
    Wrapper cho binary_search_txid
    """
    return binary_search_txid(transactions, target_txid)


def search_transaction(block, target_txid):
    """
    Pipeline đầy đủ: block → sort → search
    """
    sorted_txs = prepare_block_for_search(block)
    return binary_search(sorted_txs, target_txid)