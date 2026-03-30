class Block:

    def __init__(self, transactions, prev_hash="0"):

        """

        Khởi tạo Block mới. 

        Tiếp nhận trực tiếp danh sách 4000 giao dịch đã được Mempool (Module 2) lọc và sắp xếp.

        """

        # Lưu trữ danh sách 4000 giao dịch gốc được truyền vào

        self.transactions = transactions  

        self.prev_hash = prev_hash

        self.merkle_root = None  # Sẽ được tính toán ở Module Merkle Tree sau



    def _quick_sort(self, arr, key_func, reverse=False):

        """

        Thuật toán QuickSort tổng quát để hỗ trợ các chế độ View.

        Độ phức tạp: O(n log n). Sắp xếp trên bản sao, không làm thay đổi dữ liệu gốc của Block.

        """

        if len(arr) <= 1:

            return arr

        

        pivot = arr[len(arr) // 2]

        left = [x for x in arr if key_func(x) < key_func(pivot)]

        middle = [x for x in arr if key_func(x) == key_func(pivot)]

        right = [x for x in arr if key_func(x) > key_func(pivot)]



        if reverse:

            return self._quick_sort(right, key_func, reverse) + middle + self._quick_sort(left, key_func, reverse)

        else:

            return self._quick_sort(left, key_func, reverse) + middle + self._quick_sort(right, key_func, reverse)



    # --------------------------------------------------------------------------

    # CÁC CHẾ ĐỘ VIEW TRUY XUẤT DỮ LIỆU (KHÔNG LÀM ẢNH HƯỞNG DATA GỐC)

    # --------------------------------------------------------------------------



    def get_view_fee_desc(self):

        """View 1: Phí giảm dần (Ưu tiên giao dịch có lợi nhuận cao nhất)"""

        return self._quick_sort(self.transactions.copy(), lambda x: getattr(x, 'fee', 0), reverse=True)



    def get_view_fee_asc(self):

        """View 2: Phí tăng dần (Các giao dịch phí thấp)"""

        return self._quick_sort(self.transactions.copy(), lambda x: getattr(x, 'fee', 0), reverse=False)



    def get_view_time_desc(self):

        """View 3: Thời gian giảm dần (Giao dịch mới nhất lên đầu)"""

        return self._quick_sort(self.transactions.copy(), lambda x: getattr(x, 'timestamp', 0), reverse=True)



    def get_view_time_asc(self):

        """View 4: Thời gian tăng dần (Giao dịch cũ nhất lên đầu)"""

        return self._quick_sort(self.transactions.copy(), lambda x: getattr(x, 'timestamp', 0), reverse=False)