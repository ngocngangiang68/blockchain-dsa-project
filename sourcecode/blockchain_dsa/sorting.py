def merge_sort_transactions(arr, key_func=None, reverse=False):
    """
    Merge Sort tối ưu - O(n log n)
    Tránh tạo quá nhiều list con bằng cách dùng in-place khi có thể
    """
    if len(arr) <= 1:
        return arr

    if len(arr) == 2:
        left_key = key_func(arr[0]) if key_func else arr[0]
        right_key = key_func(arr[1]) if key_func else arr[1]

        if reverse:
            if left_key < right_key:
                return [arr[1], arr[0]]
        else:
            if left_key > right_key:
                return [arr[1], arr[0]]
        return arr[:]

    # Chia đôi
    mid = len(arr) // 2
    left = merge_sort_transactions(arr[:mid], key_func, reverse)
    right = merge_sort_transactions(arr[mid:], key_func, reverse)

    # Gộp lại
    return merge(left, right, key_func, reverse)


def merge(left, right, key_func=None, reverse=False):
    """Hợp nhất 2 danh sách đã sắp xếp - tối ưu"""
    result = []
    i = j = 0

    len_left = len(left)
    len_right = len(right)

    while i < len_left and j < len_right:
        left_key = key_func(left[i]) if key_func else left[i]
        right_key = key_func(right[j]) if key_func else right[j]

        if reverse:
            if left_key >= right_key:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else:
            if left_key <= right_key:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

    # Thêm phần còn lại
    if i < len_left:
        result.extend(left[i:])
    if j < len_right:
        result.extend(right[j:])

    return result


def quick_sort_transactions(arr, key_func=None, reverse=False):
    """
    Quick Sort tối ưu - O(n log n) trung bình
    Dùng 3-way partition
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    pivot_key = key_func(pivot) if key_func else pivot

    left = []
    middle = []
    right = []

    for x in arr:
        x_key = key_func(x) if key_func else x
        if x_key < pivot_key:
            left.append(x)
        elif x_key == pivot_key:
            middle.append(x)
        else:
            right.append(x)

    left = quick_sort_transactions(left, key_func, reverse)
    right = quick_sort_transactions(right, key_func, reverse)

    if reverse:
        return right + middle + left
    else:
        return left + middle + right


def sort_transactions_for_block(arr):
    """
    Sắp xếp transactions theo phí (cao xuống thấp),
    nếu phí bằng nhau thì ưu tiên timestamp (cũ đến mới)
    Dùng Merge Sort (stable sort) - O(n log n)
    """

    def sort_key(tx):
        return (-tx.fee, tx.timestamp)

    return merge_sort_transactions(arr, key_func=sort_key, reverse=False)


def sort_transactions_by_id(arr):
    """
    Sắp xếp transactions theo ID (cố định cho Block)
    O(n log n) - Merge Sort tối ưu
    """
    return merge_sort_transactions(arr, key_func=lambda tx: tx.txid, reverse=False)