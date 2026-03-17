# search.py

# Lấy danh sách giao dịch trong block
def get_transactions(block):
    return block["transactions"]


# Sắp xếp giao dịch theo TXID
def sort_transactions_by_id(transactions):
    return sorted(transactions, key=lambda x: x["txid"])


# Binary Search tìm giao dịch theo TXID
def binary_search(transactions, target_txid):

    left = 0
    right = len(transactions) - 1

    while left <= right:

        mid = (left + right) // 2
        mid_txid = transactions[mid]["txid"]

        if mid_txid == target_txid:
            return transactions[mid]

        elif mid_txid < target_txid:
            left = mid + 1

        else:
            right = mid - 1

    return None