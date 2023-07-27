# take utf8 return hex
def utf8ToHex(string):
    return "0x" + string.encode("utf-8").hex()