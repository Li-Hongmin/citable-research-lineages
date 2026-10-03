# SPDX-License-Identifier: Apache-2.0
# Derived finite checker: explicit checks remain active under python -O.
"""Small polynomial check over F4; no actual RW word or full large field."""

def mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return out

def power(a, n):
    out = 1
    while n:
        if n & 1:
            out = mul(out, a)
        a = mul(a, a)
        n >>= 1
    return out

def add(a, b):
    out = [0] * max(len(a), len(b))
    for i, c in enumerate(a):
        out[i] ^= c
    for i, c in enumerate(b):
        out[i] ^= c
    return out

def product(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, c in enumerate(a):
        for j, d in enumerate(b):
            out[i + j] ^= mul(c, d)
    return out

def evaluate(a, x):
    out = 0
    for c in reversed(a):
        out = mul(out, x) ^ c
    return out

def lagrange(b, u):
    out = [power(b, u - 1 - j) for j in range(u)]
    out[0] ^= 1
    return out

def coefficient(a, i):
    return a[i] if i < len(a) else 0
for mu in (4, 6, 8):
    u = 1 << mu
    s, ell, out = (lagrange(b, u) for b in (0, 1, 2))
    edge = add(s, ell)

    def moments(t):
        return (coefficient(t, u - 1), coefficient(product(s, t), 2 * u - 3), evaluate(t, 0) ^ evaluate(t, 1), coefficient(product(edge, t), 3 * u // 2 - 1))
    if not moments(s) == (1, 0, 1, 1):
        raise AssertionError('finite diagnostic check failed')
    if not moments(out) == (1, 2, 0, 1):
        raise AssertionError('finite diagnostic check failed')
    B, kap = (4 * sum((u ** j for j in range(1, 5))), 4 * u ** 5)
    a, g, h, t = moments(s)
    ao, go, ho, to = moments(out)
    c0 = mul(power(a, 2), power(h, B + kap)) ^ mul(power(g, 2), mul(power(h, B), power(t, kap)))
    c2 = mul(power(ao, 2), power(h, B + kap)) ^ mul(power(go, 2), mul(power(h, B), power(t, kap)))
    ck = mul(power(to, kap), mul(power(g, 2), power(h, B)))
    ct = mul(power(go, 2), mul(power(to, kap), power(h, B)))
    if not (c0, c2, ck, ct) == (1, 2, 0, 3):
        raise AssertionError('finite diagnostic check failed')
    if not c0 ^ c2 ^ ck ^ ct == c0 ^ c2 ^ ct == 0:
        raise AssertionError('finite diagnostic check failed')
    print(f'PASS u={u}: V1 moments=(1,0,1,1), O moments=(1,omega,0,1); c=(1,omega,0,omega^2), P0(1)=P5(1)=0, cT!=0')
print('Canonical Boolean-grid toy only; no actual-source reachability claimed.')
