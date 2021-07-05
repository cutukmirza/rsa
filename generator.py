
# This function generates a generator for Zp where p is a safe prime
# (p-1)/2 is prime, so Phi(p) = p-1 is factorised as 2 * (p-1)/2 (which means
# any number in Zp is of order either 1, 2, (p-1)/2, or p-1).
# Then to find a generator, we just have to find a number, prime with p
# (1 < g < p-1), such that it is neither of order 2 or (p-1)/2. 

def generator(p):
    phi = p-1
    facteurs_phi = [2,phi//2]
    for res in range(2,p):
        fini = True
        if pow(res, 2, p) != 1:
            if pow(res, facteurs_phi[1], p) != 1:
                return res
    return -1;

