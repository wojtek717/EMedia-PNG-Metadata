import primeNumberGenerator as pnum
import random

class Keys_Collection:
    def __init__(self, publicKey, privateKey):
        self.publicKey = publicKey
        self.privateKey = privateKey

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

def generate_keys():
    p = pnum.generate_prime_number()
    q = pnum.generate_prime_number()

    print("P:::::")
    print(p)
    print("Q:::::")
    print(q)

    n = p*q
    phi = (p-1)*(q-1)

    print("phi:::::")
    print(phi)

    e = random.randint(3, phi - 1)
    while nwd(e, phi) != 1:
        e = random.randint(3, phi - 1)

    print("e:::::")
    print(e)

    d = modinv(e, phi)

    publicKey = (n, e)
    privateKey = (n, d)

    return(Keys_Collection(publicKey, privateKey))

m = 999
keys = generate_keys()

print("Publiczny klucz:::::")
print(keys.publicKey)
print("Prywatny klucz:::::: ")
print(keys.privateKey)

#szyfrowanie
c = (m**keys.publicKey[1]) % keys.publicKey[0]
print(m**keys.publicKey[1])
print("zaszyfrowane")
print(c)

mm = (c**keys.privateKey[1]) % keys.privateKey[0]
print("rosszyfrowane")
print(mm)

