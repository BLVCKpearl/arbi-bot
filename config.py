import os
from dotenv import load_dotenv

load_dotenv()

# Supported CEXs and DEXs
SUPPORTED_CEXS = ["binance", "gateio", "mexc", "kraken"]
SUPPORTED_DEXS = ["uniswap_v3_base", "aerodrome", "pancakeswap_v2_bsc", "pancakeswap_v3_bsc"]

# Configurable stablecoins
STABLECOINS = os.getenv("STABLECOINS", "USDT,USDC").split(",")

# RPC URLs for Base and BSC
BASE_RPC_URL = os.getenv("BASE_RPC_URL")
BSC_RPC_URL = os.getenv("BSC_RPC_URL")

# Minimum net profit threshold (as decimal, e.g., 0.001 for 0.1%)
MIN_PROFIT_THRESHOLD = float(os.getenv("MIN_PROFIT_THRESHOLD", "0.001"))

# Slippage tolerance (as decimal, e.g., 0.005 for 0.5%)
MIN_SLIPPAGE = float(os.getenv("MIN_SLIPPAGE", "0.005"))
MAX_SLIPPAGE = float(os.getenv("MAX_SLIPPAGE", "0.02"))

# Capital exposure limits
MAX_PORTFOLIO_EXPOSURE = float(os.getenv("MAX_PORTFOLIO_EXPOSURE", "0.3"))  # 30%
MAX_TRADE_EXPOSURE = float(os.getenv("MAX_TRADE_EXPOSURE", "0.05"))  # 5%

# API key loaders (CEX, DEX)
def get_cex_api_key(exchange_name):
    return os.getenv(f"{exchange_name.upper()}_API_KEY")
def get_cex_api_secret(exchange_name):
    return os.getenv(f"{exchange_name.upper()}_API_SECRET")
def get_cex_api_passphrase(exchange_name):
    return os.getenv(f"{exchange_name.upper()}_API_PASSPHRASE")
def get_dex_private_key():
    return os.getenv("DEX_PRIVATE_KEY")

# Telegram/email alert keys (optional)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
EMAIL_SMTP_USER = os.getenv("EMAIL_SMTP_USER")
EMAIL_SMTP_PASS = os.getenv("EMAIL_SMTP_PASS")
EMAIL_TO = os.getenv("EMAIL_TO") 