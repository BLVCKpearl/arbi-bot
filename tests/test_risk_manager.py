from risk_manager import RiskManager

def test_check_exposure_limits():
    mgr = RiskManager()
    # Should pass
    assert mgr.check_exposure_limits(0.1, 0.05) is True
    # Exceeds portfolio
    assert mgr.check_exposure_limits(0.3, 0.05) is False
    # Exceeds per-trade
    assert mgr.check_exposure_limits(0.1, 0.2) is False

def test_validate_slippage():
    mgr = RiskManager()
    # Should pass
    assert mgr.validate_slippage(0.01) is True
    # Too low
    assert mgr.validate_slippage(0.0001) is False
    # Too high
    assert mgr.validate_slippage(0.1) is False

def test_trigger_circuit_breaker():
    mgr = RiskManager()
    # All good
    assert mgr.trigger_circuit_breaker(0.0, 0, True, True) is False
    # Drawdown
    assert mgr.trigger_circuit_breaker(-0.1, 0, True, True) is True
    # Consecutive losses
    assert mgr.trigger_circuit_breaker(0.0, 3, True, True) is True
    # Liquidity
    assert mgr.trigger_circuit_breaker(0.0, 0, False, True) is True
    # RPC
    assert mgr.trigger_circuit_breaker(0.0, 0, True, False) is True 