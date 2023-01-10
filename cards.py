import random

# A class to create any card deck you want where the values of the court cards can be changed to suit your liking.
# The static function Cards.deck_builder() returns a list of cards objects which acts as the deck of cards.
class Cards():

    cards = []

    def __init__(self, id: int, jack=11, queen=12, king=13, ace=14) -> None:

        if id == 11:
            self.name = "Jack"
            self.id = jack
        elif id == 12:
            self.name = "Queen"
            self.id = queen
        elif id == 13:
            self.name = "King"
            self.id = king
        elif id == 14:
            self.name = "Ace"
            self.id = ace
        else:
            self.name = id
            self.id = id

    def __repr__(self) -> str:
        return f"{self.id}"

    def __add__(self, other: object) -> object:
        return Cards(self.id + other.id)

    def __sub__(self, other: object) -> object:
        return Cards(self.id - other.id)

    def __eq__(self, other: object) -> bool:
        return self.id == other.id

    def __ge__(self, other: object) -> bool:
        return self.id >= other.id

    def __gt__(self, other: object) -> bool:
        return self.id > other.id

    def __int__(self) -> int:
        return self.id

    @staticmethod
    def deck_builder(jack=11, queen=12, king=13, ace=14) -> list:
        Cards.cards = []
        for i in range(2, 15):
            Cards.cards.append(Clubs(i, jack, queen, king, ace))
            Cards.cards.append(Hearts(i, jack, queen, king, ace))
            Cards.cards.append(Spades(i, jack, queen, king, ace))
            Cards.cards.append(Diamonds(i, jack, queen, king, ace))

        random.shuffle(Cards.cards)
        return Cards.cards

    @staticmethod
    def sum(x=iter) -> int:
        return sum(x, Cards(0))


class Hearts(Cards):
    def __init__(self, id, jack=11, queen=12, king=13, ace=14) -> None:
        super().__init__(id, jack, queen, king, ace)
        self.suit = "Hearts"

    def __repr__(self) -> str:
        return f"{self.name} of {self.suit}"


class Spades(Cards):
    def __init__(self, id, jack=11, queen=12, king=13, ace=14) -> None:
        super().__init__(id, jack, queen, king, ace)
        self.suit = "Spades"

    def __repr__(self) -> str:
        return f"{self.name} of {self.suit}"


class Diamonds(Cards):

    def __init__(self, id, jack=11, queen=12, king=13, ace=14) -> None:
        super().__init__(id, jack, queen, king, ace)
        self.suit = "Diamonds"

    def __repr__(self) -> str:
        return f"{self.name} of {self.suit}"


class Clubs(Cards):
    def __init__(self, id, jack=11, queen=12, king=13, ace=14) -> None:
        super().__init__(id, jack, queen, king, ace)
        self.suit = "Clubs"

    def __repr__(self) -> str:
        return f"{self.name} of {self.suit}"


if __name__ == "__main__":
    deck = Cards.deck_builder(10, 10, 10, 11)
