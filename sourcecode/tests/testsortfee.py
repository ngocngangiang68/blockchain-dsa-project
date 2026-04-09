# Nhập class Mempool
from sourcecode.blockchain_dsa.mempool import Mempool
# Nhập hàm tạo 10.000 giao dịch giả từ file utils.py
from sourcecode.blockchain_dsa.utils import generate_mock_transactions
# Nhập thư viện time của để đo thời gian chạy code
import time


def test_mempool_and_views():
    print("=== 1. KHỞI TẠO VÀ NẠP DỮ LIỆU ===")

    # Khởi tạo phòng chờ Mempool
    mempool = Mempool()

    # Gọi thẳng hàm để mượn 10.000 giao dịch ảo
    mock_data = generate_mock_transactions(10000)

    # Nạp 10.000 giao dịch đó vào Mempool
    mempool.add_transactions_bulk(mock_data)
    print(f"-> Đã nạp thành công: {len(mempool)} giao dịch vào Mempool.\n")


    # TEST 1: KỊCH BẢN TẠO BLOCK (GÓC NHÌN CỦA HỆ THỐNG BLOCKCHAIN)

    print("=== 2. TEST CHUẨN BỊ BLOCK ===")

    # Bấm giờ lúc bắt đầu (Dùng perf_counter để có độ chính xác cao nhất)
    start_time = time.perf_counter()

    # Bắt đầu xếp hàng 10.000 giao dịch theo đúng luật (Phí cao trước, thời gian cũ trước)
    mempool.sort_by_fee()

    # Cắt lấy 4000 giao dịch xịn nhất để đóng gói thành 1 Block
    block_txs = mempool.get_top_transactions(4000)

    # Bấm giờ kết thúc
    end_time = time.perf_counter()

    # In ra báo cáo thời gian
    print(f"-> Thời gian sắp xếp cực nhanh: {end_time - start_time:.6f} giây")
    print(f"-> Đã lấy ra ĐÚNG: {len(block_txs)} giao dịch cho Block.")

    # Không in vòng lặp dài dòng. Chỉ in ra ông số 1 và ông số 4000
    # để chứng minh logic thuật toán đã chạy đúng.
    if len(block_txs) > 0:
        print("\n[Kiểm tra tính đúng đắn của Block]")
        print(f"  + Top 1 (Đứng đầu hàng) : Fee = {block_txs[0].fee:.8f} | Time = {block_txs[0].timestamp:.2f}")
        print(f"  + Top 4000 (Chốt sổ)    : Fee = {block_txs[-1].fee:.8f} | Time = {block_txs[-1].timestamp:.2f}\n")


    # TEST 2: KỊCH BẢN XEM LỊCH SỬ (GÓC NHÌN NGƯỜI DÙNG TRÊN APP NGÂN HÀNG)
    print("=== 3. TEST CHẾ ĐỘ VIEW (LỊCH SỬ GIAO DỊCH) ===")

    # Lấy toàn bộ giao dịch hiện có để làm bộ lọc hiển thị
    all_txs = mempool.transactions

    # [VIEW 1] Sắp xếp Thời gian: Mới nhất -> Lâu nhất
    # Dùng hàm sorted() để tạo ra một list mới chỉ dùng để hiển thị, không làm hỏng list gốc.
    # reverse=True nghĩa là xếp ngược (từ Lớn đến Nhỏ, tức là ngày gần đây nhất sẽ lên đầu).
    view_newest = sorted(all_txs, key=lambda tx: tx.timestamp, reverse=True)
    print("\n[View 1] Bộ lọc Thời gian: Mới nhất -> Lâu nhất")
    print(f"  -> Bản ghi đầu tiên: Time = {view_newest[0].timestamp:.2f}")
    print(f"  -> Bản ghi cuối cùng: Time = {view_newest[-1].timestamp:.2f}")

    # [VIEW 2] Sắp xếp Thời gian: Lâu nhất -> Mới nhất
    # reverse=False (mặc định) nghĩa là xếp từ Nhỏ đến Lớn (ngày cũ nhất lên đầu).
    view_oldest = sorted(all_txs, key=lambda tx: tx.timestamp, reverse=False)
    print("\n[View 2] Bộ lọc Thời gian: Lâu nhất -> Mới nhất")
    print(f"  -> Bản ghi đầu tiên: Time = {view_oldest[0].timestamp:.2f}")

    # [VIEW 3] Sắp xếp Số tiền: Lớn nhất -> Nhỏ nhất
    # Sort dựa trên thuộc tính 'amount' (số tiền giao dịch).
    view_amount_desc = sorted(all_txs, key=lambda tx: tx.amount, reverse=True)
    print("\n[View 3] Bộ lọc Số tiền: Lớn nhất -> Nhỏ nhất")
    print(f"  -> Lượng tiền lớn nhất: {view_amount_desc[0].amount:.4f} coin")

    # [VIEW 4] Sắp xếp Số tiền: Nhỏ nhất -> Lớn nhất
    view_amount_asc = sorted(all_txs, key=lambda tx: tx.amount, reverse=False)
    print("\n[View 4] Bộ lọc Số tiền: Nhỏ nhất -> Lớn nhất")
    print(f"  -> Lượng tiền nhỏ nhất: {view_amount_asc[0].amount:.4f} coin")


# Lệnh này đảm bảo đoạn code test chỉ chạy khi ta chạy trực tiếp file này.
if __name__ == "__main__":
    test_mempool_and_views()