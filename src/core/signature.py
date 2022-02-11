from email import message
from hashlib import sha256, sha3_256
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey, PublicKey


def createSignature(privateKey, message):
    privKey = PrivateKey.fromString(privateKey)
    return Ecdsa.sign(message, privKey)

def verifySignature(message, signature, publicKey):
    pubKey = PublicKey.fromString(publicKey)
    return Ecdsa.verify(message, signature, pubKey)

def getKeys():
    privateKey = PrivateKey()
    return [privateKey.toString(), privateKey.publicKey().toString()]


#Tests
privKey = getKeys()[0] #private key
pubKey = getKeys()[1] #publick key
print('priv ' + privKey + ' pub ' + pubKey)
mess = 'Hello world'
sign = createSignature(privKey, mess)
print('sign ' + sign._toString())
print(verifySignature(mess, sign, pubKey))