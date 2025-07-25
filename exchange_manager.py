import time
import ccxt
from config import SUPPORTED_CEXS, get_cex_api_key, get_cex_api_secret, get_cex_api_passphrase

class ExchangeManager:
    """
    Manages CEX connections using CCXT and (future) WebSocket clients.
    Provides methods to check trading pair availability, fetch order book data, and place orders.
    """
    def __init__(self, test_mode=False):
        self.exchanges = {}
        self.test_mode = test_mode
        self._init_exchanges()

    def _init_exchanges(self):
        for name in SUPPORTED_CEXS:
            api_key = get_cex_api_key(name)
            api_secret = get_cex_api_secret(name)
            api_passphrase = get_cex_api_passphrase(name)
            params = {}
            if api_passphrase:
                params['password'] = api_passphrase
            try:
                exchange_class = getattr(ccxt, name)
                self.exchanges[name] = exchange_class({
                    'apiKey': api_key,
                    'secret': api_secret,
                    **params
                })
            except AttributeError:
                print(f"[WARN] CCXT does not support exchange: {name}")

    def get_available_pairs(self, token_symbol, stablecoins):
        available = {}
        for name, ex in self.exchanges.items():
            try:
                markets = ex.load_markets()
                pairs = []
                for stable in stablecoins:
                    pair = f"{token_symbol}/{stable}"
                    if pair in markets:
                        pairs.append(pair)
                available[name] = pairs
            except Exception as e:
                print(f"[ERROR] Failed to load markets for {name}: {e}")
                available[name] = []
        return available

    def fetch_all_order_books(self, pairs_dict):
        result = {}
        for ex_name, pairs in pairs_dict.items():
            ex = self.exchanges.get(ex_name)
            result[ex_name] = {}
            for pair in pairs:
                try:
                    ob = ex.fetch_order_book(pair)
                    bid, bid_qty = (ob['bids'][0] if ob['bids'] else (None, None))
                    ask, ask_qty = (ob['asks'][0] if ob['asks'] else (None, None))
                    result[ex_name][pair] = {
                        'bid': bid,
                        'ask': ask,
                        'bid_qty': bid_qty,
                        'ask_qty': ask_qty,
                        'timestamp': time.time()
                    }
                except Exception as e:
                    print(f"[ERROR] Failed to fetch order book for {pair} on {ex_name}: {e}")
                    result[ex_name][pair] = None
        return result

    def check_pair_availability(self, token_symbol, stablecoin):
        results = {}
        pair = f"{token_symbol}/{stablecoin}"
        for name, ex in self.exchanges.items():
            try:
                markets = ex.load_markets()
                results[name] = pair in markets
            except Exception as e:
                print(f"[ERROR] Failed to load markets for {name}: {e}")
                results[name] = False
        return results

    def fetch_order_book(self, exchange_name, symbol):
        ex = self.exchanges.get(exchange_name)
        if not ex:
            print(f"[ERROR] Exchange {exchange_name} not initialized.")
            return None
        try:
            return ex.fetch_order_book(symbol)
        except Exception as e:
            print(f"[ERROR] Failed to fetch order book for {symbol} on {exchange_name}: {e}")
            return None

    # WebSocket support (stub)
    def start_websocket(self, exchange_name):
        pass

    def place_order(self, exchange_name, symbol, side, amount, price=None, order_type='limit'):
        """
        Place a real order via CCXT. Supports 'limit' and 'market' orders.
        If test_mode is True, skip real order placement and print simulated order.
        Returns order result dict or None on error.
        """
        ex = self.exchanges.get(exchange_name)
        if not ex:
            print(f"[ORDER] Exchange {exchange_name} not initialized.")
            return None
        if self.test_mode:
            print(f"[ORDER][TEST] Would place {order_type.upper()} {side.upper()} order on {exchange_name} {symbol}: amount={amount}, price={price}")
            return {'status': 'simulated', 'exchange': exchange_name, 'symbol': symbol, 'side': side, 'amount': amount, 'price': price, 'order_type': order_type}
        try:
            if order_type == 'limit':
                order = ex.create_order(symbol, 'limit', side, amount, price)
            elif order_type == 'market':
                order = ex.create_order(symbol, 'market', side, amount)
            else:
                print(f"[ORDER] Unsupported order type: {order_type}")
                return None
            print(f"[ORDER] Placed {order_type.upper()} {side.upper()} order on {exchange_name} {symbol}: amount={amount}, price={price}, result={order}")
            return order
        except Exception as e:
            print(f"[ORDER][ERROR] Failed to place order on {exchange_name} {symbol}: {e}")
            return None 