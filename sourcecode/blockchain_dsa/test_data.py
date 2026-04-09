# sourcecode/blockchain_dsa/test_data.py
import random
from sourcecode.blockchain_dsa.utils import generate_mock_transactions

# Cố định seed để dữ liệu nhất quán
random.seed(42)

# Generate 1 lần duy nhất
MOCK_10000_TRANSACTIONS = generate_mock_transactions(n=10000)
MOCK_4000_TRANSACTIONS = MOCK_10000_TRANSACTIONS[:4000]