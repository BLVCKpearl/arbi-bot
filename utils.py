def construct_pair(token_symbol, stablecoin):
    """Constructs a trading pair string (e.g., RIZE/USDT)."""
    return f"{token_symbol}/{stablecoin}"


def get_token_metadata(token_symbol):
    """Stub: Fetch token metadata (decimals, address, etc.)."""
    pass


def is_supported_stablecoin(symbol, stablecoins):
    """Check if a symbol is a supported stablecoin."""
    return symbol.upper() in [s.upper() for s in stablecoins] 