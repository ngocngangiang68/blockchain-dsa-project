import unittest
import time
from sourcecode.blockchain_dsa.utils import generate_mock_transactions
from sourcecode.blockchain_dsa.mempool import Mempool
from sourcecode.blockchain_dsa.block import Block

class TestBlockCreation(unittest.TestCase):
    def test_block_initialization(self):
        print("\n--- TEST THỰC NGHIỆM: KHỞI TẠO BLOCK TỪ LUỒNG DỮ LIỆU CHUẨN ---")
        
        # Bước 1: Khởi tạo dữ liệu giả lập (Mock Data) theo luồng Module 1
        mock_data = generate_mock_transactions(10000)
        
        # Bước 2: Đưa dữ liệu vào Mempool và thực hiện sắp xếp (Data Pipeline Module 2)
        mempool = Mempool()
        mempool.add_transactions_bulk(mock_data)
        mempool.sort_by_fee()
        
        # Trích xuất 4000 giao dịch có độ ưu tiên cao nhất để đóng gói
        top_4000_txs = mempool.get_top_transactions(4000)

        # Bước 3: Đưa dữ liệu vào Block và đo lường hiệu năng khởi tạo (Module 3)
        start_time = time.perf_counter()
        block = Block(top_4000_txs)
        end_time = time.perf_counter()

        duration = end_time - start_time
        print(f"[Block Performance] Thời gian nạp 4000 giao dịch vào Block: {duration:.6f}s")
        
        # Kiểm thử tính đúng đắn: Đảm bảo Block nhận đúng 4000 giao dịch và đạt mục tiêu thời gian < 0.03s
        self.assertEqual(len(block.transactions), 4000)
        self.assertLess(duration, 0.03, "Lỗi: Thời gian khởi tạo Block vượt quá giới hạn 0.03s!")

if __name__ == '__main__':
    unittest.main()