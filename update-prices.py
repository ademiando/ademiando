import requests
from datetime import datetime

CRYPTO = ["bitcoin", "ethereum", "solana"]
STOCKS = ["AAPL", "NVDA"]
headers = {"Accept": "application/json"}

# Ambil data harga crypto dari CoinGecko
def fetch_crypto():
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(CRYPTO)}&vs_currencies=usd"
    res = requests.get(url, headers=headers).json()
    return {
        "BTC": f"${res['bitcoin']['usd']:,}",
        "ETH": f"${res['ethereum']['usd']:,}",
        "SOL": f"${res['solana']['usd']:,}",
    }

# Ambil data saham dari Yahoo Finance (via unofficial API)
def fetch_stocks():
    stock_data = {}
    for ticker in STOCKS:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
        res = requests.get(url, headers=headers).json()
        price = res["quoteResponse"]["result"][0]["regularMarketPrice"]
        stock_data[ticker] = f"${price:,.2f}"
    return stock_data

def update_readme(prices):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start = "<!-- PRICES-START -->"
    end = "<!-- PRICES-END -->"
    before, after = content.split(start)
    _, after = after.split(end)

    new_prices = "| Asset | Price |\n|-------|-------|\n"
    for asset, price in prices.items():
        new_prices += f"| {asset} | {price} |\n"
    new_prices += f"\n_Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}_"

    updated = before + start + "\n" + new_prices + "\n" + end + after

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)

if __name__ == "__main__":
    all_prices = fetch_crypto() | fetch_stocks()
    update_readme(all_prices)