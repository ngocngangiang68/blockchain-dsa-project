def binary_search(transactions, target_txid):
    """
    Binary Search tìm transaction theo TXID
    Yêu cầu: transactions phải đã sort theo ID
    Độ phức tạp: O(log n)
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

    return None  # Không tìm thấy