from .utils import compute_hash
import time


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
        self.txid = compute_hash(data_to_hash)

    def __str__(self):
        return f"[{self.txid[:10]}...] {self.sender} -> {self.receiver}: {self.amount} (Fee: {self.fee})"