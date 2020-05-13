from random import randrange, getrandbits

# Test if a number is prime
# n - number to test
# k - number of tests
def is_prime(n, k=128):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    
    # Test
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True
    
# length - the length of the number in bits    
def generate_prime_candidate(length):
    p = getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

# length - the length of the number in bits 
def generate_prime_number(length=1024):
    p = 4

    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p