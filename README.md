# ContextCraft: Claude-Ready Stock Trading MCP Server

> Built by **Arin Dhimar** ✨  
> Claude-integrated 🧐 • Zerodha-powered 📈 • Python 3.10+ ✨

---

## 🚀 Overview

**ContextCraft** is an intelligent, Claude-compatible [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that lets Claude (or any MCP agent) perform live stock trading through **Zerodha KiteConnect**.

Speak naturally. Claude understands:

> “Buy 10 shares of INFY at market price.”  
> “Sell 5 SBIN when it hits 780.”

---

## 🔧 Features

- Place **Market** or **Limit** orders
- Query **symbols by substring**
- Works seamlessly with Claude Desktop
- FastMCP-compatible — zero boilerplate
- Auto-installs `kiteconnect`
- Real-time stock data integration (via Zerodha KiteConnect API)
- Advanced portfolio management (coming soon)
- Full integration with the Claude platform for hands-free trading
- Auto Trade Assistant with conditions like price triggers
- Portfolio Risk Analyzer for better decision-making
- Earnings Calendar & Predictions for proactive trading strategies
- Explain This Stock AI Tool to simplify stock information

---

## 📂 Project Structure

| File            | Purpose                                 |
|-----------------|------------------------------------------|
| `server.py`     | MCP server with trading tools            |
| `main.py`       | Minimal script entrypoint                |
| `.env`          | API key + token (Git ignored)            |
| `pyproject.toml`| Project + dependency declarations        |

---

## 📅 Installation

### 1. Clone the repo
```bash
git clone https://github.com/arindhimar/contextcraft.git
cd contextcraft
```

### 2. Setup virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
uv pip install -e .
```

### 4. Setup `.env`
```env
API_KEY=your_kiteconnect_key
ACCESS_TOKEN=your_valid_access_token
```

---

## ▶️ How to Run

### 🚧 Development
```bash
mcp dev server.py
```

### ⚛️ Production
```bash
uv run python server.py
```

---

## 🧰 Tools Available

### `add(a, b)`
Returns the sum of two numbers.

### `trade(symbol, side, quantity, price?)`
Place a buy/sell order for a stock.


| Param     | Type     | Description                            |
|-----------|----------|----------------------------------------|
| symbol    | `str`    | Substring or full tradingsymbol         |
| side      | `str`    | "buy" or "sell"                         |
| quantity  | `int`    | Number of shares                        |
| price     | `float?` | Leave blank or say "market" for LTP     |


### `portfolio_risk_analyzer()`
Analyzes your portfolio’s risk by evaluating the stocks you hold, their current prices, and their market volatility.

### `explain_stock(symbol)`
Returns a simplified, AI-generated explanation of a stock, including its market trends, news, and predictions.

| Param     | Type     | Description                            |
|-----------|----------|----------------------------------------|
| symbol    | `str`    | Substring or full tradingsymbol         |

### `earnings_calendar()`
Fetches the earnings calendar for the current or upcoming quarter, providing predictions on stock movements based on earnings announcements.

---

## 🌐 Claude Desktop Integration

```json
"mcpServers": {
  "ContextCraft": {
    "command": "uv",
    "args": [
      "--directory", "C:\\Users\\Arin Dhimar\\Documents\\ContextCraft\\mcp-server-contextcraft",
      "run", "python", "server.py"
    ]
  }
}
```

Reload config in Claude Desktop. You're live!

---

## 🚀 Future Ideas

- [ ] Tool to fetch **holdings**
- [ ] View **order history**
- [ ] Fetch **current prices** on demand
- [ ] Add more financial tools (alerts, watchlists, etc.)

---

## 🎓 License

MIT License © [Arin Dhimar](https://github.com/arindhimar)

---

> _Made with coffee, code & context_ ☕️