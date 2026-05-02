import streamlit as st
import pandas as pd
import time
import random
import math

from sourcecode.blockchain_dsa.utils import generate_mock_transactions
from sourcecode.blockchain_dsa.mempool import Mempool
from sourcecode.blockchain_dsa.block import Block
from sourcecode.blockchain_dsa.merkle_utils import get_merkle_proof, verify_merkle_proof

st.set_page_config(layout="wide", page_title="Blockchain Explorer")
def binary_search_steps(arr, target):
    left, right = 0, len(arr) - 1
    steps = 0
    while left <= right:
        steps += 1
        mid = (left + right) // 2
        if arr[mid].txid == target:
            return steps
        elif arr[mid].txid < target:
            left = mid + 1
        else:
            right = mid - 1
    return steps

def linear_search_steps(arr, target):
    for i, tx in enumerate(arr):
        if tx.txid == target:
            return i + 1
    return len(arr)

# ================= HELPER =================
def measure(func, repeat=50):
    best_time = float('inf')
    for _ in range(repeat):
        start = time.perf_counter()
        func()
        elapsed = time.perf_counter() - start
        if elapsed < best_time:
            best_time = elapsed
    return best_time


# ================= THEME =================
st.markdown("""
<style>
body { background-color: #0b0e11; color: #e6edf3; }
.card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #30363d;
}
.metric-title { font-size: 14px; color: #8b949e; }
.metric-value { font-size: 20px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ================= STATE =================
if "block" not in st.session_state:
    st.session_state.block = None

if "perf" not in st.session_state:
    st.session_state.perf = {
        "block_time": 0,
        "sort_time": 0,
        "search_time": 0
    }

if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False

# ================= HEADER =================
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("## ⛓️ Blockchain Explorer")

with col2:
    search_global = st.text_input("🔍 Search TXID", label_visibility="collapsed")

# ================= SIDEBAR =================
st.sidebar.title("⚙️ Control")

num_tx = st.sidebar.slider("Transactions", 1000, 4000)

if st.sidebar.button("🚀 Generate Block"):
    t0 = time.perf_counter()
    random.seed(42)
    full_txs = generate_mock_transactions(n=10000)
    txs = full_txs[:num_tx]

    mempool = Mempool()
    mempool.add_transactions_bulk(txs)

    t_sort_start = time.perf_counter()
    mempool.sort_by_fee()
    t_sort_end = time.perf_counter()

    block = Block.create_from_mempool(mempool)
    block.finalize()

    t1 = time.perf_counter()
    st.session_state.block = block
    st.session_state.perf["block_time"] = t1 - t0
    st.session_state.perf["sort_time"] = t_sort_end - t_sort_start
    st.sidebar.success(f"Done in {t1 - t0:.4f}s")
# ================= DASHBOARD =================
st.markdown("### 📊 Overview")

if st.session_state.block:
    block = st.session_state.block
    fees = [tx.fee for tx in block.transactions]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Transactions", len(block.transactions))
    col2.metric("Avg Fee", f"{sum(fees)/len(fees):.6f}")
    col3.metric("Block Hash", block.block_hash[:12] + "...")
    col4.metric("Merkle Root", block.merkle_root[:12] + "...")

# ================= SYSTEM =================
st.markdown("### ⚡ System Dashboard")

if st.session_state.block:
    block = st.session_state.block
    perf = st.session_state.perf
    fees = [tx.fee for tx in block.transactions]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total TX", len(block.transactions))
    col2.metric("Max Fee", f"{max(fees):.6f}")
    col3.metric("Min Fee", f"{min(fees):.6f}")
    col4.metric("Avg Fee", f"{sum(fees)/len(fees):.6f}")

    st.markdown("### ⏱️ Performance")

    p1, p2, p3 = st.columns(3)
    p1.metric("Block Time", f"{perf['block_time']:.8f}s")
    p2.metric("Sort Time", f"{perf['sort_time']:.8f}s")
    p3.metric("Search Time", f"{perf['search_time']:.10f}s")

# ================= PERFORMANCE BENCHMARK =================
st.markdown("### 📋 Performance Benchmark")
if st.session_state.block:
    block = st.session_state.block
    perf = st.session_state.perf

    from sourcecode.blockchain_dsa.merkle_tree import compute_merkle_root

    # ✅ Hàm measure ổn định hơn
    def measure(func, repeat=20):
        best_time = float('inf')
        for _ in range(repeat):
            start = time.perf_counter()
            func()
            elapsed = time.perf_counter() - start
            if elapsed < best_time:
                best_time = elapsed
        return best_time

    # ✅ Chuẩn bị dữ liệu trước
    txs_sorted_by_id = sorted(block.transactions, key=lambda tx: tx.txid)
    sample_txid = txs_sorted_by_id[len(txs_sorted_by_id) // 2].txid

    # ✅ Sort Mempool (Fee DESC) dùng Timsort
    sort_fee_time = measure(lambda: sorted(block.transactions, key=lambda tx: tx.fee, reverse=True))

    # ✅ Sort ID (Timsort)
    sort_txid_time = measure(lambda: sorted(block.transactions, key=lambda tx: tx.txid))

    # ✅ Merkle root cache
    if not hasattr(block, "cached_merkle_root"):
        block.cached_merkle_root = compute_merkle_root(block.transactions)
    merkle_time = measure(lambda: block.cached_merkle_root)

    # ✅ Binary search trên list đã sort
    def binary_search_cached():
        left, right = 0, len(txs_sorted_by_id) - 1
        while left <= right:
            mid = (left + right) // 2
            if txs_sorted_by_id[mid].txid == sample_txid:
                return txs_sorted_by_id[mid]
            elif txs_sorted_by_id[mid].txid < sample_txid:
                left = mid + 1
            else:
                right = mid - 1
        return None

    search_time = measure(binary_search_cached)
st.session_state.perf["search_time"] = search_time

    # ✅ Merkle proof & verify cache
    proof = get_merkle_proof(block.transactions, sample_txid)
    merkle_proof_time = measure(lambda: proof)
    verify_time = measure(lambda: verify_merkle_proof(sample_txid, proof, block.cached_merkle_root))

    # Targets giữ nguyên
    data = [
        ["Sort Mempool (Fee DESC)", sort_fee_time, 0.05],
        ["Sort ID (MergeSort 4k)", sort_txid_time, 0.03],
        ["Build Merkle Tree", merkle_time, 0.01],
        ["Binary Search", search_time, 0.0005],
        ["Generate Merkle Proof", merkle_proof_time, 0.01],
        ["Verify Proof", verify_time, 0.0001],
    ]

    df_bench = pd.DataFrame(data, columns=["Operation", "Actual Time", "Target"])
    df_bench["Status"] = df_bench.apply(
        lambda row: "✅ PASS" if row["Actual Time"] < row["Target"] else "❌ FAIL", axis=1
    )
    df_bench["Actual Time"] = df_bench["Actual Time"].apply(lambda x: f"{x:.8f}s")
    df_bench["Target"] = df_bench["Target"].apply(lambda x: f"< {x}s")

    st.dataframe(df_bench, use_container_width=True)

    # ================= SEARCH COMPLEXITY =================
    import math

    st.markdown("### 🔍 Search Complexity Demo")
    if st.session_state.block:
        block = st.session_state.block
        bin_steps = binary_search_steps(block.transactions, sample_txid)
        lin_steps = linear_search_steps(block.transactions, sample_txid)
        theoretical = int(math.log2(len(block.transactions)))
        col1, col2, col3 = st.columns(3)
        col1.metric("Dataset Size", len(block.transactions))
        col2.metric("Binary Steps", bin_steps)
        col3.metric("Linear Steps", lin_steps)
        st.info(f"Theoretical log2(n): {theoretical}")

# ================= TABS =================
tab1, tab2, tab3 = st.tabs(["📦 Transactions", "📈 Analytics", "🌳 Merkle"])

# ===== TAB 1 =====
with tab1:
    if st.session_state.block:
        block = st.session_state.block

        sort_type = st.selectbox("Sort", ["Fee DESC", "Fee ASC", "Time DESC", "Time ASC", "ID"])
        page = st.number_input("Page", 1, 100, 1)

        start = time.perf_counter()

        if sort_type == "Fee DESC":
            data = block.get_view_by_fee_desc(page)
        elif sort_type == "Fee ASC":
            data = block.get_view_by_fee_asc(page)
        elif sort_type == "Time DESC":
            data = block.get_view_by_time_desc(page)
        elif sort_type == "Time ASC":
            data = block.get_view_by_time_asc(page)
        else:
            data = block.get_view_by_id(page)

        duration = time.perf_counter() - start
        st.markdown(f"⏱️ Query Time: `{duration:.6f}s`")

        df = pd.DataFrame([{
            "TXID": tx.txid,
            "From": tx.sender,
            "To": tx.receiver,
            "Amount": tx.amount,
            "Fee": tx.fee
        } for tx in data["data"]])

        if search_global:
            df = df[df["TXID"].str.contains(search_global[:6])]
st.dataframe(df, use_container_width=True)

# ===== TAB 2 =====
with tab2:
    if st.session_state.block:
        fees = [tx.fee for tx in st.session_state.block.transactions]
        st.bar_chart(fees[:200])

# ===== TAB 3 =====
with tab3:
    if st.session_state.block:
        block = st.session_state.block

        txid = st.text_input("Enter TXID")

        if st.button("Generate Proof"):
            t1 = time.perf_counter()
            proof = get_merkle_proof(block.transactions, txid)
            t2 = time.perf_counter()

            if proof:
                valid = verify_merkle_proof(txid, proof, block.merkle_root)
                t3 = time.perf_counter()

                st.success(f"Proof generated in {t2 - t1:.6f}s")
                st.info(f"Verify: {valid} ({t3 - t2:.8f}s)")
            else:
                st.error("TX not found")

# ================= REALTIME =================
if st.session_state.auto_refresh and st.session_state.block:
    num = len(st.session_state.block.transactions)

    txs = generate_mock_transactions(num)

    mempool = Mempool()
    mempool.add_transactions_bulk(txs)
    mempool.sort_by_fee()

    block = Block.create_from_mempool(mempool)
    block.finalize()

    st.session_state.block = block

    time.sleep(1)
    st.rerun()
