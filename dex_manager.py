import time
import random
from config import SUPPORTED_DEXS, BASE_RPC_URL, BSC_RPC_URL, get_dex_private_key
from web3 import Web3
from eth_account import Account
import json

# Minimal ABI for Uniswap V3 exactInputSingle
UNISWAP_V3_ROUTER_ABI = json.loads('[{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"internalType":"struct ISwapRouter.ExactInputSingleParams","name":"params","type":"tuple"}],"name":"exactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"}]')

# Minimal ABI for Uniswap V2-style swapExactTokensForTokens
AERODROME_ROUTER_ABI = json.loads('[{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"}]')

# Uniswap V3 router address on Base
UNISWAP_V3_ROUTER_ADDRESS = '0x5615CDAb10dc425a742d643d949a7F474C01abc4'
# Aerodrome router address on Base
AERODROME_ROUTER_ADDRESS = '0xC5b001dC33727F8F26880B184090D3E252470D45'

# Example token address map for Base
TOKEN_ADDRESS_MAP = {
    'USDT': '0x66e12db8f5c67eAE4e0D3FcbA3b5A7F5b3B5C1B3',
    'USDC': '0xd9AAEC86B65d86f6A7B5b1b0c42F3A0C4c6A2A1b',
    'RIZE': '0x9818B6c09f5ECc843060927E8587c427C7C93583',
    # Add your target token address here
}

class DEXManager:
    """
    Handles EVM DEX logic for Base and BSC chains (Uniswap V3, Aerodrome, PancakeSwap).
    Provides methods for pool reserve fetching, price calculation, and swap execution.
    """
    def __init__(self, test_mode=True):
        self.test_mode = test_mode
        self.web3_base = Web3(Web3.HTTPProvider(BASE_RPC_URL))
        self.private_key = get_dex_private_key()
        self.account = Account.from_key(self.private_key) if self.private_key else None
        self.router_v3 = self.web3_base.eth.contract(address=Web3.to_checksum_address(UNISWAP_V3_ROUTER_ADDRESS), abi=UNISWAP_V3_ROUTER_ABI)
        self.router_aero = self.web3_base.eth.contract(address=Web3.to_checksum_address(AERODROME_ROUTER_ADDRESS), abi=AERODROME_ROUTER_ABI)

    def get_available_pools(self, token_symbol, stablecoins):
        available = {}
        for dex in SUPPORTED_DEXS:
            pairs = [f"{token_symbol}/{stable}" for stable in stablecoins]
            available[dex] = pairs
        return available

    def fetch_all_pool_prices(self, pools_dict):
        result = {}
        for dex, pairs in pools_dict.items():
            result[dex] = {}
            for pair in pairs:
                price = round(random.uniform(0.9, 1.1), 4)
                qty = round(random.uniform(1000, 5000), 2)
                result[dex][pair] = {
                    'bid': price - 0.01,
                    'ask': price + 0.01,
                    'bid_qty': qty,
                    'ask_qty': qty,
                    'timestamp': time.time()
                }
        return result

    def fetch_pool_reserves(self, dex_name, token_symbol, stablecoin):
        pass

    def calculate_price_from_reserves(self, reserves):
        pass

    def execute_swap(self, dex_name, token_symbol, stablecoin, amount, side, slippage):
        """
        Perform a real swap using web3.py for Uniswap V3 or Aerodrome on Base. If test_mode, simulate swap.
        Returns tx result dict or None on error.
        """
        if self.test_mode:
            print(f"[DEX][TEST] Would execute {side.upper()} swap on {dex_name} {token_symbol}/{stablecoin}: amount={amount}, slippage={slippage}")
            return {'status': 'simulated', 'dex': dex_name, 'pair': f'{token_symbol}/{stablecoin}', 'side': side, 'amount': amount, 'slippage': slippage}
        if dex_name == 'uniswap_v3_base':
            try:
                token_in = TOKEN_ADDRESS_MAP.get(token_symbol)
                token_out = TOKEN_ADDRESS_MAP.get(stablecoin)
                if not token_in or not token_out:
                    print(f"[DEX][ERROR] Token address not found for {token_symbol} or {stablecoin}")
                    return None
                fee = 500
                deadline = int(time.time()) + 600
                amount_in = int(amount * 1e18)
                amount_out_min = int(amount_in * (1 - slippage))
                params = {
                    'tokenIn': token_in,
                    'tokenOut': token_out,
                    'fee': fee,
                    'recipient': self.account.address,
                    'deadline': deadline,
                    'amountIn': amount_in,
                    'amountOutMinimum': amount_out_min,
                    'sqrtPriceLimitX96': 0
                }
                tx = self.router_v3.functions.exactInputSingle(params).build_transaction({
                    'from': self.account.address,
                    'value': 0,
                    'nonce': self.web3_base.eth.get_transaction_count(self.account.address),
                    'gas': 500000,
                    'gasPrice': self.web3_base.eth.gas_price
                })
                signed = self.web3_base.eth.account.sign_transaction(tx, private_key=self.private_key)
                tx_hash = self.web3_base.eth.send_raw_transaction(signed.rawTransaction)
                print(f"[DEX] Sent Uniswap V3 swap tx: {tx_hash.hex()}")
                receipt = self.web3_base.eth.wait_for_transaction_receipt(tx_hash)
                print(f"[DEX] Swap confirmed in block {receipt.blockNumber}")
                return {'status': 'success', 'tx_hash': tx_hash.hex(), 'block': receipt.blockNumber}
            except Exception as e:
                print(f"[DEX][ERROR] Swap failed: {e}")
                return None
        elif dex_name == 'aerodrome':
            try:
                token_in = TOKEN_ADDRESS_MAP.get(token_symbol)
                token_out = TOKEN_ADDRESS_MAP.get(stablecoin)
                if not token_in or not token_out:
                    print(f"[DEX][ERROR] Token address not found for {token_symbol} or {stablecoin}")
                    return None
                deadline = int(time.time()) + 600
                amount_in = int(amount * 1e18)
                amount_out_min = int(amount_in * (1 - slippage))
                path = [token_in, token_out] if side == 'buy' else [token_out, token_in]
                tx = self.router_aero.functions.swapExactTokensForTokens(
                    amount_in, amount_out_min, path, self.account.address, deadline
                ).build_transaction({
                    'from': self.account.address,
                    'value': 0,
                    'nonce': self.web3_base.eth.get_transaction_count(self.account.address),
                    'gas': 300000,
                    'gasPrice': self.web3_base.eth.gas_price
                })
                signed = self.web3_base.eth.account.sign_transaction(tx, private_key=self.private_key)
                tx_hash = self.web3_base.eth.send_raw_transaction(signed.rawTransaction)
                print(f"[DEX] Sent Aerodrome swap tx: {tx_hash.hex()}")
                receipt = self.web3_base.eth.wait_for_transaction_receipt(tx_hash)
                print(f"[DEX] Aerodrome swap confirmed in block {receipt.blockNumber}")
                return {'status': 'success', 'tx_hash': tx_hash.hex(), 'block': receipt.blockNumber}
            except Exception as e:
                print(f"[DEX][ERROR] Aerodrome swap failed: {e}")
                return None
        else:
            print(f"[DEX] Swap for {dex_name} not implemented yet.")
            return None 