from sourcecode.blockchain_dsa.sorting import (
    quick_sort_transactions,
    merge_sort_transactions,
    sort_transactions_by_id
)
import time
from sourcecode.blockchain_dsa.utils import compute_hash
from sourcecode.blockchain_dsa.merkle_tree import compute_merkle_root
class Block:
    def __init__(self, transactions, prev_hash="0"):
        # ✓ Lưu trữ CỐ ĐỊNH theo ID (dùng MergeSort)
        self.transactions = sort_transactions_by_id(transactions.copy())

        self.prev_hash = prev_hash
        self.timestamp = time.time()
        self.merkle_root = None
        self.block_hash = None
        self._cached_views = {}

    @classmethod
    def create_from_mempool(cls, mempool, prev_hash="0"):
        """"Lấy 4000 tx từ mempool (đã sort theo phí)"""
        top_4000_txs = mempool.get_top_transactions(4000)
        return cls(top_4000_txs, prev_hash)

    def finalize(self):
        """Đóng gói block hoàn chỉnh"""
        # Tính merkle root dựa trên thứ tự ID cố định
        self.merkle_root = compute_merkle_root(self.transactions)

        # Tính block hash
        block_data = f"{self.prev_hash}{self.merkle_root}{self.timestamp}"
        self.block_hash = compute_hash(block_data)

        return self

    def verify_integrity(self):
        # Tính toán lại hash dựa trên dữ liệu hiện tại trong object
        actual_hash = self.compute_block_hash()

        # So sánh với mã hash đã được "khóa" lúc finalize
        if actual_hash != self.block_hash:
            return False, "Dữ liệu đã bị thay đổi (Timestamp hoặc Merkle Root không khớp)!"
        return True, "Block hợp lệ."

    def get_view_by_fee_desc(self, page=1, per_page=10):
        """
        View: Sắp xếp theo phí giảm dần
        Nếu phí bằng nhau → ưu tiên timestamp nhỏ hơn (đến trước)
        Hỗ trợ pagination + cache
        """
        cache_key = 'fee_desc'

        # ✅ Nếu đã cache → lấy luôn, không sort lại
        if cache_key not in self._cached_views:
            def sort_key(tx):
                return (-tx.fee, tx.timestamp)

            self._cached_views[cache_key] = quick_sort_transactions(
                self.transactions.copy(),
                key_func=sort_key,
                reverse=False
            )

        sorted_txs = self._cached_views[cache_key]

        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        return {
            'data': sorted_txs[start_idx:end_idx],
            'page': page,
            'per_page': per_page,
            'total': len(sorted_txs),
            'total_pages': (len(sorted_txs) + per_page - 1) // per_page
        }

    def get_view_by_fee_asc(self, page=1, per_page=10):
        """View: Sắp xếp theo phí tăng dần (cache + pagination)"""
        cache_key = 'fee_asc'

        if cache_key not in self._cached_views:
            def sort_key(tx):
                return (tx.fee, tx.timestamp)

            self._cached_views[cache_key] = quick_sort_transactions(
                self.transactions.copy(),
                key_func=sort_key,
                reverse=False
            )

        sorted_txs = self._cached_views[cache_key]

        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        return {
            'data': sorted_txs[start_idx:end_idx],
            'page': page,
            'per_page': per_page,
            'total': len(sorted_txs),
            'total_pages': (len(sorted_txs) + per_page - 1) // per_page
        }

    def get_view_by_time_desc(self, page=1, per_page=10):
        """View: Sắp xếp theo thời gian mới nhất (cache + pagination)"""
        cache_key = 'time_desc'

        if cache_key not in self._cached_views:
            self._cached_views[cache_key] = quick_sort_transactions(
                self.transactions.copy(),
                key_func=lambda tx: -tx.timestamp,
                reverse=False
            )

        sorted_txs = self._cached_views[cache_key]

        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        return {
            'data': sorted_txs[start_idx:end_idx],
            'page': page,
            'per_page': per_page,
            'total': len(sorted_txs),
            'total_pages': (len(sorted_txs) + per_page - 1) // per_page
        }

    def get_view_by_time_asc(self, page=1, per_page=10):
        """View: S��p xếp theo thời gian cũ nhất (cache + pagination)"""
        cache_key = 'time_asc'

        if cache_key not in self._cached_views:
            self._cached_views[cache_key] = quick_sort_transactions(
                self.transactions.copy(),
                key_func=lambda tx: tx.timestamp,
                reverse=False
            )

        sorted_txs = self._cached_views[cache_key]

        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        return {
            'data': sorted_txs[start_idx:end_idx],
            'page': page,
            'per_page': per_page,
            'total': len(sorted_txs),
            'total_pages': (len(sorted_txs) + per_page - 1) // per_page
        }

    def get_view_by_id(self, page=1, per_page=10):
        """View: Sắp xếp theo ID (cũng là thứ tự lưu trữ gốc) - cache + pagination"""
        cache_key = 'by_id'

        if cache_key not in self._cached_views:
            self._cached_views[cache_key] = self.transactions

        sorted_txs = self._cached_views[cache_key]

        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        return {
            'data': sorted_txs[start_idx:end_idx],
            'page': page,
            'per_page': per_page,
            'total': len(sorted_txs),
            'total_pages': (len(sorted_txs) + per_page - 1) // per_page
        }

    # ========== BINARY SEARCH ==========

    def search_by_txid(self, target_txid):
        """Binary search tìm transaction theo ID"""
        from sourcecode.blockchain_dsa.search import binary_search
        return binary_search(self.transactions, target_txid)