import json
import hashlib

from blockchain import blockchain
#python -m pip install pysha3

def create_block():
    json_str = json.load(open('src/core/properties.json'))
    ver = json_str['version']
    prevBlockHash = blockchain.get_lastblock()
    print(prevBlockHash)

#Proof of Work 
def findBlockHash(block_json):
    print()

#double hashing sha3
def hash_sha3(data):
    data = hashlib.sha3_256(data).hexdigest()
    print('hash_sha3 iteration 1 : ' + data)
    data = hashlib.sha3_256(b'{data}').hexdigest()
    print('hash_sha3 iteration 2 : ' + data)
    return data


create_block()
print(hash_sha3(b'Hello World!'))