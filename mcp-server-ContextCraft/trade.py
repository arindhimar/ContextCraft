import logging
import argparse
from kiteconnect import KiteConnect
from kiteconnect.exceptions import InputException

# ─── Configuration ─────────────────────────────────────────────────────────────
API_KEY      = "hell"
ACCESS_TOKEN = "nahh"
EXCHANGE     = "NSE"     
PRODUCT      = "CNC"      
VARIETY      = "regular"  
# ───────────────────────────────────────────────────────────────────────────────

def place_trade(kite, symbol_substr, qty, side, price=None):
    instruments = kite.instruments(EXCHANGE)
    matches = [inst for inst in instruments if symbol_substr in inst["tradingsymbol"]]
    if not matches:
        raise ValueError(f"No instruments found containing “{symbol_substr}” on {EXCHANGE}")

    inst = matches[0]
    tradingsymbol = inst["tradingsymbol"]
    token = inst["instrument_token"]
    logging.info(f"Selected {tradingsymbol} (token {token})")

    if price is None:
        order_type = kite.ORDER_TYPE_MARKET
        price_param = {}
    else:
        order_type = kite.ORDER_TYPE_LIMIT
        price_param = {"price": price}

    params = {
        "variety": VARIETY,
        "exchange": EXCHANGE,
        "tradingsymbol": tradingsymbol,
        "transaction_type": kite.TRANSACTION_TYPE_BUY if side == "buy" else kite.TRANSACTION_TYPE_SELL,
        "quantity": qty,
        "order_type": order_type,
        "product": PRODUCT,
        **price_param
    }

    order_id = kite.place_order(**params)
    return order_id

def main():
    p = argparse.ArgumentParser(description="Place a Kite Connect order")
    p.add_argument("-s","--symbol", required=True, help="Stock symbol or substring")
    p.add_argument("-q","--qty",  type=int, required=True, help="Quantity")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--buy",  action="store_true", help="Place a buy order")
    group.add_argument("--sell", action="store_true", help="Place a sell order")
    p.add_argument("-p","--price", type=float, help="Limit price (omit for market order)")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    kite = KiteConnect(api_key=API_KEY)
    kite.set_access_token(ACCESS_TOKEN)
    logging.info("Kite client ready.")

    prof = kite.profile()
    logging.info(f"User: {prof['user_name']} (UID {prof['user_id']})")

    side = "buy" if args.buy else "sell"
    try:
        order_id = place_trade(kite, args.symbol, args.qty, side, price=args.price)
        logging.info(f"Order successful. ID = {order_id}")
    except (InputException, ValueError) as e:
        logging.error(f"Trade failed: {e}")

if __name__=="__main__":
    main()
