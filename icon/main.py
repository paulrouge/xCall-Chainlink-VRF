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
DAPP_SEPOLIA = "0x5F326A7Cecb9510355324977901942bf5018d14F"

# btp address of the deployed dapp contract
btpAddressDApp = f"btp://{BTP_ID_SEPOLIA}/{DAPP_SEPOLIA}"

# deployContract(icon_service, nid, wallet, "vrf-0.1.0-optimized.jar", {})
dappBerlin = "cxb0fba7e5c4e7f0ba8c242d92acd80b00a8098dea"
# transferICX(icon_service, nid, wallet, dappBerlin, 1*10**18)

# test
# _hash = makeTransaction(icon_service, nid, dappBerlin, "voteYes", {}, 6089463169230770176, wallet)
# print(f'tx: {_hash}')

# set btp address sepolia dapp on the vrf contract
# _hash = makeTransaction(icon_service, nid, dappBerlin, "setBtpAddressSepoliaDapp", {"_btpAddressSepoliaDapp": btpAddressDApp}, 0, wallet)
# print(f'tx: {_hash}')

# call requestRandomNumber
_hash = makeTransaction(icon_service, nid, dappBerlin, "requestRandomNumber", {}, 6302692849230770176, wallet)
print(f'tx: {_hash}')

def makeXCall():
    # yellow print msg
    print("\n\033[93m" + "Making xcall from ICON Berlin..." + "\033[0m")
    print("-"*70)
    
    data = "helloworld"

    # params for the sendCallMessage method of the xcall contract
    params = {
        "_to": btpAddressDApp,
        "_data": utf8ToHex(data),
    }

    # get the fee for the xcall call
    fee =  makeCall(icon_service, XCALL_CONTRACT_BERLIN, "getFee", {"_net":BTP_ID_SEPOLIA,"_rollback":False}, wallet)
    value = int(fee, 16)

    # send the xcall transaction, will register the xcall call on the xcall contract on destination chain 
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
                '''
                the request id here, is not actually the request id needed to call executeCall with.
                I think we should listen for events on destination and get the on where _reqId == request_id
                and get the data from there, which will hold the actual request id needed to call executeCall with.
                
                sepolia exempla tx: 0xc038503bb0794faec781c55a9a79d7745d9834518759b5a727e4b52c50b8b562
                '''
    # print in red
    print("\033[93m" + "Check the event log on the xCall Contract on the destination chain!" + "\033[0m\n")

# makeXCall()
# getEvents(icon_service, "0x4cbf3ae68f2d6bd993c514d3fdbb66901a76c5a8a3e5b2d4d623f299f1fa7047")

# call executeCall on the xcall contract on the destination chain
def makeExecuteCall():
    # yellow print msg
    print("\n\033[93m" + "Making executeCall from ICON Berlin..." + "\033[0m")
    print("-"*70)
    
    # params for the executeCall method of the xcall contract
    params = {
        "_reqId": 3475,
        "_data": "0x307835",
    }

    # send the executeCall transaction, will execute the xcall call on the xcall contract on destination chain 
    # via source chain -> relay -> destination chain
    hash = makeTransaction(icon_service, nid, XCALL_CONTRACT_BERLIN, "executeCall", params, 0, wallet)
    print(f'tx: {hash}')
    
    print("trying to get the xcall request id... waiting 10 seconds...\n")
    sleep(10)
    
    # get the tx result
    tx_result = icon_service.get_transaction_result(hash)

    print(tx_result)

# makeExecuteCall()