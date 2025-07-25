from price_oracle import PriceOracle

def test_update_and_get_price():
    oracle = PriceOracle()
    oracle.update_price('binance', 'RIZE/USDT', 10, 11, 100, 200, 123456)
    price = oracle.get_price('binance', 'RIZE/USDT')
    assert price['bid'] == 10
    assert price['ask'] == 11
    assert price['bid_qty'] == 100
    assert price['ask_qty'] == 200
    assert price['timestamp'] == 123456
    # Nonexistent
    assert oracle.get_price('binance', 'BTC/USDT') is None 