import random


class Cards():

    cards = []

    def __init__(self, id: int) -> None:

        if id == 11:
            self.name = "Jack"
            self.id = 11
        elif id == 12:
            self.name = "Queen"
            self.id = 12
        elif id == 13:
            self.name = "King"
            self.id = 13
        elif id == 14:
            self.name = "Ace"
            self.id = 14
        else:
            self.name = id
            self.id = id

    def __str__(self) -> str:
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
    def deck_builder() -> list:
        Cards.cards = []
        for i in range(2, 15):
            Cards.cards.append(Clubs(i))
            Cards.cards.append(Hearts(i))
            Cards.cards.append(Spades(i))
            Cards.cards.append(Diamonds(i))

        random.shuffle(Cards.cards)
        return Cards.cards

    @staticmethod
    def sum(x=iter) -> int:
        return sum(x, Cards(0))


class Hearts(Cards):
    def __init__(self, id) -> None:
        super().__init__(id)
        self.suit = "Hearts"

    def __str__(self) -> str:
        return f"{self.name} of {self.suit}"


class Spades(Cards):
    def __init__(self, id) -> None:
        super().__init__(id)
        self.suit = "Spades"

    def __str__(self) -> str:
        return f"{self.name} of {self.suit}"


class Diamonds(Cards):

    def __init__(self, id) -> None:
        super().__init__(id)
        self.suit = "Diamonds"

    def __str__(self) -> str:
        return f"{self.name} of {self.suit}"


class Clubs(Cards):
    def __init__(self, id) -> None:
        super().__init__(id)
        self.suit = "Clubs"

    def __str__(self) -> str:
        return f"{self.name} of {self.suit}"


if __name__ == "__main__":
    pass
