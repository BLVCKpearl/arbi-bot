from config import STABLECOINS, get_cex_api_key

def test_stablecoins_is_list():
    assert isinstance(STABLECOINS, list)

def test_get_cex_api_key_unknown():
    assert get_cex_api_key('unknown') is None 