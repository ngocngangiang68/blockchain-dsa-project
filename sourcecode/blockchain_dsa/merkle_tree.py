import hashlib

def compute_merkle_root(transactions):
    if not transactions:
        return hashlib.sha256(b"").hexdigest()

    # 1. Trích xuất ID thô ngay lập tức để tránh truy cập thuộc tính .txid trong vòng lặp
    nodes = [tx.txid for tx in transactions]

    if len(nodes) == 1:
        return nodes[0]

    # 2. Cache các hàm vào biến cục bộ (Local Variables) để Python truy cập nhanh hơn
    _sha256 = hashlib.sha256

    while len(nodes) > 1:
        # Nếu lẻ, nhân đôi phần tử cuối [cite: 133-134]
        if len(nodes) % 2 != 0:
            nodes.append(nodes[-1])

        # TỐI ƯU CỐT LÕI: Sử dụng List Comprehension và băm trực tiếp
        # Loại bỏ hoàn toàn việc gọi hàm trung gian compute_hash()
        nodes = [_sha256((nodes[i] + nodes[i + 1]).encode()).hexdigest()
                 for i in range(0, len(nodes), 2)]

    return nodes[0]




import hashlib

class MerkleTree:
    def __init__(self, transactions):
        """
        Hàm khởi tạo:
        - transactions: danh sách các giao dịch (string)
        - root: Merkle Root được xây dựng từ danh sách giao dịch
        """
        self.transactions = transactions
        self.root = self.build_root(transactions)

    def build_root(self, transactions):
        """
        Xây dựng Merkle Root từ danh sách transaction:
        B1: Hash từng transaction (lá của cây)
        B2: Ghép từng cặp node lại rồi hash tiếp
        B3: Lặp lại cho đến khi còn 1 node duy nhất (root)
        """
        # Bước 1: Hash từng transaction
        nodes = [self.hash(tx) for tx in transactions]

        # Bước 2: Lặp cho đến khi còn 1 node
        while len(nodes) > 1:
            temp = []

            # Duyệt từng cặp node
            for i in range(0, len(nodes), 2):
                left = nodes[i]

                # Nếu số node lẻ → node cuối ghép với chính nó
                right = nodes[i+1] if i+1 < len(nodes) else left

                # Hash 2 node lại với nhau
                combined_hash = self.hash(left + right)

                temp.append(combined_hash)

            # Cập nhật tầng mới
            nodes = temp

        # Node cuối cùng chính là root
        return nodes[0]

    def get_root(self):
        """
        Trả về Merkle Root
        """
        return self.root

    def get_proof(self, transaction):
        """
        (Demo đơn giản)
        Bình thường:
            - Proof sẽ là danh sách các hash "anh em" trên đường đi lên root
        Nhưng ở đây:
            - Chỉ trả về hash của transaction (đơn giản hóa)
        """
        return self.hash(transaction)

    @staticmethod
    def verify_proof(transaction, proof, root):
        """
        Xác minh proof:
        - Kiểm tra proof có đúng là hash của transaction không
        - Kiểm tra root tồn tại

        (Lưu ý: Đây KHÔNG phải verify Merkle Tree chuẩn,
         chỉ là demo đơn giản)
        """
        return proof == MerkleTree.hash(transaction) and root is not None

    @staticmethod
    def hash(data):
        """
        Hàm băm SHA-256:
        - Nhận input là string
        - Trả về hash dạng hex
        """
        return hashlib.sha256(data.encode()).hexdigest()