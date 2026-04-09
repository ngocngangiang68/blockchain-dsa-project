from sourcecode.blockchain_dsa.utils import compute_hash


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
    current = txid
    _hash = compute_hash
    for h, pos in proof:
        # Băm trực tiếp theo vị trí
        current = _hash(current + h if pos == 'right' else h + current)
    return current == merkle_root