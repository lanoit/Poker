import os
import time
from collections import Counter
from itertools import combinations
from deck import Deck

hand_strength = {
    "high card": 0,
    "pair": 1,
    "two pair": 2,
    "three of a kind": 3,
    "straight": 4,
    "flush": 5,
    "full house": 6,
    "four of a kind": 7,
    "straight flush": 8,
    "royal flush": 9
}


def clear_screen():
    """
    clears the console screen using os.system
    :return: None
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_best_hand(all_cards: list[Deck], hand_type_check) -> list:
    """
    finds the best hand from a list of all cards
    :param all_cards: list of Card objects representing all cards (player's hand + comx`munity cards)
    :param hand_type_check: function to check if a hand is of a certain type (ex. flush, straight, etc.)
    :return: the best hand found

    1. it generates all possible combinations of 5 cards from the list of all cards
    2. it checks each combination to see if it is a valid hand using the provided hand_type_check function
    3. if a valid hand is found, it returns the combination of cards that make up that hand
    4. if no valid hand is found, it returns None
    """
    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    best_hand = None
    # combinations takes a list and returns all possible combinations of the given length
    for combo in combinations(all_cards, 5):
        if hand_type_check(combo):
            sorted_combo = sorted(combo, key=lambda card: rank_values[card.rank], reverse=True)
            if best_hand is None or sorted_combo > best_hand:
                best_hand = sorted_combo

    return best_hand


def is_flush(five_card_hand) -> bool:
    """
    checks if a hand is a flush (all cards of the same suit)
    :param five_card_hand: five card hand
    :return: True if the hand is a flush, otherwise False
    """
    first_suit = five_card_hand[0].suit
    # all() checks if all elements in the iterable are True (I love this so you'll see it a lot)
    return all(card.suit == first_suit for card in five_card_hand)


def is_straight(five_card_hand) -> bool:
    """
    checks if a hand is a straight (five consecutive ranks)
    :param five_card_hand: five card hand
    :return: True if the hand is a straight, otherwise False

    1. create a dictionary to map card ranks to their values
    2. get the ranks of the cards in the hand
    3. convert the ranks to their numeric values and sort them
    4. check for a low ace straight (A, 2, 3, 4, 5)
    5. check for a high ace straight (10, J, Q, K, A)
    6. return True if the hand is a straight, otherwise False
    """

    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 1}

    ranks = [card.rank for card in five_card_hand]
    numeric_ranks = sorted([rank_values[rank] for rank in ranks])

    # check for a low ace straight (A, 2, 3, 4, 5)
    if numeric_ranks == [1, 2, 3, 4, 5]:
        return True

    high_ace_ranks = [14 if rank == 1 else rank for rank in numeric_ranks]
    high_ace_ranks.sort()
    return high_ace_ranks == list(range(high_ace_ranks[0], high_ace_ranks[0] + 5))


def is_straight_flush(five_card_hand) -> bool:
    """
    checks if a hand is a straight flush (five consecutive ranks of the same suit)
    :param five_card_hand: five card hand
    :return: True if the hand is a straight flush, otherwise False
    """
    return is_flush(five_card_hand) and is_straight(five_card_hand)


def is_full_house(five_card_hand) -> bool:
    """
    checks if a hand is a full house (three of a kind and a pair)
    :param five_card_hand: five card hand
    :return: True f the hand is a full house, otherwise False
    """
    # Counter counts the occurrences of each rank in the hand and returns a dictionary-like object
    count = Counter(card.rank for card in five_card_hand)
    values = count.values()
    return 3 in values and 2 in values


def is_four_of_a_kind(five_card_hand) -> bool:
    """
    checks if a hand is a four of a kind (four cards of the same rank)
    :param five_card_hand: five card hand
    :return: True if the hand is a four of a kind, otherwise False
    """
    count = Counter(card.rank for card in five_card_hand)
    return 4 in count.values()


def is_three_of_a_kind(five_card_hand) -> bool:
    """
    checks if a hand is a three of a kind (three cards of the same rank)
    :param five_card_hand: five card hand
    :return: True if the hand is a three of a kind, otherwise False
    """
    count = Counter(card.rank for card in five_card_hand)
    values = count.values()
    return 3 in values and list(values).count(2) == 0


def is_two_pair(five_card_hand) -> bool:
    """
    checks if a hand is a two pair (two pairs of cards of the same rank)
    :param five_card_hand: five card hand
    :return: True if the hand is a two pair, otherwise False
    """
    count = Counter(card.rank for card in five_card_hand)
    values = count.values()
    return list(values).count(2) == 2


def is_pair(five_card_hand) -> bool:
    """
    checks if a hand is a pair (two cards of the same rank)
    :param five_card_hand: five card hand
    :return: True if the hand is a pair, otherwise False
    """
    count = Counter(card.rank for card in five_card_hand)
    values = count.values()
    return list(values).count(2) == 1


def is_high_card(five_card_hand) -> bool:
    """
    checks if a hand is a high card (no pairs, no flush, no straight)
    :param five_card_hand: five card hand
    :return: True if the hand is a high card, otherwise False
    """
    count = Counter(card.rank for card in five_card_hand)
    return len(count) == 5 and not is_straight(five_card_hand) and not is_flush(five_card_hand)

def is_royal_flush(five_card_hand) -> bool:
    """
    checks if a hand is a royal flush (10, J, Q, K, A of the same suit)
    :param five_card_hand: five card hand
    :return: True if the hand is a royal flush, otherwise False
    """
    if is_flush(five_card_hand) and is_straight(five_card_hand):
        ranks = [card.rank for card in five_card_hand]
        if all(rank in ranks for rank in ['10', 'J', 'Q', 'K', 'A']):
            return True
    return False


class Game:
    """
    a class representing a poker game

    attributes:
        players (list[Player]): a list of Player objects
        deck (Deck): a Deck object representing the deck of cards
        pot (int): the current pot amount
        community_cards (list[Card]): a list of community cards
        last_raiser_index (int): the index of the last player who raised
        minimum_bet (int): the minimum bet amount for the current round
        dealer_index (int): the index of the dealer player
        small_blind (int): the small blind amount
        big_blind (int): the big blind amount
        stage (str): the current stage of the game (preflop, flop, turn, river)

    methods:
        this would take too long, so I will not write it, you got this Mr. Perry :)

    """
    def __init__(self, players: list):
        """
        initializes the game with a list of players
        :param players: a list of Player objects

        attributes:
            same as above
        """

        self.players = players
        self.deck = Deck()
        self.pot = 0
        self.community_cards = []
        self.last_raiser_index = None
        self.minimum_bet = 20
        self.dealer_index = 0
        self.small_blind = 10
        self.big_blind = 20
        self.stage = "preflop"

    def reset_round(self) -> None:
        """
        resets the game state for a new round
        :return: None
        """
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.pot = 0
        self.minimum_bet = self.big_blind
        self.stage = "preflop"
        for player in self.players:
            player.reset_round()

    def deal_cards(self) -> None:
        """
        deals two cards to each player
        :return: None
        """
        for player in self.players:
            player.hand.append(self.deck.deal())
    
        for player in self.players:
            player.hand.append(self.deck.deal())

    def deal_flop(self) -> None:
        """
        deals the flop (three community cards)
        :return: None
        """
        for i in range(3):
            self.community_cards.append(self.deck.deal())

    def deal_single(self) -> None:
        """
        deals a single community card (turn or river)
        :return: None
        """
        self.community_cards.append(self.deck.deal())
    
    def play(self) -> None:
        """
        main game loop
        this method handles game flow, which includes dealing cards,
        betting rounds, and determining the winners
        :return: None
        """
        while True:
            self.reset_round()
            self.deal_cards()
            print("Dealing cards, a new round is starting")
            time.sleep(2)
            clear_screen()
            self.pre_flop()
            if self.only_one_player_remaining():
                self.give_chips()
                continue

            print("Flop starting...")
            time.sleep(2)

            self.flop()
            if self.only_one_player_remaining():
                self.give_chips()
                time.sleep(2)
                continue

            print("Turn starting...")
            time.sleep(2)

            self.turn()
            if self.only_one_player_remaining():
                self.give_chips()
                time.sleep(2)
                continue

            print("River starting...")
            time.sleep(2)

            self.river()
            if self.only_one_player_remaining():
                self.give_chips()
                time.sleep(2)
                continue

            hand_rankings = self.evaluate_hand()
            top_rank = hand_rankings[0][1]
            top_hand = hand_rankings[0][2]
            winners = [entry[0] for entry in hand_rankings if entry[1] == top_rank and entry[2] == top_hand]
            print("Calculating winners...")
            time.sleep(2)
            if len(winners) == 1:
                print(f"{winners[0].name} wins with a {top_rank}: {', '.join(str(card) for card in top_hand)}")
                winners[0].chips += self.pot
                print(f"{winners[0].name} now has {winners[0].chips} chips")
            else:
                print(f"It's a tie between: {', '.join(player.name for player in winners)} with a {top_rank}: {', '.join(str(card) for card in top_hand)}")
                split = self.pot // len(winners)
                for w in winners:
                    w.chips += split
                    print(f"{w.name} now has {w.chips} chips")

            for player in self.players:
                if player not in winners:
                    print(f"{player.name}'s hand: {player.show_hand()}")

            self.pot = 0
            time.sleep(2)

            eliminated_players = [player for player in self.players if player.chips <= 0]
            for player in eliminated_players:
                print(f"{player.name} is eliminated, nice try")
                self.players.remove(player)

            time.sleep(2)

            if len(self.players) == 1:
                print(f"{self.players[0].name} is the winner of the game!")
                break

            self.dealer_index = (self.dealer_index + 1) % len(self.players)
            clear_screen()

        print("Game over!")
        print("Thanks for playing!")
        
    def not_folded_index(self) -> int:
        """
        returns the index of the first player who has not folded
        :return: -1 if not all players have folded, otherwise the index of the player
        """
        if not self.only_one_player_remaining():
            return -1
        
        for i in range(len(self.players)):
            if not self.players[i].folded:
                return i

        return -1


    def give_chips(self) -> None:
        """
        gives the chips in the pot to the player who has not folded
        :return: None
        """
        if not self.only_one_player_remaining():
            time.sleep(2)
            return
        
        winner_idx  = self.not_folded_index()
        print(f"{self.players[winner_idx].name} wins the pot of {self.pot}")
        time.sleep(2)
        self.players[winner_idx].chips += self.pot
        print(f"{self.players[winner_idx].name} now has {self.players[winner_idx].chips} chips")
        for player in self.players:
            if player != self.players[winner_idx]:
                print(f"{player.name} has {player.chips} chips")

        self.pot = 0

        for player in self.players:
            player.current_bet = 0

    def clear_bets(self) -> None:
        """
        resets the current bet for each player to 0
        :return: None
        """

        for player in self.players:
            player.current_bet = 0

    def only_one_player_remaining(self) -> bool:
        """
        checks if only one player has not folded
        :return: True if only one player has not folded, otherwise False
        """
        all_but_one = len(self.players) - 1
        count = 0
        for player in self.players:
            if player.folded:
                count += 1

        return count == all_but_one
        
    def all_bets_equal(self) -> bool:
        """
        checks if all players who have not folded have the same bet
        :return: True if all bets are equal, otherwise False
        """
        not_folded_players = [player for player in self.players if not player.folded]
        if not not_folded_players:
            return True
        
        bet = not_folded_players[0].current_bet
        return all(player.current_bet == bet for player in not_folded_players)

    def evaluate_hand(self) -> list[tuple]:
        """
        evaluates the hands of all players and determines the best hand
        := combines assignment and comparison of a value to a variable (called a walrus operator)
        :return: sorted list of tuples containing player and their hand ranking
        """
        hand_rankings = []
        for player in self.players:
            if player.folded:
                continue
            
            all_cards = player.hand + self.community_cards
            if best_hand := get_best_hand(all_cards, is_royal_flush):
                hand_rankings.append((player, "royal flush", best_hand))
            elif best_hand := get_best_hand(all_cards, is_straight_flush):
                hand_rankings.append((player, "straight flush", best_hand))
            elif best_hand := get_best_hand(all_cards, is_four_of_a_kind):
                hand_rankings.append((player, "four of a kind", best_hand))
            elif best_hand := get_best_hand(all_cards, is_full_house):
                hand_rankings.append((player, "full house", best_hand))
            elif best_hand := get_best_hand(all_cards, is_flush):
                hand_rankings.append((player, "flush", best_hand))
            elif best_hand := get_best_hand(all_cards, is_straight):
                hand_rankings.append((player, "straight", best_hand))
            elif best_hand := get_best_hand(all_cards, is_three_of_a_kind):
                hand_rankings.append((player, "three of a kind", best_hand))
            elif best_hand := get_best_hand(all_cards, is_two_pair):
                hand_rankings.append((player, "two pair", best_hand))
            elif best_hand := get_best_hand(all_cards, is_pair):
                hand_rankings.append((player, "pair", best_hand))
            else:
                best_hand = get_best_hand(all_cards, is_high_card)
                hand_rankings.append((player, "high card", best_hand))

        sorted_hand_rankings = sorted(hand_rankings, key=lambda x: (hand_strength[x[1]], x[2]), reverse=True)
        return sorted_hand_rankings

    def handle_player_action(self, player) -> None:
        """
        handles the player's action during their turn
        this involves checking, calling, raising, or folding
        :param player:
        :return: None
        """
        call_amount = max(0, self.minimum_bet - player.current_bet)
        print(f"Current pot:\n{self.pot}\n")
        print(f"{player}{player.show_hand()}")
        print(f"\nCurrent bet to call: {self.minimum_bet}\nYou have bet: {player.current_bet}\n")
        action = input("bet/fold/check/call\n").strip().lower()
        if action == "fold":
            player.fold()
        elif action == "call":
            actual_call = min(call_amount, player.chips)
            player.bet(actual_call)
            self.pot += actual_call
            if actual_call < call_amount:
                print(f"You are all in, you have bet {actual_call}")
                time.sleep(1)
        elif action == "check" or action == "":
            if player.current_bet < self.minimum_bet != 0:
                print("You must call")
                print(f"{call_amount} to stay in")
                call_or_fold = input("call/fold\n").strip().lower()
                if call_or_fold == "fold":
                    player.fold()
                elif call_or_fold == "call":
                    actual_call = min(call_amount, player.chips)
                    player.bet(actual_call)
                    self.pot += actual_call

                    if actual_call < call_amount:
                        print(f"You are all in, you have bet {actual_call}")
                        time.sleep(1)
                else:
                    print("You mistyped, so you automatically folded")
                    player.fold()

            else:
                print("You checked")
                time.sleep(0.5)
        elif action == "bet":
            while True:
                try:
                    bet_amount = int(input("How much will you bet? "))
                    if bet_amount > player.chips:
                        print(f"You don't have enough chips for that, you only have {player.chips}")
                    elif bet_amount < self.big_blind:
                        print(f"Too low, you must bet at least {self.big_blind}")
                    elif bet_amount >= call_amount:
                        actual_bet = min(bet_amount, player.chips)
                        player.bet(actual_bet)
                        self.pot += actual_bet
                        self.minimum_bet = player.current_bet
                        self.last_raiser_index = self.players.index(player)
                        if actual_bet < bet_amount:
                            print(f"You are all in, you have bet {actual_bet}")
                            time.sleep(1)
                        break
                    else:
                        print(f"Too low, you must bet at least {self.minimum_bet}")
                except ValueError:
                    print("Please try again. That was not a valid number.")
        else:
            print("That was not a valid command. Please try again.")
            time.sleep(1)
            self.handle_player_action(player)

    def flop(self) -> None:
        """
        deals the flop (three community cards) and starts the betting round
        :return: None
        """
        self.play_betting_round(self.deal_flop, "Flop")

    def turn(self) -> None:
        """
        deals the turn (one community card) and starts the betting round
        :return: None
        """
        self.play_betting_round(self.deal_single, "Turn")

    def river(self) -> None:
        """
        deals the river (one community card) and starts the betting round
        :return: None
        """
        self.play_betting_round(self.deal_single, "River")

    def play_betting_round(self, deal_phase_func, phase_name) -> None:
        """
        handles the betting round for a given phase (flop, turn, river)
        :param deal_phase_func: function to deal cards for the phase
        :param phase_name: name of the phase (flop, turn, river)
        :return: None
        """
        clear_screen()
        self.minimum_bet = 0
        deal_phase_func()
        self.clear_bets()

        not_folded = [p for p in self.players if not p.folded]
        not_all_in = [p for p in not_folded if not p.is_all_in()]

        if len(not_all_in) == 1 and len(not_folded) > 1:
            player = not_all_in[0]
            call_amount = max(0, self.minimum_bet - player.current_bet)
            if call_amount > 0:
                player.bet(call_amount)
                self.pot += call_amount

            print(f"\n{player.name} auto-checks and all other players are all in")
            time.sleep(1)

            print(f"community cards: {', '.join(str(card) for card in self.community_cards)}\n")
            for p in not_folded:
                print(f"{p.name}: {p.show_hand()}")

            time.sleep(2)
            return


        if all(player.is_all_in() or player.folded for player in self.players):
            print("All players are all in or folded.")
            print(f"community cards: {', '.join(str(card) for card in self.community_cards)}\n")
            for p in self.players:
                print(f"{p.name}'s hand: {p.show_hand()}")

            time.sleep(1)
            return

        players_acted_since_last_raise = 0

        index = (self.dealer_index + 1) % len(self.players)
        self.last_raiser_index = 0
        while True:
            print(f"{phase_name} community cards:\n{', '.join(str(card) for card in self.community_cards)}\n")
            if self.only_one_player_remaining():
                print("Only one player remaining")
                break

            player = self.players[index]

            if not player.folded and not player.is_all_in():
                self.handle_player_action(player)


                if not player.folded:
                    if player.current_bet > self.minimum_bet:
                        self.minimum_bet = player.current_bet
                        self.last_raiser_index = index
                        players_acted_since_last_raise = 1
                    else:
                        players_acted_since_last_raise += 1
            elif not player.folded and player.is_all_in():
                print(f"{player.name} is all in")
                #print(f"{player.name}'s hand is {player.show_hand()}")
                players_acted_since_last_raise += 1

            clear_screen()

            """
            print(f"index: {index}")
            print(f"last_raiser_index: {self.last_raiser_index}")
            print(f"{index == self.last_raiser_index}")
            print(f"players_acted_since_last_raise: {players_acted_since_last_raise}")
            print(f"players: {len([p for p in self.players if not p.folded])}")
            print(f"{players_acted_since_last_raise >= len([p for p in self.players if not p.folded])}")
            print(f"all_bets_equal: {self.all_bets_equal()}")
            """

            # this line right here was absolute torture to figure out, what should have been a simple if statement took probably 3 days of trial and error
            if (index == self.last_raiser_index or players_acted_since_last_raise >= len([p for p in self.players if not p.folded])) and self.all_bets_equal():
                clear_screen()
                print(f"{phase_name} over")
                break

            index = (index + 1) % len(self.players)
            """
            if not self.players[index].folded and not self.players[index].is_all_in():
                print(f"Switching to {self.players[index].name}'s turn, please give the laptop to them")
                input(f"{self.players[index].name}, press enter to continue\n")
                clear_screen()
                pass
            elif self.players[index].is_all_in() and not self.players[index].folded:
                print(f"{self.players[index].name} is all in")
                time.sleep(2)
                index = (index + 1) % len(self.players)
                
            """
            while self.players[index].folded or self.players[index].is_all_in():
                if self.players[index].is_all_in():
                    print(f"{self.players[index].name} is all in")
                    time.sleep(1.5)
                index = (index + 1) % len(self.players)

            print(f"Switching to {self.players[index].name}'s turn, please give the laptop to them")
            input(f"{self.players[index].name}, press enter to continue\n")
            clear_screen()


    def pre_flop(self) -> None:
        """
        handles the pre-flop betting round
        has to be different from the rest because of the blinds
        :return: None
        """
        clear_screen()
        small = (self.dealer_index + 1) % len(self.players)
        big = (self.dealer_index + 2) % len(self.players)
        index = (self.dealer_index + 3) % len(self.players)
        players_acted_since_last_raise = 0

        self.players[small].bet(self.small_blind) 
        self.players[big].bet(self.big_blind)
        self.pot += self.small_blind + self.big_blind
        self.last_raiser_index = big
        self.minimum_bet = self.big_blind
        print(f"small blind is {self.players[small].name} and has bet {self.small_blind}")
        print(f"big blind is {self.players[big].name} and has bet {self.big_blind}\n")

        print(f"{self.players[index].name} is up")
        time.sleep(3)

        while True:
            if self.only_one_player_remaining():
                print('Only one player remaining')
                break

            player = self.players[index] 

            if not player.folded and not player.is_all_in():
                self.handle_player_action(player)
                if not player.folded:
                    if player.current_bet > self.minimum_bet:
                        players_acted_since_last_raise = 1
                        self.minimum_bet = player.current_bet
                        self.last_raiser_index = index
                    else:
                        players_acted_since_last_raise += 1

            clear_screen()

            print(f"index: {index}")
            print(f"last_raiser_index: {self.last_raiser_index}")
            print(f"{index == self.last_raiser_index}")
            print(f"players_acted_since_last_raise: {players_acted_since_last_raise}")
            print(f"players: {len([p for p in self.players if not p.folded])}")
            print(f"{players_acted_since_last_raise >= len([p for p in self.players if not p.folded])}")
            print(f"all_bets_equal: {self.all_bets_equal()}")


            # same thing with this line since they're the same
            if (index == self.last_raiser_index or players_acted_since_last_raise >= len([p for p in self.players if not p.folded])) and self.all_bets_equal():
                clear_screen()
                print("Preflop over")
                break

            index = (index + 1) % len(self.players)

            """
            if not self.players[index].folded:
                if self.players[index].is_all_in():
                    print(f"{self.players[index].name} is all in")
                    index = (index + 1) % len(self.players)
                
                else:
                    print(f"Switching to {self.players[index].name}'s turn, please give the laptop to them")
                    input(f"{self.players[index].name}, press enter to continue\n")
                    clear_screen()
                    pass
            """

            while self.players[index].folded or self.players[index].is_all_in():
                if self.players[index].is_all_in():
                    print(f"{self.players[index].name} is all in")
                    time.sleep(1.5)
                index = (index + 1) % len(self.players)

            print(f"Switching to {self.players[index].name}'s turn, please give the laptop to them")
            input(f"{self.players[index].name}, press enter to continue\n")
            clear_screen()
