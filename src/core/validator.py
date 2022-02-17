
import json
import datetime
import time

from block import hash_sha3
from blockchain import blockchain
from signature import verifySignature, getSHA3
from asyncio.windows_events import NULL


block_scheme = json.load(open('src/core/block_structure.json'))
tx_scheme = json.load(open('src/core/tx_structure.json'))
node_version = json.load(open('src/core/properties.json'))['version']

GENESIS_BLOCK_HASH = '66HFJVHS73FD4CMVJ678JUF4DBXFZKKD'
ADDRESS_LENGTH = 21
ADDRESS_FIRST_SYMBOL = '0'
TOTAL_COINS = 105000000 #21 bil * 5
TX_LOCK_LENGTH = 64

def validation(block_json):
    try:
        pass
        #get keys & values
        # block_keys = block_json.keys()
        # block_values = block_json.values()
        # scheme_keys = block_scheme.keys()
    except Exception as e:
        print(e)
        return False
    
    #check operations
    #structure
    #!except
    i = 0
    while i < 7: #7 - fields in block header
        if(block_json.keys() != block_scheme.keys() or block_json.values() == None):
            print('The structure of the block header is broken!')
            return False
        i += 1
        
    #version
    try:
        if str(block_json['version']) != str(node_version):
            print('Outdated version block!')
            return False
    except Exception as e:
        print('Version check. ' + str(e))
        return False

    #prevBlockHash
    try:
        if block_json['prevBlockHash'] != blockchain.get_lastblock()['blockHash']:
            print('prevBlockHash does not match the hash of the previous block!')
            return False
    except Exception as e:
        print('Previous block hash check. ' + str(e))
        return False

    #timestamp
    try:
        #check block time
        block_timestamp = datetime.datetime.fromtimestamp(float(block_json['timestamp']))
        current_timestamp = time.time()                                    #(1 block = ~2 min)
        if block_timestamp >= current_timestamp: #or block_time > current_time - datetime.timedelta(minutes = 20)
            print('Timestamp is specified incorrectly!')
            return False
    except Exception as e:
        print('Timestamp check. ' + str(e))
        return False

    #get tx
    try:
        tx_arr = block_json['tx']
    except Exception as e:
        print(str(e))
        return False

    #Proof of Work check
    try:
        #difficulty
        #get current difficulty
        if bytes(block_json['difficulty']) < json.load(open('src/core/properties.json'))['difficulty']:
            print('Field "difficulty" of the block is less than the installed one!')
            return False

        #nonce
        if type(block_json['nonce']) != int:
            print('"nonce" field type is not equal to int')
            return False

        #equal local & block hash
        #blockHash == double hashing sha3 (str( tx list + version + prevBlockHash + timestamp + difficulty + nonce))
        blockHash = hash_sha3(str(block_json['tx']) + str(block_json['version']) + str(block_json['prevBlockHash'])  
        + str(block_json['timestamp']) + str(block_json['difficulty']) + str(block_json['nonce']))

        if str(blockHash) != str(block_json['blockHash']):
            print('Invalid block hash!')
            return False

    except Exception as e:
        print('PoW check. ' + str(e))
        return False

    #tx
    try:
        i = 0
        bLen = len(block_json['tx'])
        while i < bLen:
            #!!!!!! Implement fields value size checking !!!!!!
            #!!!!!! Implement UTXO verification using UTXO pool !!!!!!
            #check tx fields
            if block_json['tx'][i].keys() != block_scheme['tx'][i].keys(): #block_json['tx'][0].values() == '' or _block_v[i] == NULL
                print('The structure of the "tx" field is broken! The keys do not match the schema.')
                return False
            
            #check tx values
            #check tx version
            if block_json['tx'][i]['version'] != node_version:
                print('The transaction version in the block does not match the current version of the node!')
                return False

            #check UTXO
            #inputs
            #check inputs fields
            if block_json['tx'][i]['inputs'].keys() != block_scheme['tx'][i]['inputs'].keys():
                print('The tx inputs structure is broken. The fields do not match the scheme!')
                return False
            
            #check inputs
            for y in range(len(block_json['tx'][i]['inputs'])):
                #check: convert val to float
                tx_val = float(block_json['tx'][i]['inputs'][y]['val'])
                if tx_val < 0:
                    print('The tx inputs structure is broken. tx cannot have a negative "val".')
                    return False

                #check: val < total_coins
                if tx_val > TOTAL_COINS:
                    print('The tx inputs structure is broken. tx cannot spend more than "total_coins".')
                    return False

                #check: txid != null || is genesis block
                if block_json['tx'][i]['inputs'][y]['txid'] == NULL:
                    if block_json['blockHash'] != GENESIS_BLOCK_HASH:
                        print('The tx inputs structure is broken. The transaction "txid" field must be filled in.')
                        return False


                #check: lock & signature
                if block_json['tx'][i]['inputs'][y]['sig'] == NULL:
                    print('Tx №' + i + ' utxo №' + ' Empty signature field!')
                    return False
                else:
                    lock = block_json['tx'][i]['inputs'][y]['lock']
                    sig = block_json['tx'][i]['inputs'][y]['sig'].split('/')
                    message = str(block_json['tx'][i]['inputs'][y]['val']) + str(block_json['tx'][i]['inputs'][y]['lock']) + str(block_json['tx'][i]['inputs'][y]['txid'])
                    
                    #check publick key hash
                    if lock != getSHA3(sig[1]):
                        print('Tx №' + i + ' utxo №' + y + ' The hash of the public key does not match!')
                        return False
                    
                    #Verification signature
                    if verifySignature(message, sig[0], sig[1]) == False:
                        print('Tx №' + i + ' utxo №' + y + ' Invalid signature!')
                        return False
                y += 1

            #outputs
            #check outputs fields
            if block_json['tx'][i]['outputs'].keys() != block_scheme['tx'][i]['outputs'].keys():
                print('The tx outputs structure is broken. The fields do not match the scheme!')
                return False

            #check outputs
            for y in range(len(block_json['tx'][i]['outputs'])):

                #address symbol & length check
                if(str(block_json['tx'][i]['outputs'][y]['address'])[0] != ADDRESS_FIRST_SYMBOL or len(str(block_json['tx'][i]['outputs'][y]['address'])) != ADDRESS_LENGTH):
                    print('Tx №' + i + ' output №' + y + 'Invalid address format!')
                    return False
                
                #tx val check
                if(block_json['tx'][i]['outputs'][y]['val'] < 0 or block_json['tx'][i]['outputs'][y]['val'] > TOTAL_COINS):
                    print('Tx №' + i + ' output №' + y + '"val" is specified incorrectly!')
                    return False

                #tx lock
                if(len(block_json['tx'][i]['outputs'][y]['lock']) > TX_LOCK_LENGTH):
                    print('Tx №' + i + ' output №' + y + '"lock" character limit exceeded!')
                    return False

                y += 1

            i += 1
        print()
        #...
    except Exception as e:
        print('Transactions check. ' + str(e))
        return False

    print('validation passed successfully ' + block_json['blockHash'])

    #if all OK return "True"
    return True

validation(json.load(open('src/core/GenesisBlock.json')))
#validation(json.load(open('src/core/GenesisBlock.json')))
