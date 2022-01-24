import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from ethereum_gasprice import AsyncGaspriceController
from ethereum_gasprice.providers import EtherscanProvider
from web3 import Web3

load_dotenv()

log_folder = Path.home().joinpath("logs")
Path(log_folder).mkdir(parents=True, exist_ok=True)
log_file = log_folder.joinpath("Crepitus.log")

if not log_file.exists():
    open(log_file, "w").close()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler(log_file, mode="w+"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

# Discord settings
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Ethereum settings
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHEREUM_MAIN_NET_URL = os.getenv("ETHEREUM_MAIN_NET_URL")
gas_tracker = AsyncGaspriceController(
    settings={EtherscanProvider.title: ETHERSCAN_API_KEY},
)
web3 = Web3(Web3.HTTPProvider(ETHEREUM_MAIN_NET_URL, request_kwargs={"timeout": 60}))
ETH_USDC = web3.toChecksumAddress("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
ETH_WETH = web3.toChecksumAddress("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
UNISWAP_ROUTER_ADDRESS = web3.toChecksumAddress(
    "0xf164fC0Ec4E93095b804a4795bBe1e041497b92a"
)
