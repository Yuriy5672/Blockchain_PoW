import json
import datetime
import time

from blockchain import blockchain
from asyncio.windows_events import NULL


block_scheme = json.load(open('src/core/block_structure.json'))
tx_scheme = json.load(open('src/core/tx_structure.json'))
node_version = json.load(open('src/core/properties.json'))['version']

def validation(block_json):
    #get keys & values
    block_keys = block_json.keys()
    block_values = block_json.values()
    scheme_keys = block_scheme.keys()

    #check operations
    #structure
    #!except
    i = 0
    while i < 8:
        if(block_keys[i] != scheme_keys[i] or block_values[i] == '' or block_values[i] == NULL):
            print('The structure of the block header is broken!')
            return False
        i += 1
        
    #version
    try:
        if int(block_values['version'], 2) != node_version:
            print('Outdated version block!')
            return False
    except Exception:
        print('Error in the "version" field!')
        return False

    #prevBlockHash
    try:
        if block_values['prevBlockHash'] != blockchain.get_lastblock()['blockHash']:
            print('prevBlockHash does not match the hash of the previous block!')
            return False
    except Exception:
        print('An error occurred when comparing block hashes!')
        return False

    #timestamp
    try:
        #check block time
        block_timestamp = datetime.datetime.fromtimestamp(float(block_values['timestamp']))
        current_timestamp = time.time()                                    #(1 block = ~2 min)
        if block_timestamp >= current_timestamp: #or block_time > current_time - datetime.timedelta(minutes = 20)
            print('Timestamp is specified incorrectly!')
            return False
    except Exception:
        print('Error checking timestamp! The format may be incorrect.')
        return False

    #get tx
    try:
        tx_arr = block_values['tx']
    except Exception:
        print('Transaction receipt error!')
        return False

    #merkleRoot
    

    #Proof of Work check
    try:
        print()
    except Exception:
        print()
        
        #target 
        #nonce
        #equal local & block hash
        #blockHash

    #return "True"

    #tx
        #...

    print('validation passed successfully ' + block_json['blockHash'])
    return True

validation(json.load(open('src/core/GenesisBlock2.json')))
#validation(json.load(open('src/core/GenesisBlock.json')))
