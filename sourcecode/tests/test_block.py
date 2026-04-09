import unittest
import time
# Đã tối ưu: Import thẳng từ module gốc thông qua __init__.py
from sourcecode.blockchain_dsa import Block, Transaction

class TestBlockCreation(unittest.TestCase):
    def test_block_initialization(self):
        print("\n--- TEST THỰC NGHIỆM: KHỞI TẠO BLOCK ---")
        
        # Chỉ tạo mock 4000 giao dịch cục bộ để Unit Test riêng cho Block 
        mock_4000_txs = [
            Transaction(f"Sender{i}", f"Receiver{i}", 10.0, 0.01) 
            for i in range(4000)
        ]
        
        # Đưa dữ liệu vào Block và đo lường hiệu năng khởi tạo
        start_time = time.perf_counter()
        block = Block(mock_4000_txs)
        end_time = time.perf_counter()

        duration = end_time - start_time
        print(f"[Block Performance] Thời gian nạp 4000 giao dịch vào Block: {duration:.6f}s")
        
        # Kiểm thử tính đúng đắn
        self.assertEqual(len(block.transactions), 4000)
        self.assertLess(duration, 0.03, "Lỗi: Thời gian khởi tạo Block vượt quá giới hạn 0.03s!")

if __name__ == '__main__':
    unittest.main()