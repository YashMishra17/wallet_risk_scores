"""
main.py — Compound V2 Wallet Risk Scorer
Fetches wallet data and computes a risk score (0–1000) based on borrow and interest.
"""

import time
import pandas as pd
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.exceptions import TransportServerError

# Configuration
SUBGRAPH_URL = "https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2"
client = Client(
    transport=RequestsHTTPTransport(url=SUBGRAPH_URL, verify=True, retries=3),
    fetch_schema_from_transport=False,
)

def fetch_wallet_batch(wallet_subset):
    """
    Fetch Compound V2 account data for a subset of wallet addresses.
    """
    wallet_str = "[" + ",".join(f'"{w}"' for w in wallet_subset) + "]"
    query = gql(f"""
    {{
      accounts(where: {{ id_in: {wallet_str} }}) {{
        id
        tokens {{
          borrowBalanceUnderlying
          lifetimeBorrowInterestAccrued
        }}
      }}
    }}
    """)
    try:
        return client.execute(query)
    except TransportServerError as e:
        print(f"❌ Error fetching data for batch: {e}")
        return {"accounts": []}

# Load wallets
with open("wallets.txt", encoding="utf-8") as f:
    wallets = [w.strip().lower() for w in f if w.strip()]

scores = []
BATCH_SIZE = 50

for i in range(0, len(wallets), BATCH_SIZE):
    subset = wallets[i : i + BATCH_SIZE]
    print(f"Processing batch {i // BATCH_SIZE + 1}...")
    data = fetch_wallet_batch(subset)
    for acc in data.get("accounts", []):
        total_borrow = sum(float(t["borrowBalanceUnderlying"]) for t in acc["tokens"])
        total_interest = sum(float(t["lifetimeBorrowInterestAccrued"]) for t in acc["tokens"])
        score = max(0, min(1000, int(1000 - (2 * total_borrow + 1.5 * total_interest))))
        scores.append({"wallet_id": acc["id"], "score": score})
    time.sleep(1)

df = pd.DataFrame(scores)
df.to_csv("wallet_risk_scores.csv", index=False)
print("Completed. Output: wallet_risk_scores.csv")
