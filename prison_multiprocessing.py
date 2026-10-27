import os
import random
import time
from concurrent.futures import ProcessPoolExecutor

# Simulates sessions of the 100 prisoners riddle using the loop strategy
# and calculates the strategy's win rate. Multi-loop runs are split across
# CPU cores with multiprocessing.

NUM_PRISONERS = 100
MAX_OPENS = NUM_PRISONERS // 2


def run_session(rng, stop_on_fail=False):
    """Run one session. Returns (free, failed) lists of prisoner numbers."""
    boxes = list(range(1, NUM_PRISONERS + 1))
    rng.shuffle(boxes)

    free, failed = [], []
    for prisoner in range(1, NUM_PRISONERS + 1):
        box = prisoner  # start with the box carrying your own number
        for _ in range(MAX_OPENS):
            paper = boxes[box - 1]
            if paper == prisoner:
                free.append(prisoner)
                break
            box = paper  # follow the loop to the next box
        else:
            failed.append(prisoner)
            if stop_on_fail:
                break  # one failure dooms the whole group
    return free, failed


def run_batch(args):
    """Run a batch of sessions in one worker. Returns the number of wins."""
    count, seed = args
    # Each worker needs its own random generator. Forked processes would
    # otherwise inherit the same random state and produce identical results.
    rng = random.Random(seed)
    wins = 0
    for _ in range(count):
        _, failed = run_session(rng, stop_on_fail=True)
        if not failed:
            wins += 1
    return wins


def split_work(loops, workers):
    """Split loops into one batch per worker, each with its own seed."""
    base, extra = divmod(loops, workers)
    sizes = [base + (1 if i < extra else 0) for i in range(workers)]
    return [(size, random.randrange(2**63)) for size in sizes if size > 0]


def experiment(loops, workers=None):
    if loops == 1:
        free, failed = run_session(random.Random())
        print("Free prisoners:  ", free)
        print("Failed prisoners:", failed)
        print(f"Found their number: {len(free)}/{NUM_PRISONERS}")
        print("Session result:", "WIN" if not failed else "LOSS")
        return

    workers = workers or os.cpu_count() or 1
    batches = split_work(loops, workers)

    with ProcessPoolExecutor(max_workers=workers) as pool:
        successes = sum(pool.map(run_batch, batches))

    failures = loops - successes
    print(f"Worker processes: {workers}")
    print("Successful experiments:", successes)
    print("Failed experiments:    ", failures)
    print(f"Win rate: {successes / loops * 100:.2f}%")


def ask_loops():
    while True:
        try:
            loops = int(input("How many loops?: "))
            if loops >= 1:
                return loops
        except ValueError:
            pass
        print("Please enter a whole number of 1 or more.")


if __name__ == "__main__":
    loops = ask_loops()
    start_t = time.perf_counter()
    experiment(loops)
    end_t = time.perf_counter()
    print(f"Total duration: {end_t - start_t:.3f}s")