import hashlib

#get a wallet address on the network

def getAddressFromPublickKey(publickKey):
    data = hashlib.sha3_256(f'{publickKey}'.encode()).hexdigest()
    return '0' + f'{data[:-44]}'



### Tests ###

#print(getAddressFromPublickKey(''))