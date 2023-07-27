from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.wallet.wallet import KeyWallet
from helpers.call import deployContract, reDeployContract
from helpers.call import makeTransaction, makeCall
from helpers.config import *
from helpers.utils import utf8ToHex
from time import sleep
import json
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# dapp on icon berlin is cx091192553d2990245988b6ccd62dbb4f53dcb568

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

# Load God wallet
# god_wallet = KeyWallet.load("../gochain-btp/data/godWallet.json", "gochain")
# god_wallet_address = god_wallet.get_address()
# print(f"God wallet address: {god_wallet_address}")

wallet = KeyWallet.load(os.getenv("WALLET_PATH"), os.getenv("WALLET_PASSWORD"))
wallet_address = wallet.get_address()
print(f"Wallet address: {wallet_address}")

# deploy the xcall contract
# path_contract = "xcall-demo-0.1.0-optimized.jar"
# deployContract(icon_service, nid, god_wallet, path_contract, {})

# address of the deployed dapp contract
DAPP_BSC = "0x2552A1086b103b7a910A11E6470DcB7d6C1798B7" # bsc

# btp address of the deployed dapp contract
btpAddressDApp = f"btp://{BTP_ADDRESS_BSC}/{DAPP_BSC}"
# btpAddressDApp = f"btp://{BTP_ADDRESS_BERLIN}/{DAPP_BSC}"

def makeXCall():
    # yellow print msg
    print("\n\033[93m" + "Making xcall from ICON Berlin..." + "\033[0m")
    print("-"*70)
    
    data = "makeMessage, 0, final message - from ICON Berlin-Net ,0x0"
    data = utf8ToHex(data)

    # params for the sendCallMessage method of the xcall contract
    params = {
        "_to": btpAddressDApp,
        "_data": utf8ToHex("makeMessage, 1, message part 1, 0x0"),
    }

    # get the fee for the xcall call
    fee =  makeCall(icon_service, XCALL_CONTRACT_BERLIN, "getFee", {"_net":BTP_ADDRESS_BSC,"_rollback":False}, wallet)
    value = int(fee, 16)

    # send the xcall transaction 
    # registeres the xcall call on the xcall contract on destination chain 
    # via source chain -> relay -> destination chain
    hash = makeTransaction(icon_service, nid, XCALL_CONTRACT_BERLIN, "sendCallMessage", params, value, wallet)
    print(f'tx: {hash}')
    
    print("trying to get the xcall request id... waiting 10 seconds...\n")
    sleep(10)
    
    # get the tx result
    tx_result = icon_service.get_transaction_result(hash)
    eventlogs = tx_result['eventLogs']

    for event in eventlogs:
        if event['scoreAddress'] == XCALL_CONTRACT_BERLIN:
            if event['indexed'][0] == 'CallMessageSent(Address,str,int,int)':
                request_id = int(event['indexed'][3],16)
                print("\033[94m" + f"reqId: {request_id}" + "\033[0m\n")

    # print in red
    print("\033[93m" + "Check the event log on the xCall Contract on the destination chain!" + "\033[0m\n")

# makeXCall()
