import time
import copy
from sourcecode.blockchain_dsa.test_data import MOCK_10000_TRANSACTIONS
from sourcecode.blockchain_dsa.utils import compute_hash


def test_transaction_hashing():
    print("--- KIỂM TRA TÍNH DUY NHẤT VÀ HIỆU NĂNG HASH ---")

    # 1. Kiểm tra tính duy nhất (Uniqueness)
    txids = [tx.txid for tx in MOCK_10000_TRANSACTIONS]
    unique_txids = set(txids)

    print(f"Tổng số giao dịch: {len(txids)}")
    print(f"Số lượng TXID duy nhất: {len(unique_txids)}")

    if len(txids) == len(unique_txids):
        print("=> Kết quả: Tất cả TXID đều duy nhất. [PASS]")
    else:
        print("=> Kết quả: Phát hiện trùng lặp TXID! [FAIL]")

    # 2. Kiểm tra hiệu năng (Performance)
    start_time = time.perf_counter()
    # GIẢ LẬP việc băm lại toàn bộ 10.000 txid
    for tx in MOCK_10000_TRANSACTIONS:
        _ = compute_hash(str(tx.__dict__))
    duration = time.perf_counter() - start_time

    print(f"Thời gian băm 10,000 giao dịch: {duration:.4f} giây")
    print(f"Trung bình: {duration / 10000:.8f} giây/hash\n")


def test_avalanche_effect():
    print("--- KIỂM TRA HIỆU ỨNG LAN TỎA (AVALANCHE EFFECT) ---")

    # Lấy một giao dịch mẫu
    original_tx = MOCK_10000_TRANSACTIONS[0]
    original_txid = original_tx.txid

    # Tạo bản sao và thay đổi 1 đơn vị nhỏ nhất (ví dụ: cộng thêm 1 đơn vị phí rất nhỏ)
    modified_tx = copy.deepcopy(original_tx)
    modified_tx.fee += 0.00000001  # Thay đổi cực nhỏ

    # Trong logic của bạn, TXID thường được tính từ hash của nội dung tx
    # Giả sử hàm tạo TXID dùng compute_hash trên dữ liệu giao dịch
    new_txid = compute_hash(str(modified_tx.__dict__))

    print(f"Giao dịch gốc ID:  {original_txid}")
    print(f"Giao dịch chỉnh sửa: {new_txid}")

    # So sánh sự khác biệt
    diff_chars = sum(1 for a, b in zip(original_txid, new_txid) if a != b)

    print(f"Sự thay đổi dữ liệu: Fee tăng 0.00000001")
    print(f"Số ký tự khác biệt trong mã Hash: {diff_chars} / {len(original_txid)}")

    if original_txid != new_txid and diff_chars > (len(original_txid) // 2):
        print("=> Kết quả: Mã TXID thay đổi hoàn toàn (Avalanche Effect). [PASS]")
    else:
        print("=> Kết quả: Mã TXID không thay đổi đủ lớn. [FAIL]")


if __name__ == "__main__":
    test_transaction_hashing()
    test_avalanche_effect()