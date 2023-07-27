import json, requests

def getTrace(tx_hash):
    url_local = "http://localhost:9080/api/v3d"
    url_main = "https://ctz.solidwallet.io/api/v3d"
    
    # test_hash = "0xbed1935c4e3f8ce4615d6dff951bf79adccc468d81d980cf2db5da43c16b50b6"

    request_object = {
        "jsonrpc": "2.0",
        "method": "debug_getTrace",
        "id": 1234,
        "params": {
            "txHash": tx_hash
        }
    }

    response = requests.post(url_local, json=request_object)    
    _json = response.json()
    logs = _json["result"]["logs"]

    only_events = True
    
    # ask user if they want to see all logs or just events
    answer = input("Only show events? (y/n):")
    if answer == "y":
        only_events = True
    elif answer == "n":
        only_events = False
    else:
        print("Invalid input. Only showing events.")

    for l in logs:
        if only_events:
            # print if l contains EVENT
            if "EVENT" in l['msg']:
                print("")
                print(l['msg'])
        else:
            print(l)
        
    print("")

