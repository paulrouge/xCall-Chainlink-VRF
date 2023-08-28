from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.wallet.wallet import KeyWallet
from helpers.call import makeTransaction, makeCall, deployContract, transferICX
from helpers.config import *
from helpers.utils import utf8ToHex
from time import sleep
import json
import os
from dotenv import load_dotenv
from helpers.events import getEvents

# Load the environment variables from the .env file
load_dotenv()

"""
First set up some configs to connect to the ICON network.
"""

local = "http://localhost:9080"
mainnet = "https://ctz.solidwallet.io" # the mainnet endpoint
lisbon = "https://lisbon.net.solidwallet.io" # the testnet endpoint
berlin = "https://berlin.net.solidwallet.io" # the testnet endpoint

# Creates an IconService instance using the HTTP provider and set a provider.
icon_service = IconService(HTTPProvider(berlin, 3))
nid = 7 # 1 for mainnet, 3 for local , 7 for berlin?

wallet = KeyWallet.load(os.getenv("WALLET_PATH"), os.getenv("WALLET_PASSWORD"))
# wallet_address = wallet.get_address()
# print(f"Wallet address: {wallet_address}")

# address of the deployed dapp contract
DAPP_SEPOLIA = "0x3D80794f07f3585f7eD0CF6c6e180C64762d80a6" # deployed SEPOLIA dapp contract address

if DAPP_SEPOLIA == "":
    print("Please deploy the SEPOLIA dapp contract first.")
    quit()

# btp address of the deployed dapp contract
btpAddressDApp = f"btp://{BTP_ID_SEPOLIA}/{DAPP_SEPOLIA}"

'''
Uncomment; 

- deployContract(icon_service, nid, wallet, "vrf-0.1.0-optimized.jar", {}) and 
- quit() 

to deploy the compiled vrf-0.1.0-optimized.jar from /jar folder
'''
# deployContract(icon_service, nid, wallet, "vrf-0.1.0-optimized.jar", {})
# quit()

dappBerlin = "cx6a60548cbceb3c3491c47e0ce934ca7cf14f05c1" # your deployed dapp contract address

if dappBerlin == "":
    print("Please deploy the SEPOLIA dapp contract first.")
    quit()

'''
Uncomment the function you want to call below
'''

# set btp address sepolia dapp 
# _hash = makeTransaction(icon_service, nid, dappBerlin, "setBtpAddressSepoliaDapp", {"_btpAddressSepoliaDapp": btpAddressDApp}, 0, wallet)
# print(f'tx: {_hash}')

# call requestRandomNumber
# _hash = makeTransaction(icon_service, nid, dappBerlin, "requestRandomNumber", {}, 6302692849230770176, wallet)
# print(f'tx: {_hash}')



