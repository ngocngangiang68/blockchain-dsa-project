import time
import pytest
import random
from sourcecode.blockchain_dsa.merkle_tree import MerkleTree

random.seed(42)

def test_merkle_tree():
    # giả lập dữ liệu giao dịch
    transactions = [f"tx{i}" for i in range(4000)]


    # [1] Build Root
    start = time.time()
    tree = MerkleTree(transactions)
    root = tree.get_root()
    t_build = time.time() - start
    print(f"[1] Build Root:   {t_build:.6f}s | < 0.01s: {'✅' if t_build < 0.01 else '❌'}")

    # [2] Create Proof
    start = time.time()
    proof = tree.get_proof(transactions[0])
    t_proof = time.time() - start
    print(f"[2] Create Proof: {t_proof:.6f}s")

    # [3] Verify Proof
    start = time.time()
    ok = MerkleTree.verify_proof(transactions[0], proof, root)
    t_verify = time.time() - start
    print(f"[3] Verify Proof: {t_verify:.8f}s | Result: {'✅' if ok else '❌'}")

    assert ok

