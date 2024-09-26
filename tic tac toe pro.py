#this is a python code for tic tac toe for python intermediates
#this game allows the user to either play with a ai or a companion
import random

class TicTacToe:
    def __init__(self):
        # Initialize the board
        self.board = [' ' for _ in range(9)]  # A list to hold the state of the 9 spaces
        self.current_winner = None  # To keep track of the winner
    
    def print_board(self):
        # This is just printing the board in rows of 3
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
    
    @staticmethod
    def print_board_nums():
        # Tells what number corresponds to what box
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        # If the move is valid, make the move (assign the square to the letter)
        # Then return True. If invalid, return False.
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check the row, column, and diagonals for a win condition
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False


def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'  # Starting letter
    # Iterate while the game still has empty squares
    while game.empty_squares():
        if game.num_empty_squares() == 0:
            break

        # Get the move from the appropriate player
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        # Let's define a function to make a move
        if game.make_move(square, letter):
            if print_game:
                print(f'{letter} makes a move to square {square}')
                game.print_board()
                print('')  # Just empty line

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter  # Ends the loop and exits the game

            # After a move, we need to alternate letters
            letter = 'O' if letter == 'X' else 'X'

        # Small pause to reduce CPU usage
        if print_game:
            print('Waiting for next move...')

    if print_game:
        print("It's a tie!")


class HumanPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8): ')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val


class RandomComputerPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class SmartComputerPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            return random.choice(game.available_moves())  # Random first move
        else:
            # Use minimax algorithm for better moves
            return self.minimax(game, self.letter)['position']

    def minimax(self, state, player):
        max_player = self.letter  # AI is the max player
        other_player = 'O' if player == 'X' else 'X'

        # First, check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                    state.num_empty_squares() + 1)}
        elif not state.empty_squares():  # No empty squares
            return {'position': None, 'score': 0}

        # Initialize some variables
        if player == max_player:
            best = {'position': None, 'score': -float('inf')}  # Want to maximize
        else:
            best = {'position': None, 'score': float('inf')}  # Want to minimize

        for possible_move in state.available_moves():
            # Make a move, try that spot
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)  # Simulate the game after the move

            # Undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # Keep track of the move

            # Update the best move based on the player
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best


if __name__ == '__main__':
    while True:
        t = TicTacToe()
        choice = input('Do you want to play against AI (y/n)? ')
        if choice.lower() == 'y':
            x_player = SmartComputerPlayer('X')
            o_player = HumanPlayer('O')
        else:
            x_player = HumanPlayer('X')
            o_player = HumanPlayer('O')

        play(t, x_player, o_player, print_game=True)

        play_again = input('Play again? (y/n): ')
        if play_again.lower() != 'y':
            break
