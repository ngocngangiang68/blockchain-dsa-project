import time
import random
import copy
from sourcecode.blockchain_dsa.block import Block
from sourcecode.blockchain_dsa.merkle_tree import compute_merkle_root
from sourcecode.blockchain_dsa.test_data import MOCK_4000_TRANSACTIONS
from sourcecode.blockchain_dsa.utils import compute_hash
from sourcecode.blockchain_dsa.merkle_utils import get_merkle_proof, verify_merkle_proof

random.seed(42) 

# 1. Khởi tạo Block (Dữ liệu đã finalize và hash sẵn trong Block)
block = Block(MOCK_4000_TRANSACTIONS)
txs = block.transactions
target_id = txs[500].txid

print(f"--- KIỂM THỬ HIỆU NĂNG & BẢO MẬT (4000 TXs) ---")

# --- PHẦN 1: ĐO THỜI GIỜ ---
t1 = time.perf_counter()
root = compute_merkle_root(txs)
t_build = time.perf_counter() - t1

t2 = time.perf_counter()
proof = get_merkle_proof(txs, target_id)
t_proof = time.perf_counter() - t2

t3 = time.perf_counter()
is_valid = verify_merkle_proof(target_id, proof, root)
t_verify = time.perf_counter() - t3

print(f"[1] Build Root:   {t_build:.6f}s | < 0.01s: {'✅' if t_build < 0.01 else '❌'}")
print(f"[2] Create Proof: {t_proof:.6f}s")
print(f"[3] Verify Proof: {t_verify:.8f}s")

# --- PHẦN 2: KIỂM TRA BẢO MẬT (GIỮ NGUYÊN) ---
print(f"\n--- KIỂM TRA TOÀN VẸN ---")
malicious_txs = copy.deepcopy(txs)
malicious_txs[1000].txid = compute_hash(malicious_txs[1000].txid + "malicious")
new_root = compute_merkle_root(malicious_txs)

is_rejected = not verify_merkle_proof(compute_hash(target_id + "fake"), proof, root)

print(f"[*] Avalanche Effect: {'✅' if root != new_root else '❌'}")
print(f"[*] Chặn giả mạo:     {'✅' if is_rejected else '❌'}")
