from .sorting import sort_transactions_for_block

class Mempool:
    """
    Mọi giao dịch người dùng tạo ra sẽ phải vào đây đứng chờ,sau đó được sắp xếp theo phí để ưu tiên đưa vào Block.
    """

    def __init__(self):
        # Khởi tạo một danh sách (list) rỗng để chứa các giao dịch.
        self.transactions = []

    def add_transactions_bulk(self, tx_list):
        """
        Hàm nạp dữ liệu hàng loạt.
        Nhận vào một danh sách các giao dịch (tx_list) và nối nó vào phòng chờ.
        """
        self.transactions.extend(tx_list)

    def sort_by_fee(self):
        """Sắp xếp theo phí (cao → thấp), timestamp (cũ → mới)"""
        # Dùng MergeSort (stable sort)
        self.transactions = sort_transactions_for_block(self.transactions)

    def get_top_transactions(self, limit=4000):
        # Hàm cắt danh sách để lấy số lượng giao dịch đưa vào Block.
        # Tham số limit=4000 nghĩa là mặc định sẽ lấy 4000 người đứng đầu hàng.
        # Cú pháp [:limit] là lệnh cắt (slice) của Python, lấy từ vị trí 0 đến 4000.
        return self.transactions[:limit]

    def __len__(self):
        """
        Hàm đếm số lượng.
        Giúp ta có thể dùng lệnh len(mempool) để biết có bao nhiêu người trong phòng chờ.
        """
        return len(self.transactions)