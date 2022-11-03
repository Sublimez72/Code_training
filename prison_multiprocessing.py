
import random
import time
from multiprocessing import Pool

# Simulates a number of sessions of the 100 prisoners riddle
# and calculates the strategys winrate
# 
# This version comes with multiprocessing support which makes it a lot faster.


def box_setup():
    global papers
    global free_prisoners
    global failed_prisoners

    papers = []
    free_prisoners = []
    failed_prisoners = []

    for i in range(1, 101):
        papers.append(i)

    random.shuffle(papers)


def experiment(loops):

    sucessfull_experiments = 0
    failed_experiments = 0
    #print(f"{loops}")
    box_setup()

    for i in range(1, 101):
        x = 1
        openedBox = papers[i - 1]

        while x <= 50:
            if openedBox == i:
                free_prisoners.append(i)
                break
            else:
                openedBox = papers[openedBox - 1]
            x += 1
        else:
            failed_prisoners.append(i)

        if len(failed_prisoners) + len(free_prisoners) == 100 and len(free_prisoners) == 100:
            sucessfull_experiments += 1

        elif len(failed_prisoners) + len(free_prisoners) == 100 and len(free_prisoners) != 100:
            failed_experiments += 1

    return sucessfull_experiments
    


if __name__ == "__main__":
    loops = int(input("How many loops?: "))
    start_t = time.perf_counter()
    with Pool() as p:
        result = p.map(experiment, range(1, loops + 1))
        end_t = time.perf_counter()
        win_rate = (result.count(1) / len(result)) * 100
        print("Win rate:", win_rate)
        print(f"Total duration {end_t - start_t}s")





