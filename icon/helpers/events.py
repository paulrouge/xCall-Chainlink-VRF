# Define ANSI escape code constants for text colors
YELLOW = "\033[93m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"  # Reset text color to default

xcallAddress = "cxf4958b242a264fc11d7d8d95f79035e35b21c1bb"

def getEvents(_iconService, _tx):
    _iconService.get_transaction_result(_tx)

    # get the eventlogs from the transaction
    eventLogs = _iconService.get_transaction_result(_tx)["eventLogs"]
    for event in eventLogs:
        if event["scoreAddress"] != xcallAddress:
            continue
        if event["indexed"][0] != "CallMessage(str,str,int,int,bytes)":
            continue
        for key, value in event.items():
            if key == "indexed":
                print(f"{YELLOW}indexed:{RESET}")
                count = 0
                for i in value:
                    print(f"\t{YELLOW}{count}:{RESET} {BLUE}{i}{RESET}")
                    count += 1
                    
            elif key == "data":
                print(f"{YELLOW}data:{RESET}")
                request_id = int(value[0], 16)
                data_hash = value[1]
                print(f"\t{RED}request_id:{RESET} {BLUE}{request_id}{RESET}")
                print(f"\t{RED}data_hash:{RESET} {BLUE}{data_hash}{RESET}")

            else:
                print(f"{YELLOW}{key}:{value}{RESET}")

        print("-"*70)