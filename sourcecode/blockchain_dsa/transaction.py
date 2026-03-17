from utils import compute_hash#lay ham hash o file utils de dung.tao ra ma dinh danh(TXID)
import time#khai bao bien thoi gian cua Python de ghi lai chinh xac thoi diem giao dich duoc tao ra


class Transaction:
    def __init__(self, sender, receiver, amount, fee):
        # Thông tin người gửi, nhận và số tiền [cite: 22]
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        # Phí giao dịch - tiêu chí để sắp xếp [cite: 23]
        self.fee = fee
        # Thời gian tạo giao dịch [cite: 24]
        self.timestamp = time.time()

        # TXID: Mã băm định danh duy nhất [cite: 21]
        # Lưu ý: Bao gồm cả 'fee' và 'timestamp' để đảm bảo tính duy nhất
        data_to_hash = f"{sender}{receiver}{amount}{fee}{self.timestamp}"
        #gom all du lieu cua giao dich thanh chuoi duy nhat de cbi tao bam(hash)
        self.txid = compute_hash(data_to_hash)
        #goi ham bam tu utils.py de bien chuoi du lieu tren thanh 1 ma bam SHA256 dai 64 ki tu(Transaction ID)

    def __str__(self):
        return f"[{self.txid[:10]}...] {self.sender} -> {self.receiver}: {self.amount} (Fee: {self.fee})"
    #dang chi lay 10 ki tu de in ra nhin gon hon