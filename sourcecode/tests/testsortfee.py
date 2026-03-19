# Nhập class Mempool
from sourcecode.blockchain_dsa.mempool import Mempool
# Nhập hàm tạo 10.000 giao dịch giả từ file utils.py
from sourcecode.blockchain_dsa.utils import generate_mock_transactions

# Nhập thư viện time của để đo thời gian chạy code
import time

def test_sorting_by_fee():
    print("=== BẮT ĐẦU CHẠY THỬ NHIỆM VỤ===")
    # BƯỚC 1: KHỞI TẠO VÀ NẠP DỮ LIỆU
    mempool = Mempool()
    print("1. Đang tạo 10,000 giao dịch mẫu...")

    # Gọi hàm của để lấy 10.000 giao dịch
    data = generate_mock_transactions(10000)

    # Đưa 10.000 giao dịch đó vào Mempool
    mempool.add_transactions_bulk(data)
    print(f"-> Đã nạp thành công {len(mempool)} giao dịch vào Mempool.\n")

    # BƯỚC 2: SẮP XẾP VÀ ĐO THỜI GIAN
    print("2. Bắt đầu sắp xếp bằng thuật toán Quick Sort...")

    # Ghi lại thời gian lúc bắt đầu bắt đầu chạy
    start_time = time.time()

    # Gọi hàm sắp xếp trong Mempool
    mempool.sort_by_fee()

    # Ghi lại thời gian lúc chạy xong
    end_time = time.time()

    # BƯỚC 3: IN KẾT QUẢ RA MÀN HÌNH
    # Tính thời gian chạy bằng cách lấy lúc kết thúc trừ đi lúc bắt đầu
    thoi_gian_chay = end_time - start_time
    print(f"-> Hoàn thành sắp xếp cực nhanh trong: {thoi_gian_chay:.4f} giây.\n")
    print("3. KẾT QUẢ: TOP 5 GIAO DỊCH CÓ PHÍ CAO NHẤT:")

    # Lấy ra 5 giao dịch đứng đầu (phí cao nhất)
    top_5 = mempool.get_top_transactions(5)

    # Dùng vòng lặp for để in từng giao dịch ra màn hình
    # enumerate(top_5, 1) giúp đánh số thứ tự từ 1 đến 5
    for stt, tx in enumerate(top_5, 1):
        # In ra số thứ tự, ID giao dịch và mức phí
        print(f"Top {stt}: ID [{tx.txid[:8]}...] | Phí (Fee): {tx.fee}")
# Lệnh giúp máy tính biết phải chạy hàm test_sorting_by_fee() khi nhấn Run
if __name__ == "__main__":
    test_sorting_by_fee()