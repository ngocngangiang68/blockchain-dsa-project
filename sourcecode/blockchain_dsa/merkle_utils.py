from .utils import compute_hash


def get_merkle_proof(
    transactions,
    target_txid
):
    """
    Tạo Merkle Proof chuẩn:
    - transactions: list Transaction object
    - target_txid: txid cần verify
    """

    nodes = [
        tx.txid
        for tx in transactions
    ]

    try:
        idx = nodes.index(
            target_txid
        )

    except ValueError:
        return None

    proof = []

    while len(nodes) > 1:

        # số node lẻ
        if len(nodes) % 2 != 0:
            nodes.append(
                nodes[-1]
            )

        sibling_idx = (
            idx + 1
            if idx % 2 == 0
            else idx - 1
        )

        position = (
            'right'
            if idx % 2 == 0
            else 'left'
        )

        proof.append(
            (
                nodes[sibling_idx],
                position
            )
        )

        # build next level
        new_nodes = []

        for i in range(
            0,
            len(nodes),
            2
        ):
            combined = (
                nodes[i]
                + nodes[i + 1]
            )

            new_nodes.append(
                compute_hash(
                    combined
                )
            )

        nodes = new_nodes
        idx //= 2

    return proof


def verify_merkle_proof(
    txid,
    proof,
    merkle_root
):
    """
    Verify Merkle Proof chuẩn
    """

    if proof is None:
        return False

    current = txid

    for (
        sibling_hash,
        position
    ) in proof:

        if position == 'right':

            current = compute_hash(
                current
                + sibling_hash
            )

        else:

            current = compute_hash(
                sibling_hash
                + current
            )


    return (
        current
        == merkle_root
    )