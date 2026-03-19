def quick_sort_transactions(arr):
    """
    Thuật toán Quick Sort (Sắp xếp nhanh).
    Nhiệm vụ: Sắp xếp danh sách giao dịch theo phí (fee) từ CAO xuống THẤP.
    """
    # 1. ĐIỀU KIỆN DỪNG:
    # Nếu danh sách chỉ có 1 giao dịch hoặc rỗng, thì không cần sắp xếp nữa, trả về luôn.
    if len(arr) <= 1:
        return arr

    # 2. CHỌN ĐIỂM CHỐT (Pivot):
    # Lấy giao dịch nằm ở vị trí chính giữa danh sách làm mốc để so sánh.
    pivot = arr[len(arr) // 2]

    # 3. PHÂN CHIA DANH SÁCH (Partitioning):
    # Tạo 3 danh sách trống để chứa các giao dịch sau khi so sánh với điểm chốt.
    # Danh sách LEFT: Chứa các giao dịch có phí LỚN HƠN phí của điểm chốt.
    left = [tx for tx in arr if tx.fee > pivot.fee]

    # Danh sách MIDDLE: Chứa các giao dịch có phí BẰNG với phí của điểm chốt.
    middle = [tx for tx in arr if tx.fee == pivot.fee]

    # Danh sách RIGHT: Chứa các giao dịch có phí NHỎ HƠN phí của điểm chốt.
    right = [tx for tx in arr if tx.fee < pivot.fee]

    # 4. ĐỆ QUY VÀ GHÉP NỐI:
    # Tiếp tục lặp lại thuật toán này cho mảng left và right.
    # Sau đó ghép 3 mảng lại với nhau thành một danh sách hoàn chỉnh đã sắp xếp.
    return quick_sort_transactions(left) + middle + quick_sort_transactions(right)