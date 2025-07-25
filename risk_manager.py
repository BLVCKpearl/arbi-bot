from config import MAX_PORTFOLIO_EXPOSURE, MAX_TRADE_EXPOSURE, MIN_SLIPPAGE, MAX_SLIPPAGE

class RiskManager:
    """
    Enforces slippage control, P&L limits, and circuit breakers for risk management.
    """
    def __init__(self):
        pass

    def check_exposure_limits(self, current_exposure, trade_size):
        """
        Check if trade is within portfolio and per-trade exposure limits.
        Returns True if allowed, False otherwise.
        """
        if current_exposure + trade_size > MAX_PORTFOLIO_EXPOSURE:
            print(f"[RISK] Portfolio exposure exceeded: {current_exposure + trade_size:.2f} > {MAX_PORTFOLIO_EXPOSURE}")
            return False
        if trade_size > MAX_TRADE_EXPOSURE:
            print(f"[RISK] Per-trade exposure exceeded: {trade_size:.2f} > {MAX_TRADE_EXPOSURE}")
            return False
        print(f"[RISK] Exposure check passed.")
        return True

    def validate_slippage(self, estimated_slippage):
        """
        Validate if slippage is within allowed range.
        Returns True if allowed, False otherwise.
        """
        if not (MIN_SLIPPAGE <= estimated_slippage <= MAX_SLIPPAGE):
            print(f"[RISK] Slippage {estimated_slippage:.4f} out of bounds [{MIN_SLIPPAGE}, {MAX_SLIPPAGE}]")
            return False
        print(f"[RISK] Slippage check passed.")
        return True

    def trigger_circuit_breaker(self, pnl, consecutive_losses, liquidity_ok, rpc_ok):
        """
        Trigger circuit breakers based on P&L, losses, liquidity, or RPC health.
        Returns True if trading should be paused, False otherwise.
        """
        if pnl < -0.05:
            print(f"[RISK] Daily drawdown exceeded: {pnl:.2%}")
            return True
        if consecutive_losses >= 3:
            print(f"[RISK] Consecutive loss limit reached: {consecutive_losses}")
            return True
        if not liquidity_ok:
            print(f"[RISK] Liquidity drought detected.")
            return True
        if not rpc_ok:
            print(f"[RISK] RPC/API connectivity issue detected.")
            return True
        print(f"[RISK] Circuit breaker check passed.")
        return False 