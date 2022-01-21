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

def hash_sha3(data):
    return hashlib.sha3_256(data).hexdigest()


create_block()
print(hash_sha3(b'Hello World!'))