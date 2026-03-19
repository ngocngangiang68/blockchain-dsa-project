# Import hàm thuật toán sắp xếp từ file sorting.py
from sourcecode.blockchain_dsa.sorting import quick_sort_transactions

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
        """
        Hàm thực hiện việc sắp xếp.
        Gọi thuật toán Quick Sort ở file sorting.py,sắp xếp danh sách hiện tại và lưu đè lại vào phòng chờ.
        """
        self.transactions = quick_sort_transactions(self.transactions)

    def get_top_transactions(self, limit=10):
        """
        Hàm lấy ra những giao dịch VIP (phí cao nhất).
        - limit=10: Nghĩa là mặc định sẽ lấy 10 giao dịch đứng đầu.
        - Cắt danh sách từ vị trí 0 đến vị trí 'limit'.
        """
        return self.transactions[:limit]

    def __len__(self):
        """
        Hàm đếm số lượng.
        Giúp ta có thể dùng lệnh len(mempool) để biết có bao nhiêu người trong phòng chờ.
        """
        return len(self.transactions)