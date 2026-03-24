def sort_transactions_for_block(arr):
    """
    Hàm sắp xếp toàn bộ giao dịch trong Mempool để chuẩn bị đóng gói vào Block.
    """

    # Sử dụng hàm .sort() mặc định của Python (thuật toán lõi là Timsort).
    # Hàm chạy trực tiếp trên mảng gốc (In-place), không tốn thêm dung lượng RAM.Có tính ổn định, không làm xáo trộn các giao dịch bị trùng phí.
    """
    Giải thích tham số key=lambda:
    Lambda là một hàm ẩn danh dùng để chỉ định tiêu chí sắp xếp.
    Mình truyền vào một tuple gồm 2 điều kiện: (-tx.fee, tx.timestamp)
     Điều kiện 1 (-tx.fee): Dấu trừ (-) giúp sắp xếp mức Phí từ CAO XUỐNG THẤP.
     Điều kiện 2 (tx.timestamp): Nếu 2 giao dịch có phí bằng nhau, máy tính tự động
    nhìn sang điều kiện 2 để xếp Thời gian từ CŨ ĐẾN MỚI (ai tới trước được ưu tiên).
    """
    arr.sort(key=lambda tx: (-tx.fee, tx.timestamp))