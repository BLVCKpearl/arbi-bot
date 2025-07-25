import asyncio
from execution_manager import ExecutionManager

class MockExchangeMgr:
    exchanges = {'binance': True}
    def place_order(self, *args, **kwargs):
        return {'status': 'simulated'}

class MockDEXMgr:
    def execute_swap(self, *args, **kwargs):
        return {'status': 'simulated'}

def test_execute_dual_leg_runs():
    exec_mgr = ExecutionManager(MockExchangeMgr(), MockDEXMgr())
    buy_leg = {'venue': 'binance', 'pair': 'RIZE/USDT', 'side': 'buy', 'price': 10, 'qty': 1}
    sell_leg = {'venue': 'aerodrome', 'pair': 'RIZE/USDT', 'side': 'sell', 'price': 11, 'qty': 1}
    asyncio.run(exec_mgr.execute_dual_leg(buy_leg, sell_leg)) 