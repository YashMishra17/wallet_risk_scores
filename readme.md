Compound V2 Wallet Risk Scorer

A Python script that fetches wallet data from the Compound V2 protocol via The Graph API and computes a **risk score** for each wallet based on borrowing behavior and accrued interest.

---

##  Features

- Queries Compound V2 subgraph using GraphQL
- Calculates a risk score (0–1000) based on:
  - `borrowBalanceUnderlying`
  - `lifetimeBorrowInterestAccrued`
- Supports up to 100+ wallets in batch mode
- Exports results as `wallet_risk_scores.csv`

---

##  Requirements

- Python 3.9 or later
- VS Code (or any Python-friendly IDE)
- Internet connection (for API access)

---

##  Setup Instructions

1. **Clone the Repo**
   ```bash
   git clone https://github.com/your-username/compound-risk-scorer.git
   cd compound-risk-scorer
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Script**
   ```bash
   python main.py
   ```

5. **Check the Output**
   - A file named `wallet_risk_scores.csv` will be created with wallet addresses and their respective scores.

---

##  File Structure

```
compound-risk-scorer/
│
├── main.py               # Main script (contains full logic)
├── wallet_risk_scores.csv # Output CSV with scores
├── requirements.txt      # Python dependencies
└── README.md             # Project instructions
```

---

##  Scoring Logic

```
score = 1000 - (2 * total_borrow + 1.5 * total_interest)
```

- Score is capped between 0 and 1000.
- If no data is returned (e.g., API fails), mock scores (300–950) are generated.

---
