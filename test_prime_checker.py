"""Tests for prime_checker.py.  Run:  python test_prime_checker.py"""
import math
import random
import subprocess
import sys
import time

import prime_checker as pc

fails = 0


def expect(cond, msg):
    global fails
    if not cond:
        fails += 1
        print("FAIL:", msg)


def naive_is_prime(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, math.isqrt(n) + 1))


def factor_product(fs):
    out = 1
    for f in fs:
        out *= f
    return out


if __name__ == "__main__":
    t = time.perf_counter()

    # 1. Both primality paths agree with brute force (BPSW forced on small numbers too)
    sieve = set(pc._sieve(300_000))
    for n in range(0, 300_000):
        p = n in sieve
        expect(pc.is_prime(n)[0] == p, f"is_prime({n})")
        if n > 1000 and n % 2:
            expect(pc.is_prime(n, force_bpsw=True)[0] == p, f"bpsw({n})")
    print(f"[1] 0..300,000 vs sieve, both methods: done ({time.perf_counter() - t:.1f}s)")

    # 2. Numbers that fool weaker tests
    strong_psp2 = [2047, 3277, 4033, 4681, 8321, 15841, 29341, 42799, 49141, 52633,
                   3215031751, 3825123056546413051, 318665857834031151167461]
    carmichael = [561, 1105, 1729, 2465, 2821, 6601, 8911, 41041, 825265, 321197185,
                  5394826801, 232250619601, 9746347772161]
    strong_lucas_psp = [5459, 5777, 10877, 16109, 18971, 22499, 24569, 25199, 40309, 58519]
    for n in strong_psp2 + carmichael + strong_lucas_psp:
        expect(not pc.is_prime(n)[0], f"pseudoprime {n} called prime")
        expect(not pc.is_prime(n, force_bpsw=True)[0], f"pseudoprime {n} fooled BPSW")
    # composites just above the deterministic limit, which use the BPSW path
    above = pc.MR_DETERMINISTIC_LIMIT
    for n in range(above, above + 2000):
        expect(pc.is_prime(n)[0] == all(pc._miller_rabin(n, a) for a in pc.MR_BASES + (43, 47, 53, 59, 61, 67, 71))
               if n % 2 else not pc.is_prime(n)[0], f"near-limit {n}")
    print("[2] pseudoprimes / Carmichael numbers / near-limit range: done")

    # 3. Known primes
    mersenne_exps = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281]
    for e in range(2, 2300):
        m = 2 ** e - 1
        expect(pc.is_prime(m)[0] == (e in mersenne_exps), f"2^{e}-1")
    for n in [19999999800000001, 67280421310721, 10 ** 100 + 267, 2 ** 255 - 19]:
        expect(pc.is_prime(n)[0], f"known prime {n}")
    expect(not pc.is_prime((2 ** 61 - 1) * (2 ** 89 - 1))[0], "product of Mersenne primes")
    expect(not pc.is_prime((10 ** 100 + 267) ** 2)[0], "square of big prime")
    print("[3] Mersenne numbers 2^2-1 .. 2^2299-1 and known big primes: done")

    # 4. Factorization finds correct prime factors
    class A:
        workers, yes, no_factor, max_time = 2, True, False, 60

    rng = random.Random(5)
    for _ in range(300):
        n = rng.randrange(2, 10 ** rng.randint(2, 22))
        fs = []
        pending = [n]
        while pending:
            m = pending.pop()
            if m == 1:
                continue
            if pc.is_prime(m)[0]:
                fs.append(m)
                continue
            f = None
            for p in pc.SMALL_PRIMES:
                if m % p == 0:
                    f = p
                    break
            if f is None:
                f, _ = pc._rho_serial(m, 10)
            pending += [f, m // f]
        expect(factor_product(fs) == n and all(pc.is_prime(f)[0] for f in fs), f"factor {n}")
    print("[4] 300 random numbers factored correctly")

    # 5. Measure rho constant: steps per walk / sqrt(p) for single-walk runs
    ratios = []
    for bits in (24, 28, 32):
        for i in range(25):
            p = q = 4
            while not pc.is_prime(p)[0]:
                p = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
            while not pc.is_prime(q)[0] or q == p:
                q = rng.getrandbits(bits + 4) | (1 << (bits + 3)) | 1
            n = pc.mpz(p * q)
            r = random.Random(i)
            steps_total = 0
            while True:
                f, steps = pc._brent(n, pc.mpz(r.randrange(1, int(n) - 1)), pc.mpz(r.randrange(0, int(n))), lambda s: False)
                steps_total += steps
                if f:
                    break
            ratios.append(steps_total / math.sqrt(min(p, q)))
    ratios.sort()
    print(f"[5] rho steps/sqrt(p): median {ratios[len(ratios) // 2]:.2f}, "
          f"mean {sum(ratios) / len(ratios):.2f}, 90th pct {ratios[int(len(ratios) * .9)]:.2f} "
          f"(script uses RHO_C={pc.RHO_C})")

    # 6. Expression parsing
    expect(pc.parse_number("2**127 - 1") == 2 ** 127 - 1, "parse **")
    expect(pc.parse_number("2^89-1") == 2 ** 89 - 1, "parse ^")
    expect(pc.parse_number("1,000,003") == 1000003, "parse commas")
    for bad in ["", "abc", "2**-1", "1.5", "__import__('os')", "10**100000000"]:
        try:
            pc.parse_number(bad)
            expect(False, f"accepted {bad!r}")
        except ValueError:
            pass
    print("[6] parsing: done")

    # 7. Command-line runs (full program, including parallel workers)
    def run(*a, timeout=120):
        r = subprocess.run([sys.executable, "prime_checker.py", *a], capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr

    # Semiprimes of two safe primes (p = 2q+1): p-1 can't crack them, so the
    # parallel rho search has to run. Also compare predicted vs actual time.
    def safe_prime(bits):
        while True:
            q = rng.getrandbits(bits - 1) | (1 << (bits - 2)) | 1
            if pc.is_prime(q)[0] and pc.is_prime(2 * q + 1)[0]:
                return 2 * q + 1

    rate = pc._rho_serial(pc.mpz(safe_prime(40) * safe_prime(40)), 1.0)[1]
    for bits in (40, 44):
        p, q = safe_prime(bits), safe_prime(bits)
        t0 = time.perf_counter()
        out = run(str(p * q), "--workers", "2")
        took = time.perf_counter() - t0
        expect(f"Factors: {min(p, q)} x {max(p, q)}" in out, "cli parallel: " + out)
        pred = pc.rho_seconds(p * q, rate * 0.6, 2, factor_bound=min(p, q))
        print(f"    {bits}-bit safe-prime semiprime: took {took:.1f}s, predicted ~{pred:.1f}s")
    out = run("19999999800000001")
    expect("IS a prime" in out, "cli prime: " + out)
    out = run("2**127-1")
    expect("IS a prime" in out and "Lucas-Lehmer" in out, "cli M127: " + out)
    out = run("10**100+267")
    expect("IS a prime" in out and "BPSW" in out, "cli bpsw: " + out)
    out = run("(2**61-1)*(2**89-1)")
    expect("Factors: 2305843009213693951 x 618970019642690137449562111" in out, "cli pm1/rho: " + out)
    out = run("1000000016000000063")  # 1000000007 * 1000000009, needs the parallel search
    expect("Factors: 1000000007 x 1000000009" in out, "cli parallel: " + out)
    out = run("12")
    expect("Factors: 2^2 x 3" in out, "cli 12: " + out)
    out = run("1")
    expect("NOT prime" in out, "cli 1")
    big = []
    for bits in (200, 201):
        p = 4
        while not pc.is_prime(p)[0]:
            p = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        big.append(p)
    hard = str(big[0] * big[1])  # 120-digit semiprime: must warn & skip non-interactively
    out = run(hard)
    expect("Warning" in out and "not factored" in out and "very unlikely" in out, "cli huge warn: " + out)
    out = run(hard, "--yes", "--max-time", "3")
    expect("search stopped: timeout" in out, "cli timeout: " + out)
    print("[7] command line: done")

    print(f"\n{'ALL PASSED' if fails == 0 else f'{fails} FAILURES'}  ({time.perf_counter() - t:.0f}s)")
    sys.exit(1 if fails else 0)
