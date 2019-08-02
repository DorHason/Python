"""
Black Jack game - multiplayer
The Dealer is the computer, the player/s are user/s
"""
from random import randint
from time import sleep


class Player:
    """ Represent a player in the game. Each player has a hand (cards), amount of money,
    a bet for each round and a boolean variable for telling if he busted or not"""

    def __init__(self, name='', money=0, hand=[], bet=0, not_busted=True):
        """ A constructor method """
        # INPUT: name - the player's name
        # money - the amount of money the player starts the game with
        # hand - the cards that the player holds, represented by a list
        # bet - the current player's bet
        # not_busted - a boolean determines if the player is busted
        self.name = name
        self.money = money
        self.hand = hand
        self.bet = bet
        self.not_busted = not_busted

    def calculate_sum(self):
        """ Calculates and returns the value of the current player's hand (his cards) """
        players_sum = 0
        for card in self.hand:
            players_sum += card[1]
        while players_sum > 21 and ('Ace', 11) in self.hand:
            index = self.hand.index(('Ace', 11))
            self.hand[index] = ('Ace', 1)
            players_sum -= 10
        return players_sum

    def hit(self, deck):
        """ Gives a new card to the player's hand, from the given deck"""
        # INPUT: deck - the given deck to take the card from
        self.hand.append(deck.get_card())

    def loses(self):
        """ Removes the amount of the bet from the player's register.
        Should be called only if the player lost"""
        self.money -= self.bet

    def wins(self):
        """ Adds the amount of the bet to the player's register.
        Should be called only if the player won"""
        self.money += self.bet

    def __str__(self):
        """ A string representation for an instance of Player
         Returns the current cards in the player's hand"""
        hand_string = ''
        for card in self.hand:
            hand_string += f"{card[0]}  "
        return hand_string


class Deck:
    """ Represent a deck of cards """

    cards = [('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8),
             ('9', 9), ('10', 10), ('J', 10), ('Q', 10), ('K', 10), ('Ace', 11)] * 4

    # cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4

    def __init__(self, decks=1):
        """ A constructor method """
        # INPUT: decks - the number of decks to create
        self.decks = decks

    def get_card(self):
        """ Returns a random card from the deck """
        return Deck.cards.pop(randint(0, len(Deck.cards) - 1))

    def new_deck(self):
        """ Returns all cards to the deck.
        After calling this method all the cards are in the deck"""
        Deck.cards = [('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7),
                      ('8', 8), ('9', 9), ('10', 10), ('J', 10), ('Q', 10), ('K', 10), ('Ace', 11)]\
                     * 4 * self.decks


class Table:
    """ Represent a table of the game. The table comprised of the Dealer, players
    and a deck of cards"""

    def __init__(self, players=[], cards=Deck()):
        """ A constructor method """
        # INPUT: players - the players in the table, represented by a list
        # By default players[0] is the dealer
        # cards - the cards to be played in the game
        self.players = players
        self.cards = cards

    def new_round(self):
        """ Gives a new pair of cards for each player in the game, including the Dealer
        and resets the players's boolean attribute (not_busted)"""
        # Reset cards
        self.cards.new_deck()

        # Give new cards to the Dealer
        self.players[0].hand = []
        self.players[0].hand.append(self.cards.get_card())
        self.players[0].hand.append(self.cards.get_card())
        # Give new cards to each player and reset their boolean attribute
        for player in self.players[1:]:
            # Reset hand
            player.not_busted = True
            player.hand = []
            player.hand.append(self.cards.get_card())
            player.hand.append(self.cards.get_card())


def round(players):
    """ Play one round of the game """
    # INPUT: players = array of players
    # By default players[0] is the dealer

    # Initialize a new table
    # Compute the ratio of decks in the game (A deck for every 3 players, approximately)
    table = Table(players, Deck(int(len(players) / 3) + 1))
    table.new_round()

    # Reveal dealer's card
    sleep(1)
    print(f"\nThe Dealer's first card: {players[0].hand[0][0]}\n")
    sleep(2)

    # Skip the Dealer
    for player in players[1:]:

        # Place a bet and check validation
        print(f"{player.name}, you have ${player.money} left\n")
        sleep(1)
        valid = False
        while not valid:
            try:
                bet = int(input(f"{player.name}, please enter your bet:\n"))
            except ValueError:
                print("The bet must be an integer, please try again\n")
                continue
            if bet > player.money:
                print(f"You don't have this amount of money (${player.money} left), "
                      f"please try again\n")
                valid = False
                continue
            elif bet < 1:
                print("The bet must be a positive integer, please try again\n")
                valid = False
                continue
            valid = True
            # Set player's bet
            player.bet = bet

        # Reveals player's hand
        print(f"{player.name}, your currently hand is: {player}\n")
        # If the player got a Blackjack, he can't proceed and his turn is automatically skipped
        if player.calculate_sum() == 21:
            print("Blackjack!\n")
            sleep(2)
            continue

        # Player's turn
        choice = input(f"{player.name} please enter your move: ('hit'/'stand')\n")

        # Check if answer valid, if not try again until it is
        while choice.lower() not in ('hit', 'stand'):
            print("Please enter 'hit' or 'stand' only\n")
            choice = input(f"{player.name}, please enter your move: ('hit'/'stand')\n")

        # If the player chose to hit, continue until he stands or until he busted
        while choice.lower() == 'hit' and player.calculate_sum() <= 21:
            player.hit(table.cards)
            print(f"{player.name}, your currently hand is: {player}\n")
            # If the player is busted
            if player.calculate_sum() > 21:
                print("Busted\n")
                sleep(2)
                player.not_busted = False
                player.loses()
                # If the player loses all of his money, he is out of the game
                if player.money == 0:
                    sleep(1)
                    print(f"{player.name} you have no money left, thus you are out of the game\n")
                    sleep(2)
                    index = players.index(player)
                    players.pop(index)
                break
            # Ask the player what he wants to do
            choice = input(f"{player.name}, please enter your move: ('hit'/'stand')\n")
            # Check if answer valid, if not try again until it is
            while choice.lower() not in ('hit', 'stand'):
                print("Please enter 'hit' or 'stand' only")
                choice = input(f"{player.name}, please enter your move: ('hit'/'stand')\n")

    # Dealer's turn
    max_hand = 0
    # Find the strongest hand that left in the round
    for player in players[1:]:
        hand = player.calculate_sum()
        if max_hand < hand <= 21:
            max_hand = hand
    # Reveals Dealer's hand
    print(f"Dealer's hand:  {players[0]}\n")
    dealers_hand = players[0].calculate_sum()
    # Dealer's hand must be stronger or equal to all players's hands
    while dealers_hand < max_hand and dealers_hand <= 21:
        players[0].hit(table.cards)
        print("The Dealer hit")
        sleep(2)
        print(f"{players[0]}\n")
        dealers_hand = players[0].calculate_sum()
    # If the Dealer is busted, every not-busted player gets his bet
    if dealers_hand > 21:
        print("The Dealer is busted\n")
        for player in players[1:]:
            if player.not_busted:
                print(f"{player.name} gets ${player.bet}")
                player.wins()
    # Otherwise only non-busted players who defeated the dealer win their bet,
    # and non-busted players who were defeated by the Dealer lose their bet
    else:
        for player in players[1:]:
            if player.not_busted and player.calculate_sum() > dealers_hand:
                player.wins()
            elif player.not_busted and player.calculate_sum() < dealers_hand:
                player.loses()
                # If the player loses all of his money, he is out of the game
                if player.money == 0:
                    sleep(1)
                    print(f"{player.name} you have no money left, thus you are out of the game\n")
                    sleep(2)
                    index = players.index(player)
                    players.pop(index)

    # consider to change: dealers_hand -> dealer_hand, calculate_sum -> calculate_hand


def game():
    """ Runs a game of black jack """
    # Opening screen
    print("Welcome to the Black Jack game!\n")
    counter = 1
    # Set the dealer to be the player in index 0
    dealer = Player('Dealer')
    players = [dealer]
    # Add players to the game, as much as the user wants
    while True:
        # Enter the player's name
        name = input(f"Player {counter}, please enter your name:")
        # Enter amount of money for the game (for this player), and check validation
        valid = False
        while not valid:
            try:
                money = int(input(f"{name}, please enter amount of money for the game:\n"))
            except ValueError:
                print("The amount must be an integer, please try again\n")
                continue
            if money < 1:
                print("The amount must be a positive integer, please try again\n")
                valid = False
                continue
            valid = True
        # Set the player
        player = Player(name, money)
        # Check for another players, and check for validation in the answer
        another = input("Is there another player who wants to play? ('Yes'/'No')\n")
        while True:
            if another.lower() in ('yes', 'no'):
                break
            print("Answer must be 'Yes' or 'No', please try again\n")
            another = input("Is there another player who wants to play? ('Yes'/'No')\n")
        # Add the player to the list of players for the game
        players.append(player)
        if another.lower() == 'no':
            break
        counter += 1
    # Run rounds of the game
    while True:
        # Check if there are players with money left in the game, if not end the game
        # A reminder: by default players[0] is the Dealer
        if len(players) == 1:
            print("\n\nThere are no participants with money left in the game - the game has ended")
            break
        # Run one round
        round(players)
        # Ask the user if he wants to play another round, and check for validation in the answer
        if len(players) > 1:
            answer = input("Do you want to play another round? ('Yes'/'No')\n")
            while True:
                if answer.lower() in ('yes', 'no'):
                    break
                print("Answer must be 'Yes' or 'No', please try again\n")
                answer = input("Do you want to play another round? ('Yes'/'No')\n")
            if answer.lower() == 'no':
                break
    # Goodbye screen
    print("\nThank you for playing")
    print("Goodbye!\n")


if __name__ == '__main__':
    game()
