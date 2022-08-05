import random

# Simulates a number of games of rock paper scissors and calculates the winrate

player1_wins = 0
player2_wins = 0
draws = 0


def evaluation(player1, player2):
    global player1_wins
    global player2_wins
    global draws
    if player1 == "Scissors" and player2 == "Rock":
        player2_wins += 1

    elif player1 == "Rock" and player2 == "Scissors":
        player1_wins += 1

    elif player1 == "Paper" and player2 == "Rock":
        player1_wins += 1

    elif player1 == "Scissors" and player2 == "Paper":
        player1_wins += 1

    elif player1 == "Rock" and player2 == "Paper":
        player2_wins += 1

    elif player1 == "Paper" and player2 == "Scissors":
        player2_wins += 1

    elif player1 == player2:
        draws += 1


def loops(loop):

    for _ in range(1, loop + 1):
        moveList = ["Rock", "Paper", "Scissors"]
        player1 = random.choice(moveList)
        player2 = random.choice(moveList)

        evaluation(player1, player2)

    print("Player 1 wins: ", player1_wins)
    print("Player 2 wins: ", player2_wins)
    print("Draws: ", draws)
    total = player2_wins + player1_wins
    winrate = (player1_wins / total) * 100
    print("Player 1 Winrate: ", winrate)


def main():
    while True:
        loop = int(input("How many rounds of RPS to you want to emulate?: "))
        loops(loop)


if __name__ == "__main__":
    main()
