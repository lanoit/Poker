from functools import total_ordering

@total_ordering
class Card:
    """
    a class representing a playing card

    each card has a rank and a suit
    the rank is represented as a string (2-10, J, Q, K, A)
    the suit is represented as a string (♠, ♥, ♦, ♣)

    attributes:
        rank_values (dict): a dictionary mapping card ranks to their values
        rank (str): the rank of the card
        suit (str): the suit of the card

    methods:
        __init__(rank, suit): initializes a card with a rank and suit
        __repr__(): returns a string representation of the card
        __str__(): returns a string representation of the card
        __eq__(other): checks if two cards are equal
        __lt__(other): compares two cards based on their rank and suit

    """
    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }
    def __init__(self, rank: str, suit:  str):
        """
        initializes a card with a rank and suit
        :param rank: rank of the card (2-10, J, Q, K, A)
        :param suit: suit of the card (♠, ♥, ♦, ♣)
        """
        self.rank = rank
        self.suit = suit

    def __repr__(self) -> str:
        """
        __repr__ is a built-in function that returns a string representation of the object
        :return: string representation of the card
        """
        return f"{self.rank}{self.suit}"

    def __str__(self) -> str:
        """
        __str__ is a built-in function that overrides the default string representation (str()) of the object
        :return: string representation of the card
        """
        return self.__repr__()
    
    def __eq__(self, other) -> bool:
        """
        __eq__ is a built-in function that overrides the default equality operator (==) for the object
        :param other: another card object
        :return: if the two cards are equal
        """
        if isinstance(other, Card): # check if other is an instance of Card
            return self.rank == other.rank and self.suit == other.suit
        return False
    
    def __lt__(self, other) -> bool:
        """
        __lt__ is a built-in function that overrides the default less than operator (<) for the object
        :param other: another card object
        :return: if the first card is less than the second card
        """
        if isinstance(other, Card):
            if Card.rank_values[self.rank] == Card.rank_values[other.rank]:
                return self.suit < other.suit
            return Card.rank_values[self.rank] < Card.rank_values[other.rank]
        return False