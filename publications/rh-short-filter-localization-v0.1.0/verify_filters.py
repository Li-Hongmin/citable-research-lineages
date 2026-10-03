# SPDX-License-Identifier: Apache-2.0
# Derived finite checker: explicit checks remain active under python -O.
"""Finite diagnostics for polynomial obstruction and Fejer localization. No dependencies."""
import cmath
import json
import math
import platform
from pathlib import Path

def polynomial_from_roots(roots):
    p = [1.0 + 0j]
    for z in roots:
        out = [0j] * (len(p) + 1)
        for i, a in enumerate(p):
            out[i] -= z * a
            out[i + 1] += a
        p = out
    return p

def dft(a):
    m = len(a)
    return [sum((v * cmath.exp(-2j * math.pi * h * x / m) for x, v in enumerate(a))) for h in range(m)]

def convolution(q, a):
    m = len(a)
    return [sum((v * a[(x - j) % m] for j, v in enumerate(q))) for x in range(m)]

def energy(a):
    return sum((abs(v) ** 2 for v in a))

def case(m, positive_frequencies, half_window):
    f = sorted(set(positive_frequencies) | {m - h for h in positive_frequencies})
    s = len(f)
    roots = [cmath.exp(-2j * math.pi * h / m) for h in f]
    p = polynomial_from_roots(roots)
    imaginary_error = max((abs(v.imag) for v in p))
    normalization = max((abs(v.real) for v in p))
    p = [v.real / normalization for v in p]
    a = [0.0] * m
    start = m - 2
    for j, v in enumerate(p):
        a[(start + j) % m] = v
    ah = dft(a)
    band = sum((abs(ah[h]) ** 2 for h in f))
    q = [1.0] * half_window + [-1.0] * half_window
    k = len(q)
    cq = convolution(q, a)
    variance = energy(cq)
    qh = dft(q + [0.0] * (m - k))
    parseval = sum((abs(qh[h] * ah[h]) ** 2 for h in range(m))) / m
    if not s + k - 1 < m:
        raise AssertionError('finite diagnostic check failed')
    if not imaginary_error < 1e-10:
        raise AssertionError('finite diagnostic check failed')
    if not band < 1e-20:
        raise AssertionError('finite diagnostic check failed')
    if not variance > 1e-05:
        raise AssertionError('finite diagnostic check failed')
    if not abs(variance - parseval) < 1e-09 * max(1, variance):
        raise AssertionError('finite diagnostic check failed')
    complement = [h for h in range(m) if h not in f]
    qs = polynomial_from_roots([cmath.exp(-2j * math.pi * h / m) for h in complement])
    scale = max((abs(v) for v in qs))
    qs = [v / scale for v in qs]
    sh = dft(qs + [0j] * (m - len(qs)))
    leakage = max((abs(sh[h]) for h in complement))
    min_active = min((abs(sh[h]) for h in f))
    if not len(qs) == m - s + 1:
        raise AssertionError('finite diagnostic check failed')
    if not leakage < 1e-10:
        raise AssertionError('finite diagnostic check failed')
    if not min_active > 1e-06:
        raise AssertionError('finite diagnostic check failed')
    vector = [complex(math.sin(x * 0.73), math.cos(x * 0.41)) for x in range(m)]
    vh = dft(vector)
    sharp_energy = energy(convolution(qs, vector))
    predicted = sum((abs(sh[h] * vh[h]) ** 2 for h in f)) / m
    if not abs(sharp_energy - predicted) < 1e-09 * max(1, sharp_energy):
        raise AssertionError('finite diagnostic check failed')
    return dict(M=m, F=f, s=s, short_filter_span=k, counterexample_band_energy=band, counterexample_filter_energy=variance, parseval_absolute_error=abs(variance - parseval), real_polynomial_imaginary_residual=imaginary_error, sharp_span=len(qs), sharp_complement_multiplier_max=leakage, sharp_active_multiplier_min=min_active, sharp_energy_identity_error=abs(sharp_energy - predicted), verdict='PASS')

def fejer_case(m, hscale, k):
    if not k < m / 2:
        raise AssertionError('finite diagnostic check failed')
    f = []
    for h in range(m):
        centered = h if h <= m // 2 else h - m
        t = abs(centered) / hscale
        f.append(math.sin(math.pi * (t - 0.5) / 1.5) ** 2 if 0.5 < t < 2 else 0.0)
    q = [0j] * m
    for n in range(-k + 1, k):
        q[n % m] = (1 - abs(n) / k) * sum((f[h] * cmath.exp(2j * math.pi * h * n / m) for h in range(m))) / m
    qh = dft(q)
    kernel = []
    for j in range(m):
        kernel.append(abs(sum((cmath.exp(2j * math.pi * r * j / m) for r in range(k)))) ** 2 / k)
    moment = sum((min(j, m - j) / m * kernel[j] for j in range(m))) / m
    lip = m * max((abs(f[(j + 1) % m] - f[j]) for j in range(m)))
    error = max((abs(qh[h] - f[h]) for h in range(m)))
    averaging_error = max((abs(qh[h] - sum((f[j] * kernel[(j - h) % m] for j in range(m))) / m) for h in range(m)))
    vector = [math.sin(0.51 * x) / m for x in range(m)]
    vh = dft(vector)
    exact_energy = sum((abs(f[h] * vh[h]) ** 2 for h in range(m)))
    local_energy = m * energy(convolution(q, vector))
    norm_difference = abs(math.sqrt(local_energy) - math.sqrt(exact_energy))
    bound = error * math.sqrt(m * energy(vector))
    if not abs(sum(kernel) / m - 1) < 1e-12:
        raise AssertionError('finite diagnostic check failed')
    if not error <= lip * moment + 1e-12:
        raise AssertionError('finite diagnostic check failed')
    if not averaging_error < 1e-11:
        raise AssertionError('finite diagnostic check failed')
    if not norm_difference <= bound + 1e-12:
        raise AssertionError('finite diagnostic check failed')
    if not max((abs(v.imag) for v in q)) < 1e-12:
        raise AssertionError('finite diagnostic check failed')
    return dict(M=m, H=hscale, K=k, filter_span=2 * k - 1, kernel_mass=sum(kernel) / m, discrete_first_moment=moment, multiplier_uniform_error=error, lipschitz_first_moment_bound=lip * moment, discrete_fejer_identity_residual=averaging_error, sqrt_energy_difference=norm_difference, parseval_triangle_bound=bound, verdict='PASS')
result = dict(python=platform.python_version(), purpose='Small finite floating-point diagnostics; proof uses polynomial algebra and analytic Fejer bounds', cases=[case(16, [3, 4], 2), case(24, [4, 5, 6], 3)], fejer_cases=[fejer_case(64, 5, 20), fejer_case(128, 8, 40)], overall='PASS')
print(json.dumps(result, indent=2))
