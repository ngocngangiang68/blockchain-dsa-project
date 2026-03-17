import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time# dung do tg thuc thi
from transaction import Transaction #lay lop Transaction de tao doi tuong giao dich
from utils import generate_mock_transactions, compute_hash #lay ham tao du lieu mau va ham bam de kiem tra


def test_nhiem_vu_1():
    print("=== KIỂM TRA  ===")

    # 1. Test tính duy nhất (Mục tiêu: TXID định danh duy nhất) [cite: 21]
    print("\n1. Đang tạo 10.000 giao dịch mẫu...")
    start_time = time.time()
    mempool = generate_mock_transactions(10000)
    end_time = time.time()

    ids = [tx.txid for tx in mempool]
    is_unique = len(ids) == len(set(ids))
    print(f"- Tạo 10.000 giao dịch mất: {end_time - start_time:.4f}s")  # Mục tiêu < 0.05s [cite: 69]
    print(f"- Tính duy nhất của TXID: {'Thành công' if is_unique else 'Thất bại'}")

    # 2. Test Avalanche Effect (Đảm bảo nếu nội dung thay đổi 1 bit, TXID thay đổi hoàn toàn) [cite: 63]
    print("\n2. Kiểm tra thay đổi nội dung giao dịch:")
    tx_root = Transaction("Alice", "Bob", 100, 0.01)

    # Tạo bản sao nhưng đổi nhẹ số tiền
    tx_modified = Transaction("Alice", "Bob", 100.0000001, 0.01)
    tx_modified.timestamp = tx_root.timestamp

    # Tính lại hash để so sánh
    data_new = f"{tx_modified.sender}{tx_modified.receiver}{tx_modified.amount}{tx_modified.fee}{tx_modified.timestamp}"
    tx_modified.txid = compute_hash(data_new)

    print(f"- TXID gốc: {tx_root.txid}")
    print(f"- TXID đã sửa: {tx_modified.txid}")

    if tx_root.txid != tx_modified.txid:
        print("=> KẾT LUẬN: TXID thay đổi hoàn toàn (ĐẠT).")


if __name__ == "__main__":
    test_nhiem_vu_1()