import random
import math


def mod_pow(base : int, exponent : int, modulo : int) -> int:
    res = 1
    while exponent > 0:
        # for every 1 in binary representation
        if exponent % 2 == 1:
            res = (res * base) % modulo
        # update base
        base = (base * base) % modulo
        exponent //= 2
    return res

# returns (d, m, n) where d = ma + nb
def extended_gcd(a : int, b : int) -> tuple[int, int, int]: 
    if b == 0:
        return (a, 1, 0)
    d, m, n = extended_gcd(b, a%b)
    return (d, n, m - a//b * n)

def mod_inv(a : int, mod : int) -> int:
    d, m, n = extended_gcd(a, mod)
    if d != 1:
        print("gcd(a, p) != 0 !!!")
    return m % mod

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

# returns jacobis symbol for (m/n); n is odd
def jacobi(m ,n):
    if m == 1:
        return 1
    if m >= n:
        return jacobi(m % n, n)
    
    if m % 2 == 0:
        if n % 8 == 3 or n % 8 == 5:
            return -jacobi(m/2, n)
        else:
            return jacobi(m/2, n)
        
    if m % 4 == 3 and n % 4 == 3:
        return -jacobi(n, m)
    else:
        return jacobi(n, m)
        
# Miller-rabin primality test for number n with probability 1 - 1/4^k
def miller_rabin_test(n : int, k: int = 20):
    if n <= 3:
        return n != 1

    # write n as 2^r * d + 1
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = mod_pow(a, d, n)
        if x == 1 or x == n - 1:  # n - 1 = -1 (mod n)
            continue

        for _ in range(r - 1):
            x = mod_pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True

def fermat_factor(n : int, max_iterations: int = 10000) -> tuple[int, int]:
    """:returns a tuple of factors of n or (-1, -1) if factoring could not be done"""
    if n % 2 == 0:
        return (2, n // 2)

    s = int(n ** 0.5) + 1
    t = int((s * s - n) ** 0.5)
    it = 0
    while (t * t != s*s - n) and it < max_iterations:
        s += 1
        t = int((s * s - n) ** 0.5)
        it += 1

    p = s + t
    q = s - t

    return (s - t, s + t) if p * q == n else (-1, -1)

def pollards_rho_algorithm(n : int, max_iterations: int = 10000) -> int:
    """returns a factor of n or -1 if factoring could not be done"""
    if n % 2 == 0:
        return 2

    def f(x : int) -> int:
        return (x * x + 1) % n

    x = 2
    y = x
    d = 1
    it = 0
    while d == 1 and it < max_iterations:
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), n)
        it += 1

    return d if d != n else -1