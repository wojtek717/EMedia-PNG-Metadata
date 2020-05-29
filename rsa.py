import primeNumberGenerator as pnum
import random
import time
import sys
import math
import functools

class Keys_Collection:
    def __init__(self, publicKey, privateKey):
        self.publicKey = publicKey
        self.privateKey = privateKey

    def savePublicKeyToFile(self, fileName):
        file = open(fileName, "w")
        file.write(str(self.publicKey.n))
        file.write("\n")
        file.write(str(self.publicKey.e))

    def savePrivateKeyToFile(self, fileName):
        file = open(fileName, "w")
        file.write(str(self.privateKey.n))
        file.write("\n")
        file.write(str(self.privateKey.d))

class Public_Key:
    def __init__(self, n, e):
        self.n = n
        self.e = e
    
    def printKey(self):
        print("Public key ---> n=" + str(self.n) + " e=" + str(self.e))

class Private_Key:
    def __init__(self, n, d):
        self.n = n
        self.d = d

    def printKey(self):
        print("Private key ---> n=" + str(self.n) + " d=" + str(self.d))

def nwd(a, b):
    if(a < b):
        tmp = a
        a = b
        b = tmp
    
    while b != 0:
        c = a % b
        a = b
        b = c
    return a

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi

def generate_keys(length):
    sys.setrecursionlimit(10**6) 

    p = pnum.generate_prime_number(length)
    q = pnum.generate_prime_number(length)

    n = p*q
    phi = (p-1)*(q-1)

    e = random.randint(3, phi - 1)
    while nwd(e, phi) != 1:
        e = random.randint(3, phi - 1)

    d = modinv(e, phi)

    publicKey = Public_Key(n, e)
    privateKey = Private_Key(n, d)

    return(Keys_Collection(publicKey, privateKey))

def encryptArray(publicKey, frameLength, data):
    stackedData = []

    frames = math.ceil(len(data) / frameLength)
    
    f = 0
    i = 0
    while f < frames:
        frameDataArray = []
        frameDataArray.clear()

        while i < (frameLength * (f+1)):
            if(i < len(data)):
                numb = data[i] + 300
                frameDataArray.append(numb)
            else:
                frameDataArray.append(600)
            i += 1

        frameData = int("".join(map(str, frameDataArray))) 
        stackedData.append(frameData)
        
        f += 1
    
    encryptedData = encrypt(publicKey, stackedData)
    return encryptedData

def decryptArray(privateKey, frameLength, data):
    decryptedData = decrypt(privateKey, data)
    unStackedData = []

    for stack in decryptedData:
        chStack = str(stack)

        f = 0
        while f < frameLength:
            i = 0
            frame = ""
            while i < 3:
                frame += chStack[(3*f + i)]
                i += 1
            numb = int(frame)
            realNumb = numb - 300

            if(realNumb < 256):
                unStackedData.append(realNumb)
            f += 1
    return unStackedData

def encrypt(publicKey, data):
    encryptedData = []

    for m in data:
        c = pow(m, publicKey.e, publicKey.n)
        encryptedData.append(c)

    return encryptedData

def decrypt(privateKey, data):
    decryptedData = []

    for c in data:
        m = pow(c, privateKey.d, privateKey.n)
        decryptedData.append(m)

    return decryptedData