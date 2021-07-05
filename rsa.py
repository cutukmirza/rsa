from random import randint
from sys import maxsize
from math import gcd 
import random
import sympy
from SHACorrection import SHA256

# smallest_512 = 2 ** 511
smallest_512 = 2*20
safe_prime = 507827401995820261511333545881257572755441097565036458224680464191395175561013913788365088969926024668163155965210269844823171005166332796106531437808995987
max_size = 2 ** 40

def isPrime (num):
    for _ in range (10):
        a = randint(2, num - 1)
        # calculate a^(n-1) mod n using fast exponentiation
        res = fast_exponentiation(a, (num - 1), num)
        if (res == 1):
            return False
    return True
    
def generate_prime():
    p = randint(smallest_512, max_size)
    while (isPrime(p) == False):
        p = randint(smallest_512, maxsize)
    return p

def generate_safe_prime():
    # generate a prime number
    p = generate_prime()
    while (isPrime((p-1)/2) == False):
        p = generate_prime()
    return p

def fast_exponentiation_power2(x, y, z):
    # fast exponentiation for x^y mod z
    ex = 1
    res = (x ** ex) % z
    while (ex < y):
        res = (res * res) % z
        ex *= 2
    return res

def rev_string(string):
    new = list(string)
    new = reversed(new)
    return ''.join(map(str, new)) 


#Python program for Extended Euclidean algorithm
def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		gcd, x, y = egcd(b % a, a)
		return (gcd, y - (b//a) * x, x)


def mod_inv(fi_n, e):
    for i in range(e):
        if (fi_n * (i % e) == 1):
            return i
        else:
            return -1
def inverse(x, m):
    a, b, u = 0, m, 1
    while x > 0:
        q = b // x # integer division
        x, a, b, u = b % x, u, x, a - q * u
    if b == 1: 
        return a % m
    

def get_d (fi_n, e):
    # find inverse of fi_n mod e
    d = inverse(fi_n, e)
    return d

"""     a = int(fi_n)
    b = int(e)
    r = [a, b]
    s = [1, 0]
    t = [0, 1]
    qi = r[0] // r[1]
    i = 1
    while(True):
        r.append(r[i-1] - (qi*r[i]))
        if (r[i + 1] == 0):
            break
        s.append(s[i-1] - (qi*s[i]))
        t.append(t[i-1] - (qi*t[i]))
        qi = r[i] // r[i+1]
        i += 1
    d = t[len(t)-1] % fi_n
    return d """

def fast_exponentiation(x, y, z):
    # convert y (exponent) into binary and reverse so 
    # we could navigate it from right to left
    y_bin  = rev_string(str(bin(y)[2:]))

    # go through the binary representation of y
    # and if bit = 1, obtain 2^index of bit
    pow2 = [] 
    for i in range(len(y_bin)):
        if (y_bin[i] == '1'):
            pow2.append(2 ** i)
    
    # obtain multiplication of x ^ all items in pow2
    temp = 1
    for item in pow2:
        temp *= fast_exponentiation_power2(x, item, z)
    
    # result is the multiplication from above mod z
    res = temp % z
    return res

def rsa_sign(message):
    # print(generate_safe_prime())
    # generate 2 prime numbers
    p = generate_prime()
    q = generate_prime()

    while (p == q):
        q = generate_prime()

    # (n, e) is the public key
    n = p * q
    fi_n = (p - 1)*(q - 1)



    e_pool = [3,5,17,257,65537]
    """ for e in range(65537, fi_n):
        if (gcd(e, fi_n) == 1):
            e_pool.append(e)
        if (len(e_pool) == 10):
            break
 """
    e = random.choice(e_pool)

    # (n, d) is the private key
    #d = (1 / e) % fi_n
    d = sympy.mod_inverse(e, fi_n) 
    #d = get_d(fi_n, e)

    # Sign the message
    # encrypt with SHA256
    encrypted = SHA256(message)

    S = fast_exponentiation(encrypted, d, n)
    
    return [S, e, n]

def rsa_verify(message, S, e, n):
    hasha = SHA256(message)
    s_validation = fast_exponentiation(hasha,e,n)

    if (S - s_validation == 0):
        return ("Signature valid")
    else:
        return ("Signature invalid") 

message = "Hello world!"
s_sent = rsa_sign(message)
s_received = rsa_verify(message, s_sent[0], s_sent[1], s_sent[2])
print(s_sent[0])
print(s_received)


e = 23
fi_n = 120

n = 143

d = sympy.mod_inverse(e, fi_n) 
print(d)

encrypted = SHA256(message)
S = fast_exponentiation(encrypted, d, n)
s_validation = fast_exponentiation(encrypted,e,n)
print(encrypted)
print(s_validation)
print((21191913429631680274679 * 65543)%145993439343950937591264)