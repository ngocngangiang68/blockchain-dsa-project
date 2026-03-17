import hashlib
import random


def compute_hash(data: str) -> str:
    """Sử dụng SHA256 để định danh duy nhất (TXID)[cite: 21]."""
    return hashlib.sha256(data.encode()).hexdigest()


def generate_mock_transactions(n=10000):
    """Tạo dữ liệu giả lập cho Mempool[cite: 45]."""
    from transaction import Transaction
#tao ra danh sach 10000 giao dich de mo phong

    transactions = []
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Ngoc Anh", "Gia Bao"]
#ds ten nguoi dung gia dinh de lam nguoi nhan va gui
    for _ in range(n):
        tx = Transaction(
            sender=random.choice(names),
            receiver=random.choice(names),
            amount=round(random.uniform(0.1, 50.0), 2),
            fee=round(random.uniform(0.0001, 0.01), 6)
        )
        transactions.append(tx)
    return transactions