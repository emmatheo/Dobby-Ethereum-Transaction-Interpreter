from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 🔑 API keys (for local/testing)
ETHERSCAN_API_KEY = "NGGVCAH5UQZZ3AHC89DY27CATXHVJVYK54"
FIREWORKS_API_KEY = "fw_3ZLLQxFyu6eZWtfKBEA6EcUQ"

# Default chain (Ethereum mainnet)
CHAIN_ID = "1"


def get_transaction_v2(tx_hash):
    """
    Try Etherscan v2 / unified API endpoint.
    This is the “modern” style with chain id in path or query.
    """
    url = f"https://api.etherscan.io/v2/chains/{CHAIN_ID}/transactions/{tx_hash}"
    headers = {"Authorization": f"Bearer {ETHERSCAN_API_KEY}"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        # If v2 not found, return None so fallback kicks in
        return None
    except Exception:
        return None


def get_transaction_v1(tx_hash):
    """
    The classic v1 proxy endpoint fallback.
    """
    url = "https://api.etherscan.io/v2/api?chainid=1"
    params = {
        "module": "proxy",
        "action": "eth_getTransactionByHash",
        "txhash": tx_hash,
        "apikey": ETHERSCAN_API_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            return {"error": f"Etherscan returned {resp.status_code}: {resp.text}"}
        data = resp.json()
        if data.get("result") is None:
            return {"error": "❌ Transaction not found or invalid hash."}
        return data
    except Exception as e:
        return {"error": str(e)}


def get_transaction(tx_hash):
    """
    Main wrapper: try v2 first, if v2 fails, fallback to v1.
    """
    v2 = get_transaction_v2(tx_hash)
    if v2:
        # v2 worked
        return v2
    # fallback
    return get_transaction_v1(tx_hash)


def explain_transaction(tx_data):
    """Send Ethereum transaction data to Dobby (Fireworks AI) for deep interpretation."""
    if not tx_data or "error" in tx_data:
        return tx_data.get("error", "❌ Transaction not found or invalid hash.")

    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
        "model": "accounts/sentientfoundation-serverless/models/dobby-mini-unhinged-plus-llama-3-1-8b",
        "max_tokens": 500,
        "temperature": 0.6,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Dobby, an Ethereum transaction interpreter. "
                    "Given the raw transaction JSON, analyze and explain what the transaction does. "
                    "Use plain, beginner-friendly language but include accurate technical insight. "
                    "Break down key details such as:\n"
                    "- What contract or address it interacts with (if visible)\n"
                    "- Whether it’s a token swap, send, mint, stake, approve, or contract interaction\n"
                    "- The value transferred (in ETH or tokens)\n"
                    "- The likely intent behind the transaction\n\n"
                    "Example style:\n"
                    "➡️ This transaction sends 0.2 ETH from wallet A to wallet B.\n"
                    "➡️ This transaction swaps 100 USDC for 0.03 ETH on Uniswap.\n"
                    "➡️ This transaction calls the 'approve' function on a token contract to authorize spending."
                )
            },
            {
                "role": "user",
                "content": f"Interpret this Ethereum transaction and describe what happened:\n\n{tx_data}"
            },
        ],
    }

    headers = {
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=25)
        resp.raise_for_status()
        result = resp.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error from Dobby: {e}\nResponse: {getattr(resp, 'text', '')}"


@app.route("/", methods=["GET", "POST"])
def home():
    explanation = None
    tx_hash = ""

    if request.method == "POST":
        tx_hash = request.form.get("tx_hash", "").strip()
        if not tx_hash:
            explanation = "⚠️ Please enter a transaction hash."
        else:
            tx_data = get_transaction(tx_hash)
            explanation = explain_transaction(tx_data)

    return render_template("index.html", explanation=explanation, tx_hash=tx_hash)


if __name__ == "__main__":
    app.run(debug=True)
