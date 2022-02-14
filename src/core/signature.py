import hashlib

from asyncio.windows_events import NULL
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey, PublicKey
from numpy import byte


def createSignature(privateKey, message):
    privKey = PrivateKey.fromString(privateKey)
    return Ecdsa.sign(message, privKey)._toString()

def verifySignature(message, signature, publicKey):
    pubKey = PublicKey.fromString(publicKey)
    return Ecdsa.verify(message, signature, pubKey)

def generatePrivateKey():
    return PrivateKey().toString()

def getPublickKey(privateKey):
    return PrivateKey.fromString(privateKey).publicKey().toString()

def getSHA3(data):
    return hashlib.sha3_256(f'{data}'.encode()).hexdigest()



#Tests
#Generate keys, create signature, verify signature
def test1():
    privKey = generatePrivateKey() #private key
    pubKey = getPublickKey(privKey) #publick key
    print('private key: ' + privKey)
    print('publick key: ' + pubKey)
    mess = 'Hello world!'
    sign = Ecdsa.sign(mess, PrivateKey.fromString(privKey))
    print('signature: ' + sign.toBase64())
    print('signature verification: ' + str(Ecdsa.verify(mess, sign, PublicKey.fromString(pubKey))))

#Create signature, verify signature
def test2(privKey, message):
    try:
        #Set keys
        privKey = PrivateKey.fromString(privKey)
        pubKey = privKey.publicKey()
        print('private key: ' + privKey.toString())
        print('publick key: ' + pubKey.toString())
        #create signature
        sign = Ecdsa.sign(message, privKey)
        print('signature: ' + sign.toBase64())
        #verify signature
        print('signature verification: ' + str(Ecdsa.verify(message, sign, pubKey)))
    except Exception as e:
        print(e)

#test1()

#test2('b066a18fd30b130d00300acc2e45f39cf08f9836bf1de06976448b83fa815b81', '{"val": "","lock": "","sig": "","txid": ""}')

#print(generatePrivateKey())
#print(getPublickKey(''))

print(createSignature('0011000100110100001011100011000000110010001011100011001000110010', '1' + '77b2cd8f23d0eb962f20f19d2e21261af0a9c54973556d2f366517e97dab9a25' + '0'))
#sign: 3045022100c9311271a98293edaced10fa01c8c3f4aef550b6b26ba5b429aede9ed75e2f560220797b43c9b60a1721eb326c92fca7b2c41c55badecc87298e919ed9ecb14c80f4
#mess: '1' + '77b2cd8f23d0eb962f20f19d2e21261af0a9c54973556d2f366517e97dab9a25' + '0'
print(verifySignature('1' + '77b2cd8f23d0eb962f20f19d2e21261af0a9c54973556d2f366517e97dab9a25' + '0', '3045022100c9311271a98293edaced10fa01c8c3f4aef550b6b26ba5b429aede9ed75e2f560220797b43c9b60a1721eb326c92fca7b2c41c55badecc87298e919ed9ecb14c80f4', 'abf579495c1e08f9f424fcb6aa9993785ac490ea417f2bc20c4bea3c5e759e6ab223564ad18117aed3028d3e6d7f452eaf5c6cf5dc5cbaa5d6ac58a19cbe6bbd'))



