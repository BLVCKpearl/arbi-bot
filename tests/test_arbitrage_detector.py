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
    opportunities = detector.detect_opportunity(prices)
    assert len(opportunities) > 0
    assert opportunities[0]['buy_venue'] == 'binance'
    assert opportunities[0]['sell_venue'] == 'aerodrome'
    assert opportunities[0]['pair'] == 'RIZE/USDT'
