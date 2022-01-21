import json
import threading
import time

class blockchain():
    #Current  blockchain
    a_blockchain = []

    #Genesis block
    a_blockchain.append(json.load(open('src/core/GenesisBlock.json')))

    def get_lastblock():
        return blockchain.a_blockchain[len(blockchain.a_blockchain) - 1]

    def get_block(idx):
        if idx < len(blockchain.a_blockchain):
            return blockchain.a_blockchain[idx]

    def start():
        print('Blockchain start')
        threading.Thread(blockchain.test_thread_func())
        #start check new blocks thread

    def test_thread_func():
        print("thread1")
        time.sleep(2)
        print("thread2")
        time.sleep(2)
        print("thread3")
        time.sleep(2)
        print("thread4")
        
    
