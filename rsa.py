import primeNumberGenerator as pnum
import random
import time
import sys

class Keys_Collection:
    def __init__(self, publicKey, privateKey):
        self.publicKey = publicKey
        self.privateKey = privateKey

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
        print("Public key ---> n=" + str(self.n) + " d=" + str(self.d))

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

def generate_keys():
    sys.setrecursionlimit(10**6) 

    p = pnum.generate_prime_number()
    q = pnum.generate_prime_number()

    n = p*q
    phi = (p-1)*(q-1)

    e = random.randint(3, phi - 1)
    while nwd(e, phi) != 1:
        e = random.randint(3, phi - 1)

    d = modinv(e, phi)

    publicKey = Public_Key(n, e)
    privateKey = Private_Key(n, d)

    return(Keys_Collection(publicKey, privateKey))
    
def encrypt(publicKey, data):
    encryptedData = []

    for m in data:
        c = pow(m, keys.publicKey.e, keys.publicKey.n)
        encryptedData.append(c)

    return encryptedData

def decrypt(privateKey, data):
    decryptedData = []

    for c in data:
        m = pow(c, keys.privateKey.d, keys.privateKey.n)
        decryptedData.append(m)

    return decryptedData



keys = generate_keys()

data = [9, 12, 42, 123]

#szyfrowanie
print("Encrypted Value:::")
e = encrypt(keys.publicKey, data)
print(e)

print("Decrypted Value:::")
print(decrypt(keys.privateKey, e))

print("Given Value:::")
print(data)