from blockchain_dsa.utils import generate_mock_transactions
from blockchain_dsa.block import Block
from blockchain_dsa.search import sort_transactions_by_txid, binary_search_txid


def main():
    print("DEMO BLOCKCHAIN SEARCH")

    # Tạo dữ liệu
    txs = generate_mock_transactions(10)

    # Tạo block
    block = Block(txs)

    print("Danh sách TXID ban đầu:")
    for tx in block.transactions:
        print(tx.txid[:10], "...")

    # Sort
    sorted_txs = sort_transactions_by_txid(block.transactions)

    print("Sau khi sort:")
    for tx in sorted_txs:
        print(tx.txid[:10], "...")

    # Chọn 1 TXID để tìm
    target = sorted_txs[3].txid

    print("Tìm TXID:", target[:10], "...")

    result = binary_search_txid(sorted_txs, target)

    print("KẾT QUẢ:")
    if result:
        print("Tìm thấy:", result.txid)
    else:
        print("Không tìm thấy")


if __name__ == "__main__":
    main()