import hashlib# Thư viện cung cấp các thuật toán mã hóa (ở đây dùng SHA256)
import random# Thư viện dùng để tạo dữ liệu ngẫu nhiên (tên, số tiền, phí)
import string # Thư viện chứa các tập ký tự để tạo mã hậu tố cho địa chỉ ví
import time # Thư viện dùng để quản lý và lấy mốc thời gian thực

compute_hash = lambda data: hashlib.sha256(data.encode()).hexdigest() #SHA256. Kết quả trả về một chuỗi ký tự dài 64 ký tự, đóng vai trò là mã định danh (TXID)

def generate_mock_transactions(n=10000):
    """THàm tạo ra danh sách 10.000 giao dịch mẫu để đưa vào Mempool.
    Giúp nhóm có tập dữ liệu lớn để kiểm tra hiệu năng sắp xếp và tìm kiếm."""
    from .transaction import Transaction
    # Import từ package để đảm bảo cấu trúc dự án của nhóm chạy đúng

    transactions = []
    # Danh sách tên cơ sở để làm phong phú dữ liệu người dùng
    base_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Ngoc Anh", "Gia Bao",
                  "Hoang", "Minh", "Phuong", "Lan", "Tu", "Khanh", "Vy", "Hien", "Giang"]
    # Lấy mốc thời gian hiện tại làm gốc để tính toán
    now= time.time()
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
        random_timestamp = now - random.uniform(0, 86400)

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