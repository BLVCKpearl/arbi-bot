from arbitrage_detector import ArbitrageDetector

def test_detect_opportunity_simple():
    prices = {
        'binance': {
            'RIZE/USDT': {'bid': 10.5, 'ask': 10.0, 'bid_qty': 100, 'ask_qty': 100, 'timestamp': 123456}
        },
        'aerodrome': {
            'RIZE/USDT': {'bid': 10.7, 'ask': 10.2, 'bid_qty': 100, 'ask_qty': 100, 'timestamp': 123456}
        }
    }
    detector = ArbitrageDetector()
    opps = detector.detect_opportunity(prices)
    assert len(opps) > 0
    assert opps[0]['buy_venue'] == 'binance'
    assert opps[0]['sell_venue'] == 'aerodrome'
    assert opps[0]['pair'] == 'RIZE/USDT' 