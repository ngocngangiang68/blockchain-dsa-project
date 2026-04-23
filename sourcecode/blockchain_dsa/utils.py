def generate_mock_transactions(n=10000, base_timestamp=None):
    """THàm tạo ra danh sách 10.000 giao dịch mẫu để đưa vào Mempool.
    Giúp nhóm có tập dữ liệu lớn để kiểm tra hiệu năng sắp xếp và tìm kiếm."""
    from .transaction import Transaction
    # Import từ package để đảm bảo cấu trúc dự án của nhóm chạy đúng

    transactions = []
    # Danh sách tên cơ sở để làm phong phú dữ liệu người dùng
    base_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Ngoc Anh", "Gia Bao",
                  "Hoang", "Minh", "Phuong", "Lan", "Tu", "Khanh", "Vy", "Hien", "Giang"]
    # Nếu không truyền base_timestamp, dùng giá trị cố định
    if base_timestamp is None:
        base_timestamp = 1700000000  # Thời gian cố định (ví dụ: 2023-11-15)
    
    for _ in range(n):

        #Tạo "địa chỉ ví" giả lập bằng cách thêm mã hex ngẫu nhiên
        suffix_sender = ''.join(random.choices(string.hexdigits.lower(), k=4))
        sender = f"{random.choice(base_names)}_{suffix_sender}"

        suffix_receiver = ''.join(random.choices(string.hexdigits.lower(), k=4))
        receiver = f"{random.choice(base_names)}_{suffix_receiver}"

        # Đảm bảo không tự gửi cho chính mình
        while sender == receiver:
            suffix_receiver = ''.join(random.choices(string.hexdigits.lower(), k=4))
            receiver = f"{random.choice(base_names)}_{suffix_receiver}"
        # Tạo mốc thời gian ngẫu nhiên lùi lại trong vòng 24 giờ qua (86400 giây)
        # Điều này giúp thời gian giao dịch thực tế hơn thay vì bị trùng lặp.
        random_timestamp = base_timestamp - random.uniform(0, 86400)

        # Khởi tạo đối tượng Transaction với các thông số đã ngẫu nhiên hóa
        tx = Transaction(
            sender=sender,
            receiver=receiver,
        # Đa dạng hóa số tiền: từ giao dịch nhỏ lẻ đến giao dịch lớn (0.001 đến 500)
            amount=round(random.uniform(0.001, 500.0), 4),
        # Đa dạng hóa phí (fee)
            fee=round(random.uniform(0.00001, 0.1), 8),
            timestamp=random_timestamp,
    )
        transactions.append(tx)
        # Dòng return này nằm ngoài vòng lặp for để trả về đủ n giao dịch
    return transactions
