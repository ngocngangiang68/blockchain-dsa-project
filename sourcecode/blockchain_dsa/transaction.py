from sourcecode.blockchain_dsa.utils import compute_hash#lay ham hash o file utils de dung.tao ra ma dinh danh(TXID)
import time#Thư viện hỗ trợ lấy mốc thời gian thực để ghi nhận thời điểm giao dịch


class Transaction:
    #Lớp này dùng để định nghĩa cấu trúc của một giao dịch (Transaction).
    #Mỗi giao dịch sẽ bao gồm thông tin người gửi, người nhận, số tiền, phí và mã định danh duy nhất (TXID).
    def __init__(self, sender, receiver, amount, fee, timestamp=None):
        # Lưu trữ tên hoặc địa chỉ ví của người gửi tiền
        self.sender = sender
        # Lưu trữ tên hoặc địa chỉ ví của người nhận tiền
        self.receiver = receiver
        # Số tiền thực hiện chuyển đổi trong giao dịch
        self.amount = amount
        # Phí giao dịch - tiêu chí để sắp xếp
        self.fee = fee
        # Thời gian tạo giao dịch:
        self.timestamp = timestamp if timestamp is not None else 1700000000 #time co dinh

        # Tạo mã định danh duy nhất (TXID) cho giao dịch:
        # Gom tất cả các thông tin biến đổi (người gửi, nhận, số tiền, phí và đặc biệt là thời gian)
        # thành một chuỗi văn bản duy nhất để chuẩn bị cho quá trình băm (hashing).
        data_to_hash = f"{sender}{receiver}{amount}{fee}{self.timestamp}"
        # Sử dụng hàm băm SHA256 từ file utils.py để biến chuỗi dữ liệu trên
        # thành một mã băm duy nhất dài 64 ký tự, đóng vai trò là ID của giao dịch.
        self.txid = compute_hash(data_to_hash)
        #goi ham bam tu utils.py de bien chuoi du lieu tren thanh 1 ma bam SHA256 dai 64 ki tu(Transaction ID)

    def __str__(self):
        #Hàm này giúp hiển thị thông tin giao dịch dưới dạng văn bản dễ đọc khi dùng lệnh print().
        return f"[{self.txid[:10]}...] {self.sender} -> {self.receiver}: {self.amount} (Fee: {self.fee})"
    #dang chi lay 10 ki tu de in ra nhin gon hon
