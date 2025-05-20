class Player:
    """
    class representing a player in a poker game

    attributes:
        name (str): name of the player
        chips (int): number of chips the player has
        folded (bool): whether the player has folded their hand
        hand (list): list of Card objects representing the player's hand
        current_bet (int): the amount the player has bet in the current round

    methods:
        __init__(name, chips): initializes a player with a name and number of chips
        reset_round(): resets the player's state for a new round
        __str__(): returns a string representation of the player
        show_hand(): returns a string representation of the player's hand
        bet(bet): updates the player's chips and current bet
        fold(): sets the player's folded state to True
        is_all_in(): checks if the player is all-in (has no chips left)
    """
    def __init__(self, name: str, chips: int):
        """
        initializes a player with a name and number of chips
        :param name:
        :param chips:

        attributes:
            same as above
        """
        self.name = name
        self.chips = chips
        self.folded = False
        self.hand = []
        self.current_bet = 0

    def reset_round(self) -> None:
        """
        resets the player's state for a new round
        :return: None
        """
        self.folded = False
        self.hand = []
        self.current_bet = 0

    def __str__(self) -> str:
        """
        :return: string representation of the player
        """
        return f"{self.name}'s turn, chips: {self.chips}\n"
        
    def show_hand(self) -> str:
        """
        :return: string representation of the player's hand
        """
        return f"{self.name}'s hand: {', '.join(str(card) for card in self.hand)}"

    def bet(self, bet: int) -> None:
        """
        updates the player's chips and current bet by amount bet
        :param bet: amount of chips the player is betting
        :return: None
        """
        self.current_bet += bet
        self.chips -= bet

    def fold(self) -> None:
        """
        folds the player
        :return: None
        """
        self.folded = True

    def is_all_in(self) -> bool:
        """
        checks if the player is all-in (has no chips left)
        :return: True if the player is all-in (has no chips left), False otherwise
        """
        return self.chips == 0
    