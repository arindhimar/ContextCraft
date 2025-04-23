from mcp.server.fastmcp import FastMCP
from kiteconnect import KiteConnect
from kiteconnect.exceptions import InputException
import requests
from typing import Union
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "indian-stock-exchange-api2.p.rapidapi.com")
EXCHANGE = "NSE"
PRODUCT = "MIS"
VARIETY = "regular"

mcp = FastMCP("ContextCraft", dependencies=["kiteconnect"])

def get_kite_client():
    kite = KiteConnect(api_key=API_KEY)
    kite.set_access_token(ACCESS_TOKEN)
    return kite

def call_rapidapi(endpoint: str, params: dict = None) -> Union[dict, list]:
    url = f"https://{RAPIDAPI_HOST}/{endpoint}"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    response = requests.get(url, headers=headers, params=params)
    try:
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def trade(symbol: str, side: str, quantity: int, price: Union[float, str, None] = None) -> dict:
    kite = get_kite_client()
    instruments = kite.instruments(EXCHANGE)
    matches = [inst for inst in instruments if symbol.upper() in inst["tradingsymbol"]]
    if not matches:
        return {"status": "error", "message": f"No matching stock for '{symbol}' on {EXCHANGE}"}

    inst = matches[0]
    tradingsymbol = inst["tradingsymbol"]

    if price is None or (isinstance(price, str) and "market" in price.lower()):
        order_type = kite.ORDER_TYPE_MARKET
        price_param = {}
    else:
        try:
            price_val = float(price)
            order_type = kite.ORDER_TYPE_LIMIT
            price_param = {"price": price_val}
        except ValueError:
            return {"status": "error", "message": f"Invalid price: {price}"}

    order_data = {
        "variety": VARIETY,
        "exchange": EXCHANGE,
        "tradingsymbol": tradingsymbol,
        "transaction_type": kite.TRANSACTION_TYPE_BUY if side.lower() == "buy" else kite.TRANSACTION_TYPE_SELL,
        "quantity": quantity,
        "order_type": order_type,
        "product": PRODUCT,
        **price_param
    }

    try:
        order_id = kite.place_order(**order_data)
        return {"status": "success", "order_id": order_id}
    except InputException as e:
        return {"status": "error", "message": str(e)}

# Portfolio tools
@mcp.tool()
def get_holdings() -> list:
    return get_kite_client().holdings()

@mcp.tool()
def get_positions() -> list:
    return get_kite_client().positions()["net"]

@mcp.tool()
def get_order_history() -> list:
    return get_kite_client().orders()[-10:]

# === Functional RapidAPI Endpoints ===

@mcp.tool()
def industry_search(query: str) -> Union[dict, list]:
    return call_rapidapi("industry_search", {"query": query})

@mcp.tool()
def mutual_fund_search(query: str) -> Union[dict, list]:
    return call_rapidapi("mutual_fund_search", {"query": query})

@mcp.tool()
def get_commodities() -> Union[dict, list]:
    return call_rapidapi("commodities")

@mcp.tool()
def get_price_shockers() -> Union[dict, list]:
    return call_rapidapi("price_shockers")

@mcp.tool()
def get_bse_most_active() -> Union[dict, list]:
    return call_rapidapi("BSE_most_active")

@mcp.tool()
def get_nse_most_active() -> Union[dict, list]:
    return call_rapidapi("NSE_most_active")

@mcp.tool()
def get_stock_target_price(stock_id: str) -> Union[dict, list]:
    return call_rapidapi("stock_target_price", {"stock_id": stock_id})

@mcp.tool()
def get_historical_data(stock_name: str, period: str = "1m", filter_type: str = "price") -> Union[dict, list]:
    return call_rapidapi("historical_data", {
        "stock_name": stock_name,
        "period": period,
        "filter": filter_type
    })

@mcp.tool()
def get_historical_stats(stock_name: str, stats: str = "quarter_results") -> Union[dict, list]:
    return call_rapidapi("historical_stats", {
        "stock_name": stock_name,
        "stats": stats
    })

@mcp.tool()
def get_stock_forecasts(stock_id: str, measure_code: str = "EPS", period_type: str = "Annual", data_type: str = "Actuals", age: str = "Current") -> Union[dict, list]:
    return call_rapidapi("stock_forecasts", {
        "stock_id": stock_id,
        "measure_code": measure_code,
        "period_type": period_type,
        "data_type": data_type,
        "age": age
    })

@mcp.tool()
def get_trending_stocks() -> Union[dict, list]:
    return call_rapidapi("trending")

@mcp.tool()
def get_52_week_high_low() -> Union[dict, list]:
    return call_rapidapi("fetch_52_week_high_low_data")

@mcp.tool()
def auto_trade_signal(stock_name: str, condition: str, threshold: float) -> dict:
    """
    Trigger a signal when a condition matches the stock's recent data.
    E.g., Drop of 5% in price in a day triggers "buy"
    """
    url = "https://indian-stock-exchange-api2.p.rapidapi.com/price_shockers"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"status": "error", "message": "Failed to fetch price shockers"}

    shockers = response.json()
    for stock in shockers:
        if stock_name.lower() in stock['symbol'].lower():
            change = float(stock['change_percentage'].replace("%", ""))
            if condition.lower() == "drop" and change <= -threshold:
                return {"signal": "buy", "reason": f"{stock_name} dropped by {change}%"}

            elif condition.lower() == "rise" and change >= threshold:
                return {"signal": "sell", "reason": f"{stock_name} rose by {change}%"}

    return {"signal": "hold", "reason": "No trigger conditions met"}


@mcp.tool()
def analyze_portfolio_risk() -> dict:
    """Basic portfolio risk estimation using sector presence."""
    holdings = get_holdings()
    sectors = {}
    for stock in holdings:
        query = {"query": stock["tradingsymbol"]}
        url = "https://indian-stock-exchange-api2.p.rapidapi.com/industry_search"
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": RAPIDAPI_HOST
        }
        response = requests.get(url, headers=headers, params=query)
        if response.status_code == 200:
            data = response.json()
            sector = data[0]['sector'] if data else "Unknown"
            sectors[sector] = sectors.get(sector, 0) + 1

    total = sum(sectors.values())
    analysis = {sector: f"{(count/total)*100:.2f}%" for sector, count in sectors.items()}
    return {"diversification": analysis}


@mcp.tool()
def explain_stock(stock_id: str) -> dict:
    """Summarize a stock using multiple data points: EPS, stats, 52-week highs/lows."""
    explanation = {}

    def fetch(endpoint, params={}):
        url = f"https://{RAPIDAPI_HOST}/{endpoint}"
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": RAPIDAPI_HOST
        }
        return requests.get(url, headers=headers, params=params).json()

    # EPS forecast
    forecast = fetch("stock_forecasts", {
        "stock_id": stock_id,
        "measure_code": "EPS",
        "period_type": "Annual",
        "data_type": "Actuals",
        "age": "Current"
    })

    # Historical stats (quarter results)
    stats = fetch("historical_stats", {
        "stock_name": stock_id,
        "stats": "quarter_results"
    })

    # 52-week data
    highlow = fetch("fetch_52_week_high_low_data")

    explanation["EPS Forecast"] = forecast
    explanation["Quarterly Results"] = stats
    explanation["52 Week Range"] = highlow

    return explanation


if __name__ == "__main__":
    mcp.run()

