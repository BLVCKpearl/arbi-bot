import argparse
import asyncio
import os
from config import STABLECOINS
from exchange_manager import ExchangeManager
from dex_manager import DEXManager
from price_oracle import PriceOracle
from arbitrage_detector import ArbitrageDetector
from execution_manager import ExecutionManager
from risk_manager import RiskManager
from position_manager import PositionManager
from alerts import Alerts

POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", "2.0"))  # seconds

async def arbitrage_loop(target_token):
    # Set test_mode=True for safety; set to False for real trading
    exchange_mgr = ExchangeManager(test_mode=True)
    dex_mgr = DEXManager(test_mode=True)
    price_oracle = PriceOracle()
    arb_detector = ArbitrageDetector()
    exec_mgr = ExecutionManager(exchange_mgr, dex_mgr)
    risk_mgr = RiskManager()
    pos_mgr = PositionManager()
    alerts = Alerts()

    cex_pairs = exchange_mgr.get_available_pairs(target_token, STABLECOINS)
    dex_pools = dex_mgr.get_available_pools(target_token, STABLECOINS)

    print("[LOOP] Starting continuous arbitrage loop...")
    try:
        while True:
            try:
                # Real-time price aggregation
                cex_prices = exchange_mgr.fetch_all_order_books(cex_pairs)
                for ex, pairs in cex_prices.items():
                    for pair, data in pairs.items():
                        if data:
                            price_oracle.update_price(ex, pair, data['bid'], data['ask'], data['bid_qty'], data['ask_qty'], data['timestamp'])
                dex_prices = dex_mgr.fetch_all_pool_prices(dex_pools)
                for dex, pairs in dex_prices.items():
                    for pair, data in pairs.items():
                        if data:
                            price_oracle.update_price(dex, pair, data['bid'], data['ask'], data['bid_qty'], data['ask_qty'], data['timestamp'])
                # Arbitrage detection
                opportunities = arb_detector.detect_opportunity(price_oracle.prices)
                if opportunities:
                    print(f"[LOOP] Found {len(opportunities)} arbitrage opportunities.")
                    for opp in opportunities:
                        print(f"  {opp['pair']}: Buy on {opp['buy_venue']} at {opp['buy_ask']} | Sell on {opp['sell_venue']} at {opp['sell_bid']} | Net Profit: {opp['net_profit']:.6f}")
                    # Simulate execution of the first opportunity with risk checks
                    opp = opportunities[0]
                    buy_leg = {
                        'venue': opp['buy_venue'],
                        'pair': opp['pair'],
                        'side': 'buy',
                        'price': opp['buy_ask'],
                        'qty': 1  # Simulated quantity
                    }
                    sell_leg = {
                        'venue': opp['sell_venue'],
                        'pair': opp['pair'],
                        'side': 'sell',
                        'price': opp['sell_bid'],
                        'qty': 1  # Simulated quantity
                    }
                    # Dummy values for risk checks
                    current_exposure = 0.0
                    trade_size = 0.05  # 5% of portfolio
                    estimated_slippage = 0.01  # 1%
                    pnl = 0.0  # No loss
                    consecutive_losses = 0
                    liquidity_ok = True
                    rpc_ok = True
                    if (risk_mgr.check_exposure_limits(current_exposure, trade_size) and
                        risk_mgr.validate_slippage(estimated_slippage) and
                        not risk_mgr.trigger_circuit_breaker(pnl, consecutive_losses, liquidity_ok, rpc_ok)):
                        print("[LOOP] All risk checks passed. Executing...")
                        await exec_mgr.execute_dual_leg(buy_leg, sell_leg)
                        print("[LOOP] Managing positions after execution...")
                        pos_mgr.manage_open_positions()
                        pos_mgr.rebalance()
                        msg = (f"Arbitrage Executed!\nPair: {opp['pair']}\nBuy: {opp['buy_venue']} @ {opp['buy_ask']}\n"
                               f"Sell: {opp['sell_venue']} @ {opp['sell_bid']}\nNet Profit: {opp['net_profit']:.6f}")
                        alerts.send_telegram_alert(msg)
                    else:
                        print("[LOOP] Trade blocked by risk management.")
                else:
                    print("[LOOP] No arbitrage opportunities found.")
                await asyncio.sleep(POLL_INTERVAL)
            except Exception as e:
                print(f"[LOOP][ERROR] {e}")
                await asyncio.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("[LOOP] Stopping arbitrage loop (KeyboardInterrupt).")


def main():
    parser = argparse.ArgumentParser(description="Aggressive Multi-Venue Pure Arbitrage Bot v2")
    parser.add_argument('--token', type=str, required=True, help='Primary token symbol to arbitrage (e.g., RIZE)')
    args = parser.parse_args()
    target_token = args.token.upper()
    print(f"[INFO] Selected target token: {target_token}")
    print(f"[INFO] Stablecoins: {STABLECOINS}")
    asyncio.run(arbitrage_loop(target_token))

if __name__ == "__main__":
    main()
