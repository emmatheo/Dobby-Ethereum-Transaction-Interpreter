
# 🧠 Dobby — Ethereum Transaction Interpreter  

Dobby is a beginner-friendly **Ethereum transaction analyzer** that explains what’s happening inside any Ethereum transaction hash — powered by **Etherscan API** and **Fireworks AI (Dobby Model)**.  

It helps users understand complex smart contract interactions (like swaps, mints, staking, or approvals) in plain English while keeping the technical accuracy intact.  

---

## 🚀 Features  

- ✅ Fetches Ethereum transaction details via **Etherscan API (v1 + v2 fallback)**  
- ✅ Interprets raw transaction data using **Fireworks AI Dobby model**  
- ✅ Beginner-friendly explanations with accurate context  
- ✅ Simple **Flask web interface** (enter hash → get explanation)  

---

## 🧩 How It Works  

1. User inputs a transaction hash  
2. App queries Etherscan (v2 → fallback to v1 if needed)  
3. Sends transaction JSON to Fireworks AI model  
4. Displays a human-readable interpretation like:  

> ➡️ This transaction swaps 100 USDC for 0.03 ETH on Uniswap.  
> ➡️ This transaction calls the `approve` function on a token contract.  

---

## ⚙️ Setup & Installation  

### 1️⃣ Clone this repository  

```bash
git clone https://github.com/<your-username>/dobby-eth-interpreter.git
cd dobby-eth-interpreter
````

### 2️⃣ Install dependencies

```bash
pip install flask requests
```

### 3️⃣ Add your API keys

Open `app.py` and replace with your own keys:

```python
ETHERSCAN_API_KEY = "your_etherscan_api_key"
FIREWORKS_API_KEY = "your_fireworks_api_key"
```

---

## 🧪 Run the App Locally

```bash
python app.py
```

Then open your browser and go to:
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🖼️ Example Usage

Enter any Ethereum transaction hash, for example:

```
0x5f0e4a1c27b089b6d8d8325ef0c5291d7094318b7d0e7e60226bb2af88c55b7c
```

**Output Example:**

> 🔍 This transaction swaps 0.5 ETH for 1,200 USDC using Uniswap V3 Router.
> It involves a call to `swapExactETHForTokens`, indicating a token swap transaction.

---

## 🧠 Tech Stack

* **Python 3**
* **Flask**
* **Etherscan API (v1 & v2)**
* **Fireworks AI – Dobby Model**

---

## 📡 Deployment

You can deploy this app easily on **Vercel**, **Render**, or **Railway**.

To deploy without Flask (static frontend + backend API), separate your Python backend as an API service and connect it to a frontend form hosted on Vercel.

---

## ⚠️ Notes

* Etherscan API may have rate limits.
* Keep your API keys private (do not commit them).
* Fireworks AI requires a valid API key and access.

---

## 👨‍💻 Author

**timmyy**

* 🔗 [Twitter/X](https://x.com/)
* 💻 [GitHub](https://github.com/emmatheo)
