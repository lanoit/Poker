import random
from typing import Any

from card import Card

class Deck:
    """
    a class representing a standard deck of 52 playing cards

    attributes:
        cards (list): a list of Card objects representing the deck of cards

    methods:
        __init__(): initializes a standard deck of 52 playing cards and shuffles them (constructor)
        shuffle(): shuffles the deck of cards in place
        deal(): deals a single card from the top of the deck
        reset_deck(): resets the deck to a standard deck of 52 playing cards and shuffles them
    """
    def __init__(self):
        """
        initializes a standard deck of 52 playing cards and shuffles them

        the deck consists of 4 suits (spades, hearts, diamonds, clubs) in symbol form and 13 ranks (2-10, J, Q, K, A)
        each card is represented by a Card object
        """
        self.cards: list[Card] = []
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(rank, suit))  

        self.shuffle()

    def shuffle(self) -> None:
        """
        shuffles the deck of cards in place using the random.shuffle() method
        :return: None
        """
        random.shuffle(self.cards)

    def deal(self) -> Any | None:
        """
        deals a single card from the top of the deck
        :return: A card object representing the dealt card, or None if the deck is empty
        """
        if self.cards:
            return self.cards.pop() 
        else:
            print("empty deck")
            return None

    def reset_deck(self) -> None:
        """
        resets the deck to a standard deck of 52 playing cards and shuffles them
        :return: None
        """
        self.__init__() 
