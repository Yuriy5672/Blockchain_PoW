import json
import datetime
import time

from block import hash_sha3
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
    except Exception as e:
        print('Version check. ' + e)
        return False

    #prevBlockHash
    try:
        if block_values['prevBlockHash'] != blockchain.get_lastblock()['blockHash']:
            print('prevBlockHash does not match the hash of the previous block!')
            return False
    except Exception as e:
        print('Previous block hash check. ' + e)
        return False

    #timestamp
    try:
        #check block time
        block_timestamp = datetime.datetime.fromtimestamp(float(block_values['timestamp']))
        current_timestamp = time.time()                                    #(1 block = ~2 min)
        if block_timestamp >= current_timestamp: #or block_time > current_time - datetime.timedelta(minutes = 20)
            print('Timestamp is specified incorrectly!')
            return False
    except Exception as e:
        print('Timestamp check. ' + e)
        return False

    #get tx
    try:
        tx_arr = block_values['tx']
    except Exception as e:
        print(e)
        return False

    #Proof of Work check
    try:
        #difficulty
        #get current difficulty
        if bytes(block_values['difficulty']) < json.load(open('src/core/properties.json'))['difficulty']:
            print('Field "difficulty" of the block is less than the installed one!')
            return False

        #nonce
        if type(block_values['nonce']) != int:
            print('"nonce" field type is not equal to int')
            return False

        #equal local & block hash
        #blockHash == double hashing sha3 (str( tx list + version + prevBlockHash + timestamp + difficulty + nonce))
        blockHash = hash_sha3(str(block_values['tx']) + str(block_values['version']) + str(block_values['prevBlockHash'])  
        + str(block_values['timestamp']) + str(block_values['difficulty']) + str(block_values['nonce']))

        if str(blockHash) != str(block_values['blockHash']):
            print('Invalid block hash!')
            return False

    except Exception as e:
        print('PoW check. ' + e)
        return False

    #tx
    try:
        print()
        #...
    except Exception as e:
        print('Transactions check. ' + e)
        return False

    print('validation passed successfully ' + block_values['blockHash'])

    #if all OK return "True"
    return True

validation(json.load(open('src/core/GenesisBlock2.json')))
#validation(json.load(open('src/core/GenesisBlock.json')))
