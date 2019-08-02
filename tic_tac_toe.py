"""
A Tic Tac Toe Game/s for two players
"""

from time import sleep

def is_winner(board, last_player):
    """Checks if there is a winner given a board, if so announce him and return True,
     otherwise return False"""
    # DOCSTRING: Checks if there is a winner given a board, if so announce him and return True,
    # otherwise return False
    # INPUT: board - the given board, last_player - the last player who made a move in the game
    # OUTPUT: True if there is a winner, False otherwise

    # If there is a winner
    if (board[1] == board[2] == board[3] != '') or (board[4] == board[5] == board[6] != '') \
            or (board[7] == board[8] == board[9] != '') or (board[1] == board[4] == board[7] != '')\
            or (board[2] == board[5] == board[8] != '') or (board[3] == board[6] == board[9] != '')\
            or (board[1] == board[5] == board[9] != '') or (board[3] == board[5] == board[7] != ''):
        print(f'\n{last_player} is the Winner!\n')
        return True

    # Else there is no winner
    return False


def start_game():
    """Initialing a new game"""
    # DOCSTRING: Initialing a new game
    # INPUT: player1 - the first player, player2: the second player, board - the board to play on
    # OUTPUT: the first player ('X' or 'O')

    # Prints the opening screen for the game
    player1 = input('\nPlayer 1, do you want to be X or O?: (X/O)\n')
    player2 = ''

    # To determine whether the answer is valid or not, we use a boolean variable
    # (we first assume it is not)
    valid = False

    # Checks if the answer given by the player was valid, otherwise keep asking
    while not valid:
        if player1 in ('X', 'x'):
            player2 = 'O'
            valid = True
        elif player1 in ('O', 'o'):
            player2 = 'X'
            valid = True
        else:
            player1 = input('\nA player can be either X or O, please choose again:\n')

    print(f'\nPlayer 1 is {player1.upper()}, Player 2 is {player2.upper()}')
    sleep(2)
    return player1.upper()


def print_board(board):
    """Prints the given board"""
    # DOCSTRING: Prints the given board
    # INPUT: board - the board to print
    # OUTPUT: void

    print()
    print(board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('--------')
    print(board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('--------')
    print(board[1] + ' | ' + board[2] + ' | ' + board[3])
    print()


def one_game():
    """Runs one game of Tic Tac Toe"""
    # DOCSTRING: Runs one game of Tic Tac Toe
    # INPUT: none
    # OUTPUT: void

    # initializes board and players
    board = [''] * 10
    player1 = start_game()

    # Determine player 2 based on player 1's choice
    if player1 == 'X':
        player2 = 'O'
    else:
        # Else, player1 = 'O'
        player2 = 'X'

    print_board(board)

    # To determine whose move it is, we use a counter
    counter = 0

    # To determine if the game has ended, we use a boolean variable
    terminate = False

    # While there is no winner and the game has not ended yet, keep playing
    while not terminate and counter < 9:

        # The players's move will be stored as an integer variable
        spot = 0

        # Checks if the answer given by the player is valid, otherwise keep asking
        while spot not in range(1, 10) or board[int(spot)] != '' or spot != int(spot):
            if counter % 2 == 0:
                try:
                    spot = float(input(f'Player 1, please enter a move: (1-9)\n'))
                except ValueError:
                    # Assign spot to some not valid integer in case user's answer was not a number
                    spot = 0
            else:
                try:
                    spot = float(input(f'Player 2, please enter a move: (1-9)\n'))
                except ValueError:
                    # Assign spot to some not valid integer in case user's answer was not a number
                    spot = 0

            # If the answer is not valid
            if spot != int(spot) or spot not in range(1, 10):
                print('\nThe move should be an integer between 1 to 9, please try again\n')
                sleep(1.5)

            # If the spot is taken
            elif board[int(spot)] != '':
                print('\nThis spot is already taken, please try a different spot\n')
                sleep(1.5)

        # Convert float to int
        spot = int(spot)

        # If this is player 1's turn - write his move on the board
        if counter % 2 == 0:
            board[spot] = player1

        # Else write player 2's move on the board
        else:
            board[spot] = player2

        print_board(board)

        # If player 1 made the last move:
        if counter % 2 == 0:
            terminate = is_winner(board, "Player 1")
        # Else player 2 made the last move
        else:
            terminate = is_winner(board, "Player 2")

        # If there is no winner yet:
        if not terminate:
            counter += 1

    # If there is a tie:
    if counter == 9:
        print('The game has ended in a tie!\n')


def tic_tac_toe():
    """Runs games of Tic Tac Toe until the players terminate"""

    print('\nWelcome to the Tic Tac Toe game!\n')
    sleep(1)

    another_game = True
    answer = ''

    # While the players want to play:
    while another_game:

        one_game()

        sleep(2)
        answer = input('Do you want to play another game?: (Yes/No)\n')

        # To determine whether the answer is valid , we use a boolean variable
        # (we first assume it is not):
        valid = False

        # Checks if the answer given by the player was valid, otherwise keep asking
        while not valid:
            if answer.lower() == 'yes':
                another_game = True
                valid = True
            elif answer.lower() == 'no':
                another_game = False
                valid = True
            # Else the answer was not valid, ask again:
            else:
                answer = input('The answer should be "Yes" or "No" only, please enter again:\n')
                valid = False
        sleep(1)
    print('\nThank you for playing,')
    print('Goodbye!')


if __name__ == "__main__":
    tic_tac_toe()
