# fast modular pow
def mod_pow(a, n, m):
    res = 1
    while n > 0:
        # for every 1 in binary representation
        if n % 2 == 1:
            res = (res * a) % m
        # update a
        a = (a * a) % m
        n //= 2
    return res

# returns (d, m, n) where d = ma + nb
def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    d, m, n = extended_gcd(b, a%b)
    return (d, n, m - a//b * n)

def mod_inv(a, p):
    d, m, n = extended_gcd(a, p)
    if d != 1:
        print("gcd(a, p) != 0 !!!")
    return m % p

def legendreSymbol(a: int, p: int) -> int:
    res = pow(a, (p-1) // 2, p)
    # handle python moment
    if res == p - 1:
        return -1
    return res

def tonelli_shanks(a, p):
    """
    Tonelli-Shanks algorithm for finding the square root of a modulo a prime p.
    Returns the smaller of the two roots.
    """
    if legendreSymbol(a, p) != 1:
        return -1

    # Step 1: Write p - 1 as q * 2^s, where q is odd
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1

    # Step 2: Find a non-quadratic residue of p
    z = 2
    while legendreSymbol(z, p) != -1:
        z += 1

    # Step 3: Initialize variables
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)

    # Step 4: Main loop
    while t != 1:
        i, tt = 0, t
        while tt != 1 and i < m:
            tt = (tt * tt) % p
            i += 1

        if i == 0:
            return r

        b = pow(c, pow(2, m - i - 1, p - 1), p)
        r = (r * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i

    return r