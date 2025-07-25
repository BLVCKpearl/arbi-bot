from config import MIN_PROFIT_THRESHOLD

class ArbitrageDetector:
    """
    Implements net-profit logic and generates trade signals for arbitrage opportunities.
    """
    def __init__(self):
        pass

    def detect_opportunity(self, prices):
        """
        Scan all (buy_venue, sell_venue) pairs for each token/stablecoin pair.
        Calculate gross/net profit and return a list of arbitrage opportunities where net profit > MIN_PROFIT_THRESHOLD.
        For now, fees/gas/slippage are stubbed as zero.
        Output: List of dicts with keys: pair, buy_venue, sell_venue, buy_ask, sell_bid, gross_profit, net_profit
        """
        opportunities = []
        # Gather all unique pairs
        all_pairs = set()
        for venue in prices:
            all_pairs.update(prices[venue].keys())
        # For each pair, check all venue combinations
        for pair in all_pairs:
            venues_with_pair = [v for v in prices if pair in prices[v] and prices[v][pair] is not None]
            for buy_venue in venues_with_pair:
                buy_ask = prices[buy_venue][pair]['ask']
                if buy_ask is None:
                    continue
                for sell_venue in venues_with_pair:
                    if sell_venue == buy_venue:
                        continue
                    sell_bid = prices[sell_venue][pair]['bid']
                    if sell_bid is None:
                        continue
                    gross_profit = sell_bid - buy_ask
                    # Stub: fees, gas, slippage = 0
                    net_profit = gross_profit
                    if net_profit > MIN_PROFIT_THRESHOLD * buy_ask:
                        opportunities.append({
                            'pair': pair,
                            'buy_venue': buy_venue,
                            'sell_venue': sell_venue,
                            'buy_ask': buy_ask,
                            'sell_bid': sell_bid,
                            'gross_profit': gross_profit,
                            'net_profit': net_profit
                        })
        return opportunities

    def calculate_net_profit(self, buy_price, sell_price, fees, gas, slippage):
        """Stub: Calculate net profit for a potential arbitrage trade."""
        return (sell_price - buy_price) - (fees + gas + slippage) 