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