import random


def tutorial():
    print()
    print("Rock Paper Scissors Controls")
    print("-" * 50)
    print()
    print("Rock = 1")
    print("Paper = 2")
    print("Scissors = 3")
    print("Tutorial = 4")
    print("Quit = 5")
    print()


tutorial()

while True:

    moveList = ["Rock", "Paper", "Scissors"]
    player2 = random.choice(moveList)

    try:
        player1_index = int(input("Move: ")) - 1

        if player1_index == 4:
            break

        player1 = moveList[player1_index]

        if player1_index < 0:
            player1 = None

        if player1 == "Scissors" and player2 == "Rock":
            print("You played {0}".format(player1))
            print(
                "The computer played {0} which means that you LOSE!".format(player2))
            print()

        elif player1 == "Rock" and player2 == "Scissors":
            print("You played {0}".format(player1))
            print(
                "The computer played {0} which means that you WIN!".format(player2))
            print()

        elif player1 == "Paper" and player2 == "Rock":
            print("You played {0}".format(player1))
            print(
                "The computer played {0} which means that you WIN!".format(player2))
            print()

        elif player1 == "Scissors" and player2 == "Paper":
            print("You played {0}".format(player1))
            print(
                "The computer played {0} which means that you WIN!".format(player2))
            print()

        elif player1 == "Rock" and player2 == "Paper":
            print("You played {0}".format(player1))
            print(
                "The computer played {0} which means that you LOSE!".format(player2))
            print()

        elif player1 == "Paper" and player2 == "Scissors":
            print("You played {0}".format(player1))
            print(
                "The computer played {0} which means that you LOSE!".format(player2))
            print()

        elif player1 == player2:
            print("It's a draw!")
            print()

        elif player1 == None:
            tutorial()

    except IndexError:
        tutorial()

    except ValueError:
        tutorial()
