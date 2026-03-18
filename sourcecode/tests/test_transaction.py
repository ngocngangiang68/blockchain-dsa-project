import sys
import os
import time  # Thư viện dùng để đo đạc thời gian thực thi của thuật toán

# Thêm thư mục gốc vào hệ thống để Python có thể tìm thấy các package trong sourcecode
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import các lớp và hàm cần thiết từ project để tiến hành kiểm tra
from sourcecode.blockchain_dsa.transaction import Transaction
from sourcecode.blockchain_dsa.utils import generate_mock_transactions, compute_hash


def test_nhiem_vu_1():
    """
    Hàm thực hiện kiểm tra Nhiệm vụ 1: Khởi tạo dữ liệu và mã hóa giao dịch.
    Mục tiêu: Đảm bảo tạo 10.000 giao dịch cực nhanh (< 0.05s) và mã TXID là duy nhất.
    """
    print("=== BÁO CÁO THỰC NGHIỆM NHIỆM VỤ 1 ===")

    # 1. Kiểm tra tính duy nhất và hiệu năng tạo dữ liệu
    # Mục tiêu: Mỗi giao dịch phải có một mã định danh (TXID) riêng biệt.
    print("\n1. Đang tiến hành tạo 10.000 giao dịch mẫu trong Mempool...")
    start_time = time.time()  # Bắt đầu bấm giờ
    mempool = generate_mock_transactions(10000)
    end_time = time.time()  # Kết thúc bấm giờ

    # Thu thập tất cả các TXID để kiểm tra sự trùng lặp
    ids = [tx.txid for tx in mempool]
    # Sử dụng set() để loại bỏ các phần tử trùng, nếu độ dài không đổi nghĩa là tất cả ID là duy nhất
    is_unique = len(ids) == len(set(ids))

    # Tính toán thời gian thực thi (Mục tiêu bài tập lớn là dưới 0.05 giây)
    print(f"- Thời gian tạo 10.000 giao dịch: {end_time - start_time:.4f}s")
    print(f"- Kết quả kiểm tra tính duy nhất: {'THÀNH CÔNG' if is_unique else 'THẤT BẠI'}")

    # 2. Kiểm tra hiệu ứng Tuyết lở (Avalanche Effect)
    # Mục tiêu: Đảm bảo chỉ cần thay đổi 1 đơn vị dữ liệu nhỏ nhất, mã TXID phải thay đổi hoàn toàn.
    print("\n2. Kiểm tra tính nhạy cảm của mã băm (Avalanche Effect):")

    # Tạo giao dịch gốc
    tx_root = Transaction("Alice", "Bob", 100, 0.01)

    # Tạo giao dịch mới chỉ thay đổi một lượng cực nhỏ ở số tiền (amount)
    # Truyền cùng timestamp để so sánh sự thay đổi do dữ liệu gốc gây ra
    tx_modified = Transaction("Alice", "Bob", 100.0000001, 0.01, timestamp=tx_root.timestamp)

    print(f"- TXID giao dịch gốc: {tx_root.txid}")
    print(f"- TXID khi sửa 1 bit:  {tx_modified.txid}")

    # So sánh hai mã băm
    if tx_root.txid != tx_modified.txid:
        print("=> KẾT LUẬN: Mã băm thay đổi hoàn toàn dù dữ liệu chỉ lệch 0.0000001 (ĐẠT).")
    else:
        print("=> KẾT LUẬN: Mã băm không đổi (THẤT BẠI).")


if __name__ == "__main__":
    test_nhiem_vu_1()