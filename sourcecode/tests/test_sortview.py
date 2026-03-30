import unittest
import time
from sourcecode.blockchain_dsa.utils import generate_mock_transactions
from sourcecode.blockchain_dsa.mempool import Mempool
from sourcecode.blockchain_dsa.block import Block

class TestSortView(unittest.TestCase):
    def setUp(self):
        # Thiết lập môi trường kiểm thử tuân thủ chặt chẽ Data Pipeline của hệ thống
        # Giả lập luồng truyền dữ liệu: Transaction -> Mempool -> Block
        mock_data = generate_mock_transactions(10000)
        mempool = Mempool()
        mempool.add_transactions_bulk(mock_data)
        mempool.sort_by_fee()
        
        # Khởi tạo đối tượng Block với 4000 giao dịch đã qua xử lý tại Mempool
        self.block = Block(mempool.get_top_transactions(4000))

    def test_view_performance_and_logic(self):
        print("\n--- TEST THỰC NGHIỆM: HIỆU NĂNG 4 CHẾ ĐỘ VIEW TRONG BLOCK ---")
        
        # Các kịch bản truy xuất (View) cần kiểm thử
        views = [
            ("Phí Giảm dần (Ưu tiên cao nhất)", self.block.get_view_fee_desc),
            ("Phí Tăng dần", self.block.get_view_fee_asc),
            ("Thời gian Giảm dần (Mới nhất)", self.block.get_view_time_desc),
            ("Thời gian Tăng dần (Cũ nhất)", self.block.get_view_time_asc)
        ]

        for name, view_func in views:
            start = time.perf_counter()
            result = view_func()
            duration = time.perf_counter() - start
            
            print(f"[{name}]: {duration:.6f}s")
            # Đảm bảo các hàm view chỉ sắp xếp hiển thị, không làm mất mát dữ liệu gốc (đủ 4000)
            self.assertEqual(len(result), 4000)

if __name__ == '__main__':
    unittest.main()