"""
This is the main file for the poker game. This program was the most challenging program I've ever had to write by far.
Overall time spent on this project was about 35-40 hours over the course of about three weeks. I spent a lot of time
trying to figure out how to implement the game logic, including how to evaluate hands and to loop through the players.
I'm really proud of myself for finishing the project and I taught me a lot about both Python and myself as a programmer.

Thanks for having the most fun two classes of my day this year Mr. Perry (and the most fun one sophomore year)!
I'll forever remember the times spent in your classes and cherish upon them. Have a great summer and I hope to
see you again in the future! -Justin Schmid

Feel free to use this as you please for examples or whatever else. One last time, thank you for everything! Your classes
inspired me to become a programmer!
"""

from player import Player
from game import Game

def main() -> None:
    """
    main function to start the game
    :return: None
    """
    while True:
        try:
            num_players = int(input("How many players? (3-8) "))
            if num_players <= 2 or num_players > 8:
                print("Players must be between 3 and 8")
                continue
            break
        except ValueError:
            print("Invalid input. Please try again.")


    print()
    players: list[Player] = []
    names: list[str] = []
    chips: list[int] = []
        

    for i in range(num_players):
        while True:
            name = input(f"Player {i + 1} name? ")
            if name in names:
                print("Name already taken. Please try again.")
                continue
            names.append(name)
            break

    print()

    for i in range(num_players):
        while True:
            try:
                chip = int(input(f"How many chips for {names[i]}? "))
                if chip <= 0:
                    print("Chips must be greater than 0.")
                    continue
                chips.append(chip)
                break
            except ValueError:
                print("Invalid input. Please try again.")

    print()
        
    players.extend([Player(name, chip) for name, chip in zip(names, chips)])

    game = Game(players)
    game.play()


if __name__ == '__main__': # ensures that the main function is only called when the script is run directly
    main()