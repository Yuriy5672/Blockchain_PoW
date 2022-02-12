from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey, PublicKey


def createSignature(privateKey, message):
    privKey = PrivateKey.fromString(privateKey)
    return Ecdsa.sign(message, privKey)

def verifySignature(message, signature, publicKey):
    pubKey = PublicKey.fromString(publicKey)
    return Ecdsa.verify(message, signature, pubKey)

def generatePrivateKey():
    return PrivateKey().toString()

def getPublickKey(privateKey):
    return PrivateKey.fromString(privateKey).publicKey().toString()



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

