from mcp.server.fastmcp import FastMCP
from kiteconnect import KiteConnect
from kiteconnect.exceptions import InputException
import logging
from typing import Union
from dotenv import load_dotenv
import os


load_dotenv() 


API_KEY = os.getenv("API_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")   
EXCHANGE = "NSE"
PRODUCT = "MIS"
VARIETY = "regular"

mcp = FastMCP("ContextCraft", dependencies=["kiteconnect"])

def get_kite_client():
    kite = KiteConnect(api_key=API_KEY)
    kite.set_access_token(ACCESS_TOKEN)
    return kite

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def trade(symbol: str, side: str, quantity: int, price: Union[float, str, None] = None) -> dict:
    """
    Place a trade.
    - If price is "market" or None, places market order.
    - If price is a number, places limit order.
    - Fetches current price from LTP if needed.
    """
    kite = get_kite_client()

    instruments = kite.instruments(EXCHANGE)
    matches = [inst for inst in instruments if symbol.upper() in inst["tradingsymbol"]]
    if not matches:
        return {"status": "error", "message": f"No matching stock for '{symbol}' on {EXCHANGE}"}

    inst = matches[0]
    tradingsymbol = inst["tradingsymbol"]
    token = inst["instrument_token"]

   if price is None or (isinstance(price, str) and "market" in price.lower()):
        order_type = kite.ORDER_TYPE_MARKET
        price_param = {}
    else:
        try:
            price_val = float(price)
            order_type = kite.ORDER_TYPE_LIMIT
            price_param = {"price": price_val}
        except ValueError:
            return {"status": "error", "message": f"Invalid price value: {price}"}

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
        return {
            "status": "success",
            "order_id": order_id,
            "symbol": tradingsymbol,
            "type": side,
            "qty": quantity,
            "price": price_param.get("price", "market")
        }
    except InputException as e:
        return {"status": "error", "message": str(e)}

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
