import math
import time


class MockTX:
    """
    Transaction giả lập tối giản.

    Mục đích:
    - Chỉ lưu txid
    - Giảm tiêu thụ RAM
    - Phục vụ test scalability với dataset cực lớn
    """

    def __init__(self, txid):
        self.txid = txid


class VirtualTransactionList:
    """
    Danh sách transaction ảo.

    Ý tưởng:
    - KHÔNG lưu thật 1,000,000 object trong bộ nhớ
    - Chỉ tạo object khi truy cập index

    => Giúp mô phỏng dữ liệu lớn hiệu quả hơn.
    """

    def __init__(self, size):
        self.size = size

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        return MockTX(index)


def binary_search_steps(arr, target):
    """
    Binary Search trên danh sách đã sort theo TXID.

    Đầu ra:
    - Trả về số bước tìm kiếm thực tế

    Độ phức tạp:
    O(log n)
    """

    left = 0
    right = len(arr) - 1
    steps = 0

    while left <= right:

        # Tăng số lần so sánh
        steps += 1

        mid = (left + right) // 2
        current_txid = arr[mid].txid

        # Tìm thấy target
        if current_txid == target:
            return steps

        # Target nằm bên phải
        elif current_txid < target:
            left = mid + 1

        # Target nằm bên trái
        else:
            right = mid - 1

    return steps


def linear_search_steps(arr, target):
    """
    Linear Search duyệt tuần tự.

    Đầu ra:
    - Trả về số bước duyệt thực tế

    Độ phức tạp:
    O(n)
    """

    for index, tx in enumerate(arr):

        if tx.txid == target:
            return index + 1

    return len(arr)


def run_scalability_test(dataset_size):
    """
    Hàm chạy benchmark scalability.

    Bao gồm:
    - Binary Search
    - Linear Search
    - So sánh số bước
    - So sánh thời gian thực thi
    """

    print("\n" + "=" * 80)
    print(f"SCALABILITY TEST - {dataset_size:,} TRANSACTIONS")
    print("=" * 80)

    # ---------------------------------------------------------
    # Tạo dataset ảo
    # ---------------------------------------------------------
    transactions = VirtualTransactionList(dataset_size)

    # Chọn phần tử cuối để tạo worst-case cho Linear Search
    target_txid = dataset_size - 1

    # =========================================================
    # 1. BINARY SEARCH
    # =========================================================
    start_binary = time.perf_counter()

    binary_steps = binary_search_steps(
        transactions,
        target_txid
    )

    binary_time = time.perf_counter() - start_binary

    # =========================================================
    # 2. LINEAR SEARCH
    # =========================================================
    start_linear = time.perf_counter()

    linear_steps = linear_search_steps(
        transactions,
        target_txid
    )

    linear_time = time.perf_counter() - start_linear

    # =========================================================
    # 3. KẾT QUẢ LÝ THUYẾT
    # =========================================================
    theoretical_steps = math.ceil(math.log2(dataset_size))

    # =========================================================
    # 4. IN KẾT QUẢ
    # =========================================================
    print("\n[1] Binary Search")

    print(f" - Dataset Size:        {dataset_size:,}")
    print(f" - Actual Steps:        {binary_steps}")
    print(f" - Theoretical log2(n): {theoretical_steps}")
    print(f" - Execution Time:      {binary_time:.10f}s")

    print("\n[2] Linear Search")

    print(f" - Actual Steps:        {linear_steps:,}")
    print(f" - Execution Time:      {linear_time:.10f}s")

    print("\n[3] Complexity Analysis")

    print(" - Binary Search Complexity : O(log n)")
    print(" - Linear Search Complexity : O(n)")

    reduction_ratio = linear_steps / binary_steps

    print(
        f"\n✅ Binary Search giảm khoảng "
        f"{reduction_ratio:,.0f} lần số bước duyệt."
    )

    # =========================================================
    # 5. ASSERT
    # =========================================================
    assert binary_steps <= theoretical_steps + 1

    print("\n✅ PASS SCALABILITY TEST")


# =============================================================
# MAIN
# =============================================================
if __name__ == "__main__":

    # ---------------------------------------------------------
    # TEST 100,000 TRANSACTIONS
    # ---------------------------------------------------------
    run_scalability_test(100_000)

    # ---------------------------------------------------------
    # TEST 1,000,000 TRANSACTIONS
    # ---------------------------------------------------------
    run_scalability_test(1_000_000)