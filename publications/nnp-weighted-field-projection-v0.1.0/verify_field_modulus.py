# SPDX-License-Identifier: Apache-2.0
# Derived finite checker: explicit checks remain active under python -O.
"""Rabin irreducibility check for the finite illustrative computation only."""
p = 1 << 18 | 1 << 7 | 1

def rem(a, b):
    while a.bit_length() >= b.bit_length():
        a ^= b << a.bit_length() - b.bit_length()
    return a

def square(a):
    return rem(sum((1 << 2 * i for i in range(a.bit_length()) if a >> i & 1)), p)

def gcd(a, b):
    while b:
        a, b = (b, rem(a, b))
    return a
x = 2
for i in range(1, 19):
    x = square(x)
    if i in (6, 9):
        value = gcd(x ^ 2, p)
        print(f'Rabin gcd index {i} = {value}')
        if not value == 1:
            raise AssertionError('finite diagnostic check failed')
if not x == 2:
    raise AssertionError('finite diagnostic check failed')
print('Rabin x^(2^18) == x; irreducible polynomial verified')
