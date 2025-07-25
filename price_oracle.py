class PriceOracle:
    """
    Aggregates and normalizes real-time prices from all venues (CEXs and DEXs).
    Maintains a structure: prices[venue][pair] = {bid, ask, bid_qty, ask_qty, timestamp}
    """
    def __init__(self):
        self.prices = {}

    def update_price(self, venue, pair, bid, ask, bid_qty, ask_qty, timestamp):
        """Update normalized price data for a venue and pair."""
        if venue not in self.prices:
            self.prices[venue] = {}
        self.prices[venue][pair] = {
            'bid': bid,
            'ask': ask,
            'bid_qty': bid_qty,
            'ask_qty': ask_qty,
            'timestamp': timestamp
        }

    def get_price(self, venue, pair):
        """Retrieve normalized price data for a venue and pair."""
        return self.prices.get(venue, {}).get(pair) 