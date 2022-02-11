import datetime
import json

genesisBlock = json.load(open('src/core/GenesisBlock.json'))
blockKeysList = list(genesisBlock)

print(blockKeysList[6])
print(genesisBlock['tx'][0][0])
#print(genesisBlock['tx'][0]['outputs'])
