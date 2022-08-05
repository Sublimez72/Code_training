import random


money = 1000


class Blackjack():
    cards = []
    player_hand = []
    dealer_hand = []
    player_hand_value = 0
    dealer_hand_value = 0
    dealer_wins = 0
    player_wins = 0
    pushes = 0

    def __init__(self, id, symbol, value) -> None:
        self.id = id
        self.symbol = symbol
        self.value = value
        self.name = "{0} of {1}".format(id, symbol)

# Shuffles a new deck
    def deck_shuffle():
        Blackjack.player_hand = []
        Blackjack.dealer_hand = []
        Blackjack.player_hand_value = 0
        Blackjack.dealer_hand_value = 0
        Blackjack.cards = []
        Blackjack.deck_creator()
        random.shuffle(Blackjack.cards)

# Creates a new deck in a specific order
    def deck_creator():

        for i in range(1, 14):
            symbol = "Diamonds"
            if i == 1:
                card = Blackjack("Ace", symbol, 11)
            elif i == 11:
                card = Blackjack("Jack", symbol, 10)
            elif i == 12:
                card = Blackjack("Queen", symbol, 10)
            elif i == 13:
                card = Blackjack("King", symbol, 10)
            else:
                card = Blackjack(i, symbol, i)
            Blackjack.cards.append(card)

        for i in range(1, 14):
            symbol = "Spades"
            if i == 1:
                card = Blackjack("Ace", symbol, 11)
            elif i == 11:
                card = Blackjack("Jack", symbol, 10)
            elif i == 12:
                card = Blackjack("Queen", symbol, 10)
            elif i == 13:
                card = Blackjack("King", symbol, 10)
            else:
                card = Blackjack(i, symbol, i)
            Blackjack.cards.append(card)

        for i in range(1, 14):
            symbol = "Hearts"
            if i == 1:
                card = Blackjack("Ace", symbol, 11)
            elif i == 11:
                card = Blackjack("Jack", symbol, 10)
            elif i == 12:
                card = Blackjack("Queen", symbol, 10)
            elif i == 13:
                card = Blackjack("King", symbol, 10)
            else:
                card = Blackjack(i, symbol, i)
            Blackjack.cards.append(card)

        for i in range(1, 14):
            symbol = "Clubs"
            if i == 1:
                card = Blackjack("Ace", symbol, 11)
            elif i == 11:
                card = Blackjack("Jack", symbol, 10)
            elif i == 12:
                card = Blackjack("Queen", symbol, 10)
            elif i == 13:
                card = Blackjack("King", symbol, 10)
            else:
                card = Blackjack(i, symbol, i)
            Blackjack.cards.append(card)

# Deals the first 2 cards
    def deal_first_2():

        for i in range(4):
            if i % 2 == 0:
                Blackjack.hit("player")
            else:
                Blackjack.hit("dealer")

# Handles all of the players and dealers hits
# also handles the value of each players hand with aces accounted for
    def hit(player):

        # Hits to the player
        if player == "player":
            card = Blackjack.cards.pop()
            Blackjack.player_hand.append(card)
            Blackjack.player_hand_value += card.value

            # Handles aces when the player has more than 2 cards
            if len(Blackjack.player_hand) > 2:
                c = 0
                while Blackjack.player_hand_value > 21 and c < len(Blackjack.player_hand):
                    if Blackjack.player_hand[c].value == 11:
                        Blackjack.player_hand[c].value = 1
                        Blackjack.player_hand_value -= 10
                        c += 1
                    else:
                        c += 1
        # Hits to the dealer
        elif player == "dealer":
            card = Blackjack.cards.pop()
            Blackjack.dealer_hand.append(card)
            Blackjack.dealer_hand_value += card.value

            # Handles aces when the dealer has more than 2 cards
            if len(Blackjack.dealer_hand) > 2:
                x = 0
                while Blackjack.dealer_hand_value > 21 and x < len(Blackjack.dealer_hand):
                    if Blackjack.dealer_hand[x].value == 11:
                        Blackjack.dealer_hand[x].value = 1
                        Blackjack.dealer_hand_value -= 10
                        x += 1
                    else:
                        x += 1

        # If the player gets 2 aces
        if len(Blackjack.player_hand) == 2:
            if Blackjack.player_hand[0].value == 11 and Blackjack.player_hand[1].value == 11:
                Blackjack.player_hand[0].value = 1
                Blackjack.player_hand_value -= 10

        # If the dealer gets 2 aces
        if len(Blackjack.dealer_hand) == 2:
            if Blackjack.dealer_hand[0].value == 11 and Blackjack.dealer_hand[1].value == 11:
                Blackjack.dealer_hand[1].value = 1
                Blackjack.dealer_hand_value -= 10


def end():
    total = Blackjack.dealer_wins + Blackjack.player_wins + Blackjack.pushes
    winrate = (Blackjack.player_wins / total) * 100
    print("-" * 50)
    print(f"Total games played: {total}")
    print(f"Player wins: {Blackjack.player_wins}")
    print(f"Dealer wins: {Blackjack.dealer_wins}")
    print(f"Pushes: {Blackjack.pushes}")
    print("")
    print(f"Player winrate: {winrate}")
    quit()


# The main function handles the game flow
def main():
    # While loop so the player can play multiple hands
    while True:
        global money
        if money <= 0:
            print("You have no more money!")
            end()
        insta_blackjack = False
        print("\n" * 100)
        Blackjack.deck_shuffle()
        Blackjack.deal_first_2()
        print(f"Money = ${money}")
        bet = int(input("How much do you want to bet?: "))
        if bet > money:
            print("You don't have that much money!")
            continue
        print()
        print("-" * 50)
        print("These are your cards: ")

        for card in Blackjack.player_hand:
            print(card.name)

        print("The total value of your cards is: {0}".format(
            Blackjack.player_hand_value))
        print("-" * 50)

        print("The dealers first card is a {0}".format(
            Blackjack.dealer_hand[0].name))
        # While loop to deal with players turn
        while Blackjack.player_hand_value < 21:

            move = input("Enter H to hit or S to stand: ")

            if move.lower() == "s":
                break

            elif move.lower() == "h":
                Blackjack.hit("player")
                print("-" * 50)
                print(
                    f"The dealer gives you the {Blackjack.player_hand[-1].name}")
                print(
                    f"Your total hand value is equal to {Blackjack.player_hand_value}")

            elif move.lower() == "q":
                end()
        # If statement in case the player gets a blackjack with 2 cards
        if Blackjack.player_hand_value == 21 and len(Blackjack.player_hand) == 2:
            print("-" * 50)
            print("You got a BLACKJACK!")
            print("-" * 50)
            insta_blackjack = True
        # If player busts out
        elif Blackjack.player_hand_value > 21:
            Blackjack.dealer_wins += 1
            print(f"Loss = ${bet}")
            print("You have busted out\n".upper())
            money -= bet
            input("ENTER TO PLAY AGAIN... ")
            continue
        # While loop to deal with dealers turn, if the player got a blackjack with 2 cards the dealer is not allowed to hit
        while Blackjack.dealer_hand_value < 17 and insta_blackjack == False:
            print("-" * 50)
            print("The dealers cards are:")

            for card in Blackjack.dealer_hand:
                print(card.name)
            print("-" * 50)

            print("The dealer hits...")
            Blackjack.hit("dealer")

            print("-" * 50)

        print("The dealers cards:")
        print("-" * 50)
        for card in Blackjack.dealer_hand:
            print(card.name)

        print(f"Dealers score: {Blackjack.dealer_hand_value}")
        # If and elif statements to figure out the victor
        if Blackjack.dealer_hand_value > 21:
            Blackjack.player_wins += 1
            money += bet
            print("-" * 50)
            print(f"Won = ${bet}")
            print("The dealer has busted")
            print("YOU WIN!")
            input("ENTER TO PLAY AGAIN... ")
            continue

        elif Blackjack.dealer_hand_value > Blackjack.player_hand_value:
            Blackjack.dealer_wins += 1
            money -= bet
            print("-" * 50)
            print(f"Loss = ${bet}")
            print("The Dealer wins")
            print("YOU LOSE!")
            input("ENTER TO PLAY AGAIN... ")
            continue

        elif Blackjack.player_hand_value > Blackjack.dealer_hand_value:
            Blackjack.player_wins += 1
            if insta_blackjack == True:
                money += 1.5 * bet
                print(f"Won = ${1.5 * bet}")
            else:
                print(f"Won = ${bet}")
                money += bet

            print("-" * 50)
            print("YOU WIN!")
            input("ENTER TO PLAY AGAIN... ")
            continue

        elif Blackjack.dealer_hand_value == Blackjack.player_hand_value:
            Blackjack.pushes += 1
            print("-" * 50)
            print("PUSH!")
            input("ENTER TO PLAY AGAIN... ")
            continue
        else:
            print("error")

            for card in Blackjack.player_hand:
                print(card.name)
            for card in Blackjack.dealer_hand:
                print(card.name)
            quit()


if __name__ == "__main__":
    main()
