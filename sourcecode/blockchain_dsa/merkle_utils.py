from .utils import compute_hash


def get_merkle_proof(transactions, target_txid):
    nodes = [tx.txid for tx in transactions]
    try:
        idx = nodes.index(target_txid)
    except ValueError:
        return None

    proof = []
    _hash = compute_hash
    while len(nodes) > 1:
        if len(nodes) % 2 != 0:
            nodes.append(nodes[-1])

        # Lấy sibling dựa trên index
        sibling_idx = idx + 1 if idx % 2 == 0 else idx - 1
        proof.append((nodes[sibling_idx], 'right' if idx % 2 == 0 else 'left'))

        # Nâng tầng
        nodes = [_hash(nodes[i] + nodes[i + 1]) for i in range(0, len(nodes), 2)]
        idx //= 2
    return proof


def verify_merkle_proof(txid, proof, merkle_root):
    """
    Xác minh Merkle Proof:

    - txid: hash của transaction ban đầu (leaf)
    - proof: danh sách các tuple (hash_anh_em, vị_trí)
        + hash_anh_em: hash của node "anh em"
        + vị_trí: 'left' hoặc 'right'
    - merkle_root: root cần verify

    Ý tưởng:
    - Bắt đầu từ txid
    - Lần lượt hash với các node anh em theo đúng thứ tự
    - Nếu kết quả cuối cùng == merkle_root → hợp lệ
    """

    # current sẽ đại diện cho hash đang được "leo lên cây"
    current = txid

    # Gán hàm hash (giả sử compute_hash đã được định nghĩa)
    _hash = compute_hash

    # Duyệt từng bước trong proof
    for sibling_hash, position in proof:

        """
        Nếu sibling ở bên phải:
            current = hash(current + sibling)

        Nếu sibling ở bên trái:
            current = hash(sibling + current)

        Thứ tự rất quan trọng!
        """
        if position == 'right':
            current = _hash(current + sibling_hash)
        else:  # position == 'left'
            current = _hash(sibling_hash + current)

    # So sánh với Merkle Root
    return current == merkle_root