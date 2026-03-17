import hashlib
import random
import string

def compute_hash(data: str) -> str:
    """Sử dụng SHA256 để định danh duy nhất (TXID)[cite: 21]."""
    return hashlib.sha256(data.encode()).hexdigest()


def generate_mock_transactions(n=10000):
    """Tạo dữ liệu giả lập cho Mempool[cite: 45]."""
    from sourcecode.blockchain_dsa.transaction import Transaction
#tao ra danh sach 10000 giao dich de mo phong

    transactions = []
    base_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Ngoc Anh", "Gia Bao",
                  "Hoang", "Minh", "Phuong", "Lan", "Tu", "Khanh", "Vy", "Hien", "Giang"]
#ds ten nguoi dung gia dinh de lam nguoi nhan va gui
    # Tạo "địa chỉ ví" giả lập bằng cách thêm mã hex ngẫu nhiên (VD: Alice_a1b2)
    suffix_sender = ''.join(random.choices(string.hexdigits.lower(), k=4))
    sender = f"{random.choice(base_names)}_{suffix_sender}"

    suffix_receiver = ''.join(random.choices(string.hexdigits.lower(), k=4))
    receiver = f"{random.choice(base_names)}_{suffix_receiver}"

    # Đảm bảo không tự gửi cho chính mình
    while sender == receiver:
        suffix_receiver = ''.join(random.choices(string.hexdigits.lower(), k=4))
        receiver = f"{random.choice(base_names)}_{suffix_receiver}"

    tx = Transaction(
        sender=sender,
        receiver=receiver,
        # Đa dạng hóa số tiền: từ giao dịch nhỏ lẻ đến giao dịch lớn (0.001 đến 500)
        amount=round(random.uniform(0.001, 500.0), 4),
        # Đa dạng hóa phí (fee)
        fee=round(random.uniform(0.00001, 0.1), 8)
    )
    transactions.append(tx)
    return transactions