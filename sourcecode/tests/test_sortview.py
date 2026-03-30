import unittest
import time
import random
from sourcecode.blockchain_dsa.block import Block
from sourcecode.blockchain_dsa.transaction import Transaction

class TestSortView(unittest.TestCase):
    def setUp(self):
        # Tạo nhanh 4000 giao dịch với fee và timestamp ngẫu nhiên để test hàm sort
        # Không dùng Mempool ở đây để đảm bảo đây là Unit Test độc lập của Module 3
        mock_txs = []
        for i in range(4000):
            tx = Transaction(
                sender=f"S{i}", 
                receiver=f"R{i}", 
                amount=random.uniform(1, 100), 
                fee=random.uniform(0.001, 0.05)
            )
            mock_txs.append(tx)
        
        self.block = Block(mock_txs)

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