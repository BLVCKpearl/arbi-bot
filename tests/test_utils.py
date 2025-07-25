from utils import construct_pair, is_supported_stablecoin, get_token_metadata

def test_construct_pair():
    assert construct_pair('RIZE', 'USDT') == 'RIZE/USDT'
    assert construct_pair('BTC', 'USDC') == 'BTC/USDC'

def test_is_supported_stablecoin():
    assert is_supported_stablecoin('USDT', ['USDT', 'USDC']) is True
    assert is_supported_stablecoin('usdc', ['USDT', 'USDC']) is True
    assert is_supported_stablecoin('DAI', ['USDT', 'USDC']) is False

def test_get_token_metadata():
    assert get_token_metadata('RIZE') is None  # stub 