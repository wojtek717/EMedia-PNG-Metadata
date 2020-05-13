import primeNumberGenerator as pnum
import random

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

def moduleInverse (a,n):

    a0 = a
    n0 = n
    p0 = 0
    p1 = 1
    q = int(n0 / a0)
    r = n0 % a0

    while r > 0:
        t = p0 - (q * p1)
        if(t>=0):
            t = t % n
        else:
            t = n - ((-t) % n )

        p0 = p1
        p1 = t
        n0 = a0
        a0 = r
        q = int(n0 / a0)
        r = n0 % a0

    return p1

def generate_keys():
    p = pnum.generate_prime_number()
    q = pnum.generate_prime_number()

    n = p*q
    phi = (p-1)*(q-1)

    e = random.randint(3, phi - 1)
    while nwd(e, phi) != 1:
        e = random.randint(3, phi - 1)

    d = moduleInverse(e, phi)

    publicKey = (n, e)
    privateKey = (n, d)