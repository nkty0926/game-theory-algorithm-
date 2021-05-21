'''
// Main File:        teeko2_player.py
// Semester:         CS 540 Fall 2020
// Authors:          Tae Yong Namkoong
// CS Login:         namkoong
// NetID:            kiatvithayak
// References:       TA's Office Hours
                    https://sandipanweb.wordpress.com/2017/03/06/using-minimax-with-alpha-beta-pruning-and-heuristic-evaluation-to-solve-2048-game-with-computer/
                     https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
                     https://www.javatpoint.com/mini-max-algorithm-in-ai
                     https://www.baeldung.com/java-minimax-algorithm

'''
import random
import time
import copy
class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def position_pieces(self, state):
        """
        This method  positions the pieces on the board
        :param state: current state of the board
        :return: pieces position
        """
        black_pieces = []
        red_pieces = []
        for i in range(5):
            for j in range(5):
                position = state[i][j]
                if position == 'b':
                    black_pieces.append((i, j))
                elif position == 'r':
                    red_pieces.append((i, j))
                else:
                    pass
        return black_pieces, red_pieces
    def get_succ(self, state, curr_player):
        """
        This method returns all succ for a given player
        :param state: the board's current state
        :param curr_player: which player is playing
        :return: returns a list of move from to move to
        """
        num = 0
        drop_phase = True
        default_pos = [(2, 2), (2, 2)]
        # all directions for board
        orientations = [(1, 0), (-1, 0), (0, -1), (0, 1), (-1, 1), (1, 1), (1, -1), (-1, -1)]

        for i in range(5):
            for j in range(5):
                if state[i][j] != ' ':
                    num += 1
        if num == 0:
            return [default_pos]
        if num == 8:
            drop_phase = False

        if drop_phase:
            succ = []
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        new_pos = [(i, j), (i, j)]
                        succ.append(new_pos)
            return succ

        black_pieces, red_pieces = self.position_pieces(state)
        succ = []
        if curr_player == 'b':
            pieces = black_pieces
        else:
            pieces = red_pieces

        for piece in pieces:
            for orientation in orientations:
                new_piece = (piece[0] + orientation[0], piece[1] + orientation[1])
                if new_piece[0] in range(5) and new_piece[1] in range(5) \
                        and new_piece not in black_pieces and new_piece not in red_pieces:
                    succ.append([piece, new_piece])
        return succ

    def heuristic_game_value(self, state, curr_player):
        """
         function to evaluate non-terminal states. (You should call game_value(state) from this function to
         determine whether state is a terminal state before you start evaluating it heuristically.)
         This function should return some float value between 1 and -1.
        :param state: board's current state
        :param curr_player: player's turn
        :return: heuristic value
        """
        black_pieces, red_pieces = self.position_pieces(state)
        sigma = 0
        if curr_player == 'b':
            pieces = black_pieces
        else:
            pieces = red_pieces

        for piece in pieces:
            minimum = 100
            arr = [p for p in pieces if p != piece]
            for element in arr:
                minimum = min(abs(element[0] - piece[0]) + abs(element[1] - piece[1]), minimum)
            sigma += minimum
        heuristic = 1 / sigma
        return heuristic

    def max_value(self, state, depth):
        """
        recursive max value finding function
        :param state: board's current state
        :param depth: depth
        :return: max value
        """
        if depth == 0:
            return self.heuristic_game_value(state, self.my_piece)
        if self.game_value(state) != 0:
            return self.game_value(state)
        a = -2
        successors = self.get_succ(state, self.my_piece)
        for succ in successors:
            copy_state = [row[:] for row in state]
            copy_state[succ[0][0]][succ[0][1]] = ' '
            copy_state[succ[1][0]][succ[1][1]] = self.my_piece
            a = max(self.min_value(copy_state, depth - 1), a)
        return a

    def min_value(self, state, depth):
        """
        recursive min value finding function
        :param state: board's current state
        :param depth: depth
        :return: min value
        """
        if depth == 0:
            return self.heuristic_game_value(state, self.opp)
        if self.game_value(state) != 0:
            return self.game_value(state)
        b = 2
        successors = self.get_succ(state, self.opp)
        for succ in successors:
            new_state = [row[:] for row in state]
            new_state[succ[0][0]][succ[0][1]] = ' '
            new_state[succ[1][0]][succ[1][1]] = self.opp
            b = min(self.max_value(new_state, depth - 1),b)
        return b

    def mini_max(self, state, depth):
        threshold = -2
        if depth < 1:
            raise Exception("depth must be greater than 0")
        successors = self.get_succ(state, self.my_piece)
        for succ in successors:
            copy_state = [row[:] for row in state]
            copy_state[succ[0][0]][succ[0][1]] = ' '
            copy_state[succ[1][0]][succ[1][1]] = self.my_piece
            if threshold < self.min_value(copy_state, depth - 1):
                move_piece = succ
            threshold = max(threshold, self.min_value(copy_state, depth - 1))

        move_piece = [move_piece[1], move_piece[0]]
        return move_piece

    def drop_minimax(self, depth, state):
        """
        this function finds minimax during drop_phase
        :param state: board's current state
        :param depth: depth when algo ends
        :return: valid moves
        """
        return [self.mini_max(state, depth)[0]]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        num = 0
        start_time = time.time()
        drop_phase = True  # TODO: detect drop phase

        for i in range(5):
            for j in range(5):
                if state[i][j] != ' ':
                    num += 1
        if num == 8:
            drop_phase = False

        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            move = self.mini_max(state, 4)
            end_time = time.time()
            t = end_time - start_time
            print('Time: ', t)
            return move
            pass

        else:
            move = self.drop_minimax(2, state)
            end_time = time.time()
            t = end_time - start_time
            print('Time: ', t)
            return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and diamond wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][
                    col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # TODO: check \ diagonal wins
        for row in range(2):
            for i in range(2):
                if state[row][i] != ' ' and state[row][i] == state[row + 1][i + 1] == state[row + 2][i + 2] == \
                        state[row + 3][i + 3]:
                    return 1 if state[row][i] == self.my_piece else -1

        # TODO: check / diagonal wins // WORKS
        for row in range(3, 5):
            for i in range(2):
                if state[row][i] != ' ' and state[row][i] == state[row - 1][i + 1] == state[row - 2][i + 2] == \
                        state[row - 3][i + 3]:
                    return 1 if state[row][i] == self.my_piece else -1

        # TODO: check diamond wins
        for row in range(3):
            for i in range(1, 4):
                if state[row][i] != ' ' and state[row][i] == state[row + 2][i] == state[row + 1][i - 1] == \
                        state[row + 1][
                            i + 1]:
                    return 1 if state[row][i] == self.my_piece else -1
        return 0


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
