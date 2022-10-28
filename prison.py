import random
import time

# Simulates a number of sessions of the 100 prisoners riddle
# and calculates the strategys winrate


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

    for i in range(1, loops + 1):
        #print("{0} / {1}".format(i, loops))
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

        if len(failed_prisoners) == 0:
            sucessfull_experiments += 1
        else:
            failed_experiments += 1

    if loops > 1:
        print("Successfull Experiments: ", sucessfull_experiments)
        print("Failed Experiments: ", failed_experiments)
        total_experiments = sucessfull_experiments + failed_experiments
        win_rate = (sucessfull_experiments / total_experiments) * 100
        print("Winrate: {0}%".format(win_rate))
    elif loops == 1:
        print("Free Prisoners: ", free_prisoners)
        print("Failed Prisoners: ", failed_prisoners)
        win_rate = len(free_prisoners)
        print("Winrate: ", win_rate)


loops = int(input("How many loops?: "))

start_t = time.perf_counter()
experiment(loops)
end_t = time.perf_counter()
print(f"Total duration {end_t - start_t}s")
