from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import CallTransactionBuilder
from iconsdk.builder.transaction_builder import DeployTransactionBuilder
from iconsdk.signed_transaction import SignedTransaction

def makeCall(icon_service, score_address, method, params, wallet):
    call = CallBuilder().from_(wallet.get_address()) \
        .to(score_address) \
        .method(method) \
        .params(params) \
        .build()

    result = icon_service.call(call)
    return result

def makeTransaction(icon_service,nid, score_address, method, params, value, wallet):
    txObj = CallTransactionBuilder() \
        .from_(wallet.get_address()) \
        .to(score_address) \
        .step_limit(100_000_000_000) \
        .nid(nid) \
        .nonce(100) \
        .version(3) \
        .value(value) \
        .method(method) \
        .params(params) \
        .build()
    
    signed_transaction = SignedTransaction(txObj, wallet)
    tx_hash = icon_service.send_transaction(signed_transaction)
    
    return tx_hash

def deployContract(icon_service, nid, wallet, filename, params):

    # Ask user for yes or no to continue
    verify = input("Are you sure you want to deploy this contract? (y/n): ")
    if verify != "y":
        print("Aborting...")
        return

    # Generates an instance of transaction for deploying SCORE.
    transaction = DeployTransactionBuilder()\
        .from_(wallet.get_address())\
        .to("cx"+"0"*40)\
        .step_limit(100_000_000_000)\
        .nid(nid)\
        .nonce(100)\
        .content_type("application/java")\
        .content(getBytesFile(filename))\
        .params(params)\
        .build()
    
    # Returns the signed transaction object having a signature
    signed_transaction = SignedTransaction(transaction, wallet)
    tx = icon_service.send_transaction(signed_transaction)
    print(tx)

def getBytesFile(filename):
    with open(f'jar/{filename}', "rb") as binary_file:
        # Read the whole file at once
        data = binary_file.read()
    return data

def reDeployContract(icon_service, nid, wallet, to, filename, params):

    # Ask user for yes or no to continue
    verify = input("Are you sure you want to re-deploy this contract? (y/n): ")
    if verify != "y":
        print("Aborting...")
        return

    # Generates an instance of transaction for deploying SCORE.
    transaction = DeployTransactionBuilder()\
        .from_(wallet.get_address())\
        .to("cx"+"0"*40)\
        .step_limit(100_000_000_000)\
        .nid(nid)\
        .to(to)\
        .nonce(100)\
        .content_type("application/java")\
        .content(getBytesFile(filename))\
        .params(params)\
        .build()
    
    # Returns the signed transaction object having a signature
    signed_transaction = SignedTransaction(transaction, wallet)
    tx = icon_service.send_transaction(signed_transaction)
    print(tx)