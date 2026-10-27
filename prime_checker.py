"""
prime_checker.py - fast prime checker and factorizer.

    python prime_checker.py 19999999800000001
    python prime_checker.py "2**127 - 1"
    python prime_checker.py                     (asks for numbers until you type q)

Options:
    --no-factor        only say prime / not prime, don't look for factors
    --max-time SEC     give up factoring after SEC seconds
    --workers N        number of processes for factoring (default: all CPU threads)
    --yes              don't ask before starting very long searches

How it works
  * Primality: trial division by small primes, then Miller-Rabin.
      - below 3.3 * 10^24 the Miller-Rabin bases used make the answer PROVEN.
      - above that it uses BPSW (Miller-Rabin base 2 + strong Lucas test).
        No number has ever been found that fools BPSW, and it is what
        Mathematica, PARI/GP, SymPy etc. use. Takes milliseconds even for
        1000-digit numbers.
  * Factoring (only if the number is composite): Pollard p-1, then Brent's
    variant of Pollard rho, run on every CPU thread in parallel. Before a long
    search it benchmarks your CPU and warns you how long it could take.

Install gmpy2 (pip install gmpy2) to make all the big-number math several
times faster; the script uses it automatically when present.
"""
import argparse
import ast
import math
import multiprocessing as mp
import os
import queue
import random
import sys
import time

try:
    import gmpy2
    from gmpy2 import mpz
    HAVE_GMPY2 = True
except ImportError:  # plain Python ints work too, just slower
    gmpy2 = None
    mpz = int
    HAVE_GMPY2 = False

if hasattr(sys, "set_int_max_str_digits"):  # Python 3.11+ limits int<->str size
    sys.set_int_max_str_digits(0)

gcd = gmpy2.gcd if HAVE_GMPY2 else math.gcd


def _sieve(limit):
    flags = bytearray([1]) * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(limit) + 1):
        if flags[i]:
            flags[i * i::i] = bytearray(len(range(i * i, limit + 1, i)))
    return [i for i, f in enumerate(flags) if f]


SMALL_PRIMES = _sieve(1000)
MR_DETERMINISTIC_LIMIT = 3317044064679887385961981  # Sorenson & Webster 2015
MR_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)

# Brent rho: steps each walk needs ~= RHO_C * sqrt(p / walks) to find a prime
# factor p. Calibrated empirically (see test_prime_checker.py).
RHO_C = 1.9


# --------------------------------------------------------------------------
# Primality
# --------------------------------------------------------------------------

def _is_square(n):
    if HAVE_GMPY2:
        return gmpy2.is_square(n)
    r = math.isqrt(n)
    return r * r == n


def _miller_rabin(n, a):
    """Strong probable-prime test to base a. n odd, > 3."""
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def _jacobi(a, n):
    a %= n
    result = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0


def _strong_lucas(n):
    """Strong Lucas probable-prime test, Selfridge parameters. n odd, not square."""
    D = 5
    while True:
        j = _jacobi(D, n)
        if j == -1:
            break
        if j == 0 and abs(D) != n:
            return False
        D = -D - 2 if D > 0 else -D + 2
    P, Q = 1, (1 - D) // 4

    d, s = n + 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    def half(x):
        x %= n
        return (x + n if x & 1 else x) // 2

    U, V, Qk = mpz(1), mpz(P), mpz(Q % n)
    for bit in bin(d)[3:]:
        U, V = U * V % n, (V * V - 2 * Qk) % n
        Qk = Qk * Qk % n
        if bit == "1":
            U, V = half(P * U + V), half(D * U + P * V)
            Qk = Qk * Q % n
    if U == 0 or V == 0:
        return True
    for _ in range(s - 1):
        V = (V * V - 2 * Qk) % n
        if V == 0:
            return True
        Qk = Qk * Qk % n
    return False


def _lucas_lehmer(p):
    """Proves or disproves that 2^p - 1 is prime (p an odd prime). Used by GIMPS."""
    n = (mpz(1) << p) - 1
    s = mpz(4)
    for _ in range(p - 2):
        s = s * s
        s = (s & n) + (s >> p)  # fast "mod 2^p - 1" using shifts
        s -= 2
        if s < 0:
            s += n
        while s >= n:
            s -= n
    return s == 0


def is_prime(n, force_bpsw=False):
    """Return (prime?, how). how is 'proven' or 'bpsw' for primes."""
    n = mpz(n)
    if n < 2:
        return False, "below 2"
    for p in SMALL_PRIMES:
        if n % p == 0:
            return n == p, "proven"
    if n < 1000 * 1000:
        return True, "proven"
    if n & (n + 1) == 0 and not force_bpsw:  # n = 2^p - 1: Mersenne number
        p = n.bit_length()
        if not is_prime(p)[0]:
            return False, "proven"  # 2^(ab)-1 is divisible by 2^a-1
        return _lucas_lehmer(p), "lucas-lehmer"
    if n < MR_DETERMINISTIC_LIMIT and not force_bpsw:
        return all(_miller_rabin(n, a) for a in MR_BASES), "proven"
    if not _miller_rabin(n, 2) or _is_square(n):
        return False, "proven"
    return _strong_lucas(n), "bpsw"


# --------------------------------------------------------------------------
# Factoring
# --------------------------------------------------------------------------

def _pollard_pm1(n, bound=100_000, time_budget=0.5):
    """Finds a factor p when p-1 has only small prime factors. Cheap, often lucky."""
    t_end = time.perf_counter() + time_budget
    powers = []
    for p in _PM1_PRIMES:
        if p > bound:
            break
        pk = p
        while pk * p <= bound:
            pk *= p
        powers.append(pk)

    for base in (3, 5, 7):  # several bases: one can have tiny order mod both factors
        a = saved = mpz(base)
        saved_i = 0
        for i, pk in enumerate(powers):
            a = pow(a, pk, n)
            if i % 200 == 199 or i == len(powers) - 1:
                g = gcd(a - 1, n)
                if g == 1:
                    saved, saved_i = a, i + 1
                    if time.perf_counter() > t_end:
                        return None
                    continue
                if g < n:
                    return int(g)
                # both factors appeared in the same batch: redo it one prime at a time
                a = saved
                for pk2 in powers[saved_i:i + 1]:
                    a = pow(a, pk2, n)
                    g = gcd(a - 1, n)
                    if 1 < g < n:
                        return int(g)
                    if g == n:
                        break
                break  # this base failed; try the next one
        else:
            return None  # finished with gcd 1: no smooth p-1 factor
    return None


_PM1_PRIMES = _sieve(100_000)


def _brent(n, c, y, should_stop, m=256):
    """One Brent-rho walk. Returns (factor or None, steps)."""
    g = q = r = mpz(1)
    x = ys = y
    steps = 0
    while g == 1:
        x = y
        j = 0
        while j < r:
            k = min(m, r - j)
            for _ in range(k):
                y = (y * y + c) % n
            j += k
            steps += k
            if should_stop(steps):
                return None, steps
        j = 0
        while j < r and g == 1:
            ys = y
            k = min(m, r - j)
            for _ in range(k):
                y = (y * y + c) % n
                q = q * abs(x - y) % n
            g = gcd(q, n)
            j += k
            steps += k
            if should_stop(steps):
                return None, steps
        r *= 2
    if g == n:  # overshot inside the last batch: step back one at a time
        while True:
            ys = (ys * ys + c) % n
            g = gcd(abs(x - ys), n)
            if g > 1:
                break
    return (int(g) if g != n else None), steps


def _rho_serial(n, time_budget, seed=1):
    """Quick single-process attempt; also measures steps/second on this CPU."""
    n = mpz(n)
    rng = random.Random(seed)
    ni = int(n)
    t0 = time.perf_counter()
    t_end = t0 + time_budget
    total = 0
    while True:
        def stop(steps):
            return time.perf_counter() > t_end
        f, steps = _brent(n, mpz(rng.randrange(1, ni - 1)), mpz(rng.randrange(0, ni)), stop)
        total += steps
        if f or time.perf_counter() > t_end:
            return f, total / max(time.perf_counter() - t0, 1e-9)


def _rho_worker(n, seed, out_q, stop_event):
    """Runs in its own process: walk until a factor is found or told to stop."""
    try:
        ni, n = int(n), mpz(n)
        rng = random.Random(seed)
        total = 0
        last = [time.perf_counter()]

        def stop(steps):
            now = time.perf_counter()
            if now - last[0] > 0.5:
                last[0] = now
                out_q.put(("progress", seed, total + steps))
            return stop_event.is_set()

        while not stop_event.is_set():
            f, steps = _brent(n, mpz(rng.randrange(1, ni - 1)), mpz(rng.randrange(0, ni)), stop)
            total += steps
            if f:
                out_q.put(("found", seed, f))
                return
    except KeyboardInterrupt:
        pass


def _rho_parallel(n, workers, deadline, show_progress=True):
    """Returns (factor or None, reason) where reason is 'found', 'timeout' or 'interrupted'."""
    ctx = mp.get_context("spawn")  # same behaviour on Windows, Linux and macOS
    out_q = ctx.Queue()
    stop_event = ctx.Event()
    procs = [ctx.Process(target=_rho_worker, args=(int(n), 1000 + i, out_q, stop_event), daemon=True)
             for i in range(workers)]
    for p in procs:
        p.start()
    t0 = time.perf_counter()
    counts = {}
    last_print = 0
    result, reason = None, "timeout"
    try:
        while True:
            try:
                kind, wid, value = out_q.get(timeout=0.25)
                if kind == "found":
                    result, reason = value, "found"
                    break
                counts[wid] = value
            except queue.Empty:
                pass
            now = time.perf_counter()
            if deadline and now > deadline:
                break
            if show_progress and now - last_print > 2 and counts:
                last_print = now
                walk = sum(counts.values()) / len(counts)
                ruled_out = workers * (walk / RHO_C) ** 2 / 3  # ~95% sure no factor below this
                print(f"\r  {fmt_time(now - t0)} elapsed, {sum(counts.values()) / (now - t0) / 1e6:.1f}M steps/s"
                      f" - any factor is likely more than {_digits(ruled_out)} digits      ",
                      end="", flush=True)
    except KeyboardInterrupt:
        reason = "interrupted"
    finally:
        stop_event.set()
        for p in procs:
            p.join(timeout=2)
            if p.is_alive():
                p.terminate()
        if show_progress and last_print:
            print()
    return result, reason


def rho_seconds(n, rate_per_walk, workers, factor_bound=None):
    """Rough time for rho to find a factor below factor_bound (default: worst case sqrt(n))."""
    p = factor_bound if factor_bound else math.isqrt(int(n))
    return RHO_C * math.sqrt(p / workers) / rate_per_walk


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def fmt_time(sec):
    if sec < 1:
        return f"{sec * 1000:.1f} ms"
    if sec < 120:
        return f"{sec:.1f} s"
    if sec < 7200:
        return f"{sec / 60:.0f} min"
    if sec < 2 * 86400:
        return f"{sec / 3600:.1f} hours"
    years = sec / (365.25 * 86400)
    if years < 1:
        return f"{sec / 86400:.0f} days"
    if years < 1e6:
        return f"{years:,.0f} years"
    return f"10^{math.log10(years):.0f} years"


def _digits(x):
    return max(1, int(math.log10(max(x, 1))) + 1)


def digit_count(n):
    n = abs(int(n))
    if n.bit_length() < 200_000:
        return len(str(n))
    return int(n.bit_length() * math.log10(2)) + 1  # approximate for gigantic numbers


def show(n, edge=25):
    s = str(int(n)) if int(n).bit_length() < 200_000 else None
    if s is not None and len(s) <= 2 * edge + 10:
        return s
    if s is None:
        return f"<number with ~{digit_count(n):,} digits>"
    return f"{s[:edge]}...{s[-edge:]} ({len(s):,} digits)"


_ALLOWED_BINOPS = (ast.Add, ast.Sub, ast.Mult, ast.Pow, ast.FloorDiv, ast.Mod)


def parse_number(text):
    """Parse an integer or a simple expression like 2**127-1, 2^89-1, 10**50+151."""
    text = text.strip().replace("^", "**").replace(",", "").replace(" ", "")
    if not text:
        raise ValueError("empty input")

    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            v = ev(node.operand)
            return -v if isinstance(node.op, ast.USub) else v
        if isinstance(node, ast.BinOp) and isinstance(node.op, _ALLOWED_BINOPS):
            a, b = ev(node.left), ev(node.right)
            if isinstance(node.op, ast.Pow):
                if b < 0:
                    raise ValueError("negative exponents aren't integers")
                if abs(a) > 1 and b * max(abs(a).bit_length(), 1) > 50_000_000:
                    raise ValueError("number too large (over ~15 million digits)")
                return a ** b
            ops = {ast.Add: a.__add__, ast.Sub: a.__sub__, ast.Mult: a.__mul__,
                   ast.FloorDiv: a.__floordiv__, ast.Mod: a.__mod__}
            return ops[type(node.op)](b)
        raise ValueError("use whole numbers with + - * // % ** only")

    try:
        return ev(ast.parse(text, mode="eval"))
    except SyntaxError:
        raise ValueError(f"can't read {text!r} as a number")


_PRIMALITY_CALIBRATION = None


def primality_seconds(n):
    """Estimate how long the primality test takes (only matters past ~10,000 digits)."""
    global _PRIMALITY_CALIBRATION
    bits = int(n).bit_length()
    if bits < 10_000 or int(n) & (int(n) + 1) == 0:  # small, or Mersenne (fast test)
        return 0.0
    if _PRIMALITY_CALIBRATION is None:
        b0 = 8192
        m = mpz(random.getrandbits(b0) | (1 << (b0 - 1)) | 1)
        t0 = time.perf_counter()
        pow(mpz(3), m - 1, m)
        _PRIMALITY_CALIBRATION = (b0, time.perf_counter() - t0)
    b0, t = _PRIMALITY_CALIBRATION
    exponent = 2.6 if HAVE_GMPY2 else 2.9  # cost grows a bit under bits^3
    return 1.5 * t * (bits / b0) ** exponent  # measured: BPSW ~= 1.5 modular exponentiations


def confirm(question, assume_yes):
    if assume_yes:
        return True
    if not sys.stdin.isatty():
        print("  (not running interactively - skipping; use --yes to run it anyway)")
        return False
    try:
        return input(f"  {question} [y/N] ").strip().lower() in ("y", "yes")
    except EOFError:
        return False


# --------------------------------------------------------------------------
# Main logic
# --------------------------------------------------------------------------

def find_factor(n, args, deadline, calib, found_so_far=()):
    """Find one nontrivial factor of composite n, warning first if it may take long."""
    f = _pollard_pm1(n) if n.bit_length() < 3000 else None
    if f:
        return f, "found"
    f, rate = _rho_serial(n, time_budget=0.4)
    if f:
        return f, "found"
    calib.setdefault("rate", rate)
    workers = args.workers
    per_walk = calib["rate"] * (0.6 if workers > 1 else 1.0)  # threads share cores
    worst = rho_seconds(n, per_walk, workers)
    if worst > 20:
        half = _digits(math.isqrt(int(n)))
        what = "its factors"
        if found_so_far:
            print(f"  Factors found so far: {' x '.join(str(f) for f in sorted(found_so_far))}")
            what = f"the rest of the factors (a {digit_count(n)}-digit part is left)"
        print(f"\n  Warning: finding {what} could take up to")
        print(f"  ~{fmt_time(worst)} on {workers} threads (if it is two ~{half}-digit primes multiplied).")
        if worst > 3600:
            for secs, label in ((60, "1 minute"), (3600, "1 hour"), (86400, "1 day")):
                print(f"    in {label:9s} it can find factors up to ~{_digits(_bound_for(secs, per_walk, workers))} digits")
        if worst > 100 * 365.25 * 86400:
            print("  Fully factoring it is very unlikely unless it happens to have a smaller factor.")
        if worst > 3600 and not deadline:
            if not confirm("Keep looking for factors anyway? (Ctrl+C stops it)", args.yes):
                return None, "skipped"
        else:
            print("  Searching... (Ctrl+C stops it)")
    return _rho_parallel(n, workers, deadline)


def _bound_for(seconds, per_walk, workers):
    return workers * (seconds * per_walk / RHO_C) ** 2


def check(n, args):
    t0 = time.perf_counter()
    print(f"\n{show(n)}")
    if n < 2:
        print("  NOT prime (primes are 2 or bigger)")
        return

    has_small_factor = any(n % p == 0 for p in SMALL_PRIMES) and n not in SMALL_PRIMES
    est = 0 if has_small_factor else primality_seconds(n)
    if est > 30:
        print(f"  Warning: this number has ~{digit_count(n):,} digits; the primality test alone")
        print(f"  may take up to ~{fmt_time(est)} (less if it turns out not to be prime).")
        if not confirm("Run it?", args.yes):
            return

    prime, how = is_prime(n)
    t1 = time.perf_counter()
    if prime:
        print(f"  IS a prime!  ({fmt_time(t1 - t0)})")
        if how == "lucas-lehmer":
            print("  Proven with the Lucas-Lehmer test for Mersenne numbers (2^p - 1).")
        if how == "bpsw":
            print("  Certainty: BPSW probable prime - no exception to this test has ever been found,")
            print("  but above 3.3*10^24 it isn't a formal proof.")
        return
    print(f"  NOT a prime  ({fmt_time(t1 - t0)})  - this answer is final")
    if args.no_factor:
        return
    print("  Looking for its factors...")

    deadline = time.perf_counter() + args.max_time if args.max_time else None
    calib = {}
    factors, unfactored, unchecked, pending = [], [], [], []
    m = n
    for p in SMALL_PRIMES:
        while m % p == 0:
            factors.append(p)
            m //= p
    if m > 1:
        pending.append(m)
    status = "found"
    while pending:
        pending.sort()
        m = pending.pop(0)  # smallest first, so small factors are reported early
        est = primality_seconds(m)
        if est > 30:
            print(f"  Warning: the remaining {digit_count(m):,}-digit part needs a primality test"
                  f" that may take up to ~{fmt_time(est)}.")
            if status != "found" or not confirm("Run it?", args.yes):
                unchecked.append(m)
                status = "skipped"
                continue
        if is_prime(m)[0]:
            factors.append(m)
            continue
        if _is_square(m):
            r = math.isqrt(m)
            pending += [r, r]
            continue
        if status != "found":
            unfactored.append(m)
            continue
        f, status = find_factor(m, args, deadline, calib, factors)
        if f:
            pending += [f, m // f]
        else:
            unfactored.append(m)

    factors.sort()
    parts = []
    for p in sorted(set(factors)):
        k = factors.count(p)
        parts.append(f"{p}^{k}" if k > 1 else str(p))
    parts += [f"[{show(u)}: composite, not factored]" for u in unfactored]
    parts += [f"[{show(u)}: not checked]" for u in unchecked]
    label = "Factors" if not (unfactored or unchecked) else "Partial factorization"
    print(f"  {label}: {' x '.join(parts)}  ({fmt_time(time.perf_counter() - t1)})")
    if (unfactored or unchecked) and status in ("timeout", "interrupted"):
        print(f"  (search stopped: {status})")


def main():
    ap = argparse.ArgumentParser(description="Fast prime checker and factorizer.")
    ap.add_argument("number", nargs="*", help='a number or expression, e.g. 12345 or "2**127-1"')
    ap.add_argument("--no-factor", action="store_true", help="don't search for factors")
    ap.add_argument("--max-time", type=float, default=None, help="stop factoring after this many seconds")
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 1, help="processes used for factoring")
    ap.add_argument("--yes", action="store_true", help="don't ask before long searches")
    args = ap.parse_args()
    args.workers = max(1, args.workers)

    print(f"Prime checker - {args.workers} threads, "
          f"{'gmpy2 fast math' if HAVE_GMPY2 else 'plain Python ints (pip install gmpy2 for more speed)'}")
    if args.number:
        try:
            check(parse_number(" ".join(args.number)), args)
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
        return
    while True:
        try:
            text = input("\nNumber (or q to quit): ")
        except (EOFError, KeyboardInterrupt):
            break
        if text.strip().lower() in ("q", "quit", "exit"):
            break
        try:
            check(parse_number(text), args)
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\n  Stopped.")


if __name__ == "__main__":
    mp.freeze_support()
    main()
