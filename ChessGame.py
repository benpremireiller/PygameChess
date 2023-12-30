import re
import pygame


class ChessVar:
    """
    Represents a game of chess:
    The game is over once a king is put into check mate

    Use the make_move() method to alter the state of the board

    Change the self._board data member to the test_board for testing purposes
    """

    def __init__(self):

        # Define the boards
        official_board = [
            [Rook('black'), Knight('black'), Bishop('black'), Queen('black'), King('black'), Bishop('black'), Knight('black'), Rook('black')],
            [Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black')],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white')],
            [Rook('white'), Knight('white'), Bishop('white'), Queen('white'), King('white'), Bishop('white'), Knight('white'),Rook('white')]
        ]

        test_board = [
            [Rook('black'), Knight('black'), Bishop('black'), None, None, None, Rook('black'), King('black')],
            [Bishop('black'), None, None, Pawn('black'), None, Pawn('black'), None, None],
            [None, None, Pawn('black'), None, None, Knight('black'), None, Bishop('black')],
            [None, None, None, None, None, None, None, None],
            [None, Bishop('white'), None, None, None, None, None, None],
            [None, Pawn('white'), Queen('black'), None, None, Pawn('black'), None, Pawn('white')],
            [King('white'), None, Pawn('white'), Pawn('white'), None, None, Pawn('white'), None],
            [Rook('white'), None, None, None, None, Bishop('white'), Knight('white'), Rook('white')]
        ]

        self._board = official_board  # Switch this to test

        # Define the piece dictionary and fill the list
        self._piece_positions_dict = {'white': [], 'black': []}
        self.fill_piece_dictionary()

        # Keep track of turns
        self._active_player = 'white'  # White starts
        self._opponent_player = 'black'

        self._col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}  # Map col letters to list indices

        self._game_state = 'UNFINISHED'

        # Define the last move dict. This is used to revert test and invalid moves.
        self._last_move = {
            'move_from': None,
            'move_to': None,
            'moving_piece': None,
            'captured_piece': None
        }

    def fill_piece_dictionary(self) -> None:
        """
        Add piece positions to the piece position dictionary
        This dict makes working with checking if spaces are occupied by pieces easier
        """

        # Loop through the board and add all pieces to the piece position dictionary
        for i, row in enumerate(self._board):
            for j, cell in enumerate(row):
                if cell is not None:  # A piece
                    piece_color = cell.get_color()
                    self._piece_positions_dict[piece_color].append((i, j))

    def get_piece_positions(self, piece_name: str, color: str) -> list:
        """
        Return the positions of the pieces for the piece_name with the provided color
        """

        positions = []

        for position in self._piece_positions_dict[color]:
            row, col = position
            if self._board[row][col].get_class_name() == piece_name:
                positions.append(position)

        return positions

    def position_is_on_board(self, position: tuple) -> bool:
        """
        Static helper method which returns True if the position passed is on the board.
        Takes the form (row, col) as a tuple
        """

        row, col = position

        return 0 <= row <= 7 and 0 <= col <= 7

    def print_board(self) -> None:
        """
        Prints the board in a user-friendly format with row and column headers
        """

        # Print columns first
        print('  ', end='')  # Need a spot for the row header
        for letter in self._col_map:
            print(letter, end=' ')
        print()  # New line

        # Print the row header then the rows
        for i, row in enumerate(self._board):
            print(8 - i, end=' ')  # Row header
            for cell in row:
                if cell is None:
                    print(' ', end=' ')
                else:
                    print(cell.get_visual(), end=' ')
            print()

    def get_other_color(self, color):
        """
        Return the 'other' color
        If the color argument is 'black', return 'white'
        If the color argument is 'white', return 'black'
        """

        other_color, = list({'white', 'black'} - {color})  # Uses set difference operation
        return other_color

    def get_game_state(self):
        """Return the game state"""

        return self._game_state

    def end_game(self):
        """
        Set the game state to a winning state based on the active player
        """

        self._game_state = f'{self._active_player.upper()}_WINS'

    def decode_player_input(self, move: str) -> tuple:
        """
        Takes a string in the form 'a1' and returns two integers as a tuple which matches the inputted move
        to the coordinates in the board list.

        The string must be a letter between a and h directly followed by a number between 1 and 8
        """

        col_index = self._col_map[move[0]]
        row_index = 8 - int(move[1])  # 8 minus because the board is reversed

        return col_index, row_index

    def make_move(self, move_from: str, move_to: str) -> bool:
        """
        Make a move in the following format: move_from('a3', 'a2')
        This method verifies the ongoing status of the game. If the game is still active, it proceeds to validate the proposed move.
        If the move is valid, it relocates the piece then returns True. Otherwise, it returns False.
        """

        # Check that the game is still in progress
        if self._game_state != 'UNFINISHED':
            return False

        # Make sure the move is valid within the board
        is_valid_from_move = True if re.match('^[a-hA-H][1-8]$', move_from) else False
        is_valid_to_move = True if re.match('^[a-hA-H][1-8]$', move_from) else False

        if not is_valid_to_move or not is_valid_from_move:
            print('Invalid coordinates')
            return False

        # Decode the move into int, int format
        from_col, from_row = self.decode_player_input(move_from)
        to_col, to_row = self.decode_player_input(move_to)

        # Get the cells at the coordinates
        from_cell = self._board[from_row][from_col]

        if from_cell is None:  # No piece
            print('No piece at position entered')
            return False

        if from_cell.get_color() != self._active_player:  # Piece is not the players
            print('Piece does not belong to you')
            return False

        # Check if the move is in the set of available moves for the piece
        to_positions, remove_positions = self.get_available_moves(from_cell, from_row, from_col)

        move_from_position = (from_row, from_col)
        move_to_position = (to_row, to_col)

        if move_to_position not in to_positions:
            print('Invalid move')
            return False

        # Get the corresponding remove_from position for the associated move (needed for en passant moves)
        remove_position = remove_positions[to_positions.index(move_to_position)]
        move_to_data = (move_to_position, remove_position)

        # Check if the move results in the active player's king being in check
        self.update_board_positions(move_from_position, move_to_data, self._active_player)

        player_is_in_check = self.check_for_check(self._active_player)

        # If the player is in check as a result of the move, it is invalid
        if player_is_in_check:
            print('Move results in King being in check')
            self.revert_last_move()
            return False

        # Update that the piece has already moved
        from_cell.update_has_already_moved()

        # Check if there is a checkmate and end game if so
        is_check_mate = self.check_for_mate()

        if is_check_mate:
            print('Check mate!')
            self.end_game()
            return True

        # Update player turns
        self._active_player, self._opponent_player = self._opponent_player, self._active_player

    def update_board_positions(self, from_position: tuple, to_move: list, moving_color: str) -> None:
        """
        Move the piece at the from_position by using the data in the to_move
        The to_move argument contains a list with a to_position and a remove_position which indicate the position the piece
        should move to and the position which the opponent piece should be removed from, respectively.
        """

        opponent_color = self.get_other_color(moving_color)

        # Unpack to_move data
        to_position, remove_position = to_move

        # Get the moving coordinates
        from_row, from_col = from_position
        to_row, to_col = to_position
        from_piece = self._board[from_row][from_col]
        remove_piece = None

        # Remove the opponent piece from the board and dict if the move is a capture
        if remove_position is not None:
            remove_row, remove_col = remove_position
            remove_piece = self._board[remove_row][remove_col]
            self._board[remove_row][remove_col] = None
            self._piece_positions_dict[opponent_color].remove(remove_position)

        # Move the piece to the new position
        self._board[from_row][from_col] = None
        self._board[to_row][to_col] = from_piece

        self._piece_positions_dict[moving_color].remove(from_position)
        self._piece_positions_dict[moving_color].append(to_position)

        # Check for queening piece
        if isinstance(from_piece, Pawn) and from_piece.get_end_row() == to_row: # Pawn has reached the end
            self.add_queen_at_position(to_row, to_col, moving_color)

        # Convert to lists incase we need to add a move (for knighting)
        from_position, to_position, from_piece = [from_position], [to_position], [from_piece]

        # Check if the move is a castling move
        col_distance = to_col - from_col
        if isinstance(from_piece[0], King) and abs(col_distance) > 1: # Kings will only move at least two spaces if castling

            # Get the rooks from and to positions
            orientation = (col_distance > 0) - (col_distance < 0) # 1 is right, -1 is left
            rook_col = 7 if orientation == 1 else 0 # If king moving right, then rook at far right (col index 7) and vice versa

            rook_from_position = (from_row, rook_col)
            rook_to_position = (from_row, to_col - orientation) # Right before or after the king col
            rook_move = (rook_to_position, None)
            rook_piece = self._board[from_row][rook_col]

            # Recurse this method to move the rook
            self.update_board_positions(rook_from_position, rook_move, moving_color)

            # Append the rook move to the lists we will use to update the last move
            from_position.append(rook_from_position)
            to_position.append(rook_to_position)
            from_piece.append(rook_piece)

        # Set the last move
        self._last_move = {
            'move_from': from_position,
            'move_to': to_position,
            'moving_piece': from_piece,
            'captured_piece': remove_piece
        }

    def revert_last_move(self) -> None:
        """Revert the board list and position dict to their state right before the last move that occurred"""

        moves_from, moves_to, moving_pieces, captured_piece = self._last_move.values()

        # Loop through the piece moves in the last move
        for move_from, move_to, moving_piece in zip(moves_from, moves_to, moving_pieces):

            from_row, from_col = move_from
            to_row, to_col = move_to

            # Move the pieces back to their move_from positions on the board and the position dict
            self._board[from_row][from_col] = self._board[to_row][to_col]
            self._board[to_row][to_col] = captured_piece # This will be None if the move wasn't a capture

            self._piece_positions_dict[moving_piece.get_color()].remove(move_to)
            self._piece_positions_dict[moving_piece.get_color()].append(move_from)

            # If the move was a capture, return the piece to the board
            if captured_piece is not None: # This can't happen for knighting
                captured_color = captured_piece.get_color()
                self._piece_positions_dict[captured_color].append(move_to)



    def get_available_moves(self, piece, from_row: int, from_col: int):
        """
        Get the available moves for a particular piece on the board.
        This method will fetch the available moves for the inputted piece based on its allowed movement rules

        Returns a tuple with two elements. The first element is a list of legal 'move to' positions and the
        second element is a list of 'remove from' positions which correspond to the positions we need to remove opponent
        pieces from for each 'move to' move. The reason we need a remove from position is it may be different from
        the move_to_positions for en passant captures (pawns). If the move is not a capture, the 'remove from' value will be None.
        """

        # We will fill these lists with the available moves for the piece
        move_to_positions = []
        remove_from_positions = []

        # Get the piece's allowed rules for moving
        allowed_distance = piece.get_max_allowed_distance()
        allowed_move_orientations = piece.get_allowed_moved_orientations()

        # Get color of the moving piece and opponent for use later
        player_color = piece.get_color()
        opponent_color = self.get_other_color(player_color)

        if isinstance(piece, Knight):  # Knights move in L shape, so we need to handle separately

            def add_knight_move(position_to_check: tuple) -> None:
                """Add valid moves based on what is present at the position_to_check"""

                position_on_board = self.position_is_on_board(position_to_check)
                position_not_players_piece = position_to_check not in self._piece_positions_dict[player_color]
                position_is_opponent_piece = position_to_check in self._piece_positions_dict[opponent_color]

                if position_on_board and position_is_opponent_piece:  # A capture
                    move_to_positions.append(position_to_check)
                    remove_from_positions.append(position_to_check)

                elif position_on_board and position_not_players_piece:  # A move
                    move_to_positions.append(position_to_check)
                    remove_from_positions.append(None)

            # Loop through all possible sets of moves for knights
            for i in [1, -1]:
                for j in [2, -2]:

                    # First check for moves that move one cell vertically then two cells horizontally
                    add_knight_move((from_row + i, from_col + j))

                    # Next check for moves that move two cells vertically then one cell horizontally
                    add_knight_move((from_row + j, from_col + i))

        elif isinstance(piece, Pawn):  # Pawns move only in one direction and capture diagonally (including en passant)

            direction = allowed_move_orientations[0][0]  # The vertical direction (1 or -1)

            # Get regular moves
            dist = 1
            while dist <= allowed_distance:
                forward_cell = self._board[from_row + (dist * direction)][from_col]
                if forward_cell is None:
                    empty_position = (from_row + (dist * direction), from_col)
                    move_to_positions.append(empty_position)
                    remove_from_positions.append(None)
                dist += 1

            # Get captures
            for direct in [1, -1]:  # Right then left

                # Check if capture position has an opponent piece
                forward_diagonal_position = (from_row + direction, from_col + direct)
                forward_cell_is_opponent = forward_diagonal_position in self._piece_positions_dict[opponent_color]

                if forward_cell_is_opponent:
                    move_to_positions.append(forward_diagonal_position)
                    remove_from_positions.append(forward_diagonal_position)

            # Get en passant moves
            last_move_from, last_move_to, last_moving_piece, _ = self._last_move.values()
            if last_moving_piece is None or not isinstance(last_moving_piece[0], Pawn): # If a move hasn't been made yet or the piece isn't a pawn
                return move_to_positions, remove_from_positions

            last_to_row, last_to_col = last_move_to[0] # This variable will be a list of len 2 (for knighting) or 1 (all other moves)
            last_from_row, last_from_col = last_move_from[0]
            vertical_distance_moved_is_two = abs(last_from_row - last_to_row) == 2
            pawn_is_adjacent = last_to_row == from_row and abs(last_to_col - from_col) == 1

            if vertical_distance_moved_is_two and pawn_is_adjacent:
                move_coordinate = (from_row + direction, last_to_col)
                move_to_positions.append(move_coordinate)
                remove_from_positions.append(last_move_to[0])

        else:  # All other pieces move in straight lines

            # Loop through all allowed directions a piece can go
            for orientation in allowed_move_orientations:

                vertical_direction, horizontal_direction = orientation

                # Get the first position that will be checked for legality
                position_offset = (from_row + vertical_direction, from_col + horizontal_direction)
                position_offset_on_board = self.position_is_on_board(position_offset)
                dist = 1

                # Loop until we reach the pieces max allowed distance or the position is not on the board anymore
                while dist <= allowed_distance and position_offset_on_board:

                    cell_is_players_piece = position_offset in self._piece_positions_dict[player_color]
                    if cell_is_players_piece:
                        break  # Stop looping as we've hit a 'wall'

                    cell_is_opponent_piece = position_offset in self._piece_positions_dict[opponent_color]
                    if cell_is_opponent_piece:
                        move_to_positions.append(position_offset)
                        remove_from_positions.append(position_offset)
                        break  # Hit a wall again (that we can capture)

                    # If we've reached here, the cell is empty
                    move_to_positions.append(position_offset)
                    remove_from_positions.append(None)

                    dist += 1

                    # Advance the position offset by one cell in the direction we are checking
                    position_offset = (from_row + (vertical_direction * dist), from_col + (horizontal_direction * dist))
                    position_offset_on_board = self.position_is_on_board(position_offset)

            # Add castling for kings. Kings can only castle if they haven't already moved.
            if isinstance(piece, King) and not piece.get_already_moved():

                rook_positions = self.get_piece_positions('Rook', player_color)

                # Check if the rook can castle
                for rook_position in rook_positions:
                    rook_row, rook_col = rook_position
                    rook_piece = self._board[rook_row][rook_col]

                    # If the rook has already moved, castling in not legal
                    if rook_piece.get_already_moved():
                        continue

                    col_difference = rook_col - from_col

                    # Get orientation to determine queen side or king side castling
                    orientation = (col_difference > 0) - (col_difference < 0)  # -1 is left (queen side), 1 is right (king side)

                    # Check if the path is clear between the king and rook
                    path_is_clear = True
                    offset = 1
                    while offset < abs(col_difference):
                        cell = self._board[from_row][from_col + (offset * orientation)]
                        if cell is not None:
                            path_is_clear = False
                            break
                        offset += 1

                    # If the path is clear, the king hasn't moved and the rook hasn't moved, castling is legal
                    if path_is_clear:
                        king_move_to = (from_row, from_col + ((offset - 1) * orientation))
                        move_to_positions.append(king_move_to)
                        remove_from_positions.append(None)

        return move_to_positions, remove_from_positions

    def check_for_check(self, color: str) -> bool:
        """Return if the kings position is in the set of available moves of the 'color' opponent's pieces"""

        # Get the 'color' player
        players_king_position, = self.get_piece_positions('King', color)  # Only one value will be returned so unpack

        # Create a set we will fill with the opponents moves
        opponent_color = self.get_other_color(color)
        opponent_piece_positions = self._piece_positions_dict[opponent_color]

        # Get the distinct set of moves that the opponent pieces can make
        for opponent_position in opponent_piece_positions:
            row, col = opponent_position
            piece = self._board[row][col]
            to_positions, _ = self.get_available_moves(piece, row, col)

            # If the players king position is in the set of available moves for any opponent piece, the king is in check
            if players_king_position in to_positions:
                return True

        # If we've reached here, the opponent does not have a move at the active player's king position
        return False

    def check_for_mate(self) -> bool:
        """
        Returns true if the opponent (non-active) player is mated and false otherwise
        This method checks if a move that the opponents pieces can make results in the king still being in check

        The opponent could move their king, capture a piece that has the king in check or move a piece in front of
        a piece that has the king in check. This method checks every possible move for simplicity.
        """

        # Check if the non-active player's (opponent) king is currently in check
        king_in_check = self.check_for_check(self._opponent_player)
        if not king_in_check:
            return False

        actual_last_move = self._last_move

        # Get the opponent's piece positions then loop through them
        opponent_piece_positions = list(self._piece_positions_dict[self._opponent_player])

        for opponent_position in opponent_piece_positions:

            row, col = opponent_position
            piece = self._board[row][col]

            # Get the available moves for the piece
            to_positions, remove_positions = self.get_available_moves(piece, row, col)

            for move in zip(to_positions, remove_positions):

                # Update the board for the available 'test' move
                self.update_board_positions(opponent_position, move, self._opponent_player)

                # Check if the king is in check
                king_in_check = self.check_for_check(self._opponent_player)

                # Revert the move since we were just testing
                self.revert_last_move()

                # If there is a single move which results in the king not being in check then it is not checkmate
                if not king_in_check:
                    self._last_move = actual_last_move
                    return False

        # If we've reached here then the opponent has no moves to 'un-check' themselves and is thus mated
        self._last_move = actual_last_move
        return True

    def add_queen_at_position(self, row: int, col: int, color: str) -> None:
        """Add a queen of the color passed at the position passed to the board list"""

        self._board[row][col] = Queen(color)


class ChessPiece:
    """
    Represents a chess piece in a game of chess.
    There are 6 distinct pieces: Pawn, Knight, Rook, Bishop, Queen and King
    """

    def __init__(self, color: str):
        self._color = color  # white or black
        self._visual = ''  # A placeholder for the letter which will represent a piece
        self._already_moved = False  # If the piece has already moved
        self._max_allowed_distance = 0  # How far a piece is allowed to go at most
        self._allowed_move_orientations = []

    def get_max_allowed_distance(self) -> int:
        """Return the max allowed distance"""

        return self._max_allowed_distance

    def get_allowed_moved_orientations(self) -> list:
        """Return the allowed movement orientations"""

        return self._allowed_move_orientations

    def get_already_moved(self) -> bool:
        """Return if the piece has already moved"""

        return self._already_moved

    def update_has_already_moved(self) -> None:
        """Update that the piece has already moved"""

        self._already_moved = True

    def get_visual(self) -> str:
        """Return the visual representation of the piece. White pieces are in uppercase and black are in lowercase"""

        if self._color == 'white':
            return self._visual.upper()
        else:
            return self._visual

    def get_color(self) -> str:
        """Get the color of the piece"""

        return self._color

    def get_class_name(self) -> str:
        """Get the name of the class"""

        return self.__class__.__name__

    def __str__(self):
        """Override the string dunder method to print a more visually friendly output"""

        return self._color + ' ' + self.__class__.__name__


class Pawn(ChessPiece):
    """Represents a chess pawn which can move forward and capture diagonally"""

    def __init__(self, color: str):
        super().__init__(color)
        self._max_allowed_distance = 2
        self._visual = 'p'

        if color == 'white':
            self._allowed_move_orientations = [[-1, 0]]
            self._end_row = 0
        else:
            self._allowed_move_orientations = [[1, 0]]
            self._end_row = 7

    def update_has_already_moved(self) -> None:
        """
        Overwrite the superclass method as there are different rules for pawns
        Once a pawn has moved, it can only move a maximum of one space for the rest of the game
        """

        self._max_allowed_distance = 1
        self._already_moved = True

    def get_end_row(self) -> int:
        """Get the 'end' row of the pawn. This is the row at the opposite side of the board"""

        return self._end_row


class Bishop(ChessPiece):
    """Represents a bishop which can move diagonally"""

    def __init__(self, color: str):
        super().__init__(color)
        self._visual = 'b'
        self._max_allowed_distance = 8
        self._allowed_move_orientations = [[1, 1], [1, -1], [-1, 1], [-1, -1]]


class Rook(ChessPiece):
    """Represents a rook which can move vertically and horizontally"""

    def __init__(self, color: str):
        super().__init__(color)
        self._visual = 'r'
        self._max_allowed_distance = 8
        self._allowed_move_orientations = [[1, 0], [0, 1], [-1, 0], [0, -1]]


class Knight(ChessPiece):
    """Represents a knight which can move in an L shape two spaces in one direction then one space in another direction"""

    def __init__(self, color: str):
        super().__init__(color)
        self._visual = 'h'
        self._max_allowed_distance = 2


class Queen(ChessPiece):
    """Represents a queen which can move vertically, horizontally or diagonally a maximum of eight spaces"""

    def __init__(self, color: str):
        super().__init__(color)
        self._visual = 'q'
        self._max_allowed_distance = 8
        self._allowed_move_orientations = [[1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [0, 1], [-1, 0], [0, -1]]


class King(ChessPiece):
    """Represents a king which can move vertically, horizontally or diagonally a maximum of one space"""

    def __init__(self, color: str):
        super().__init__(color)
        self._visual = 'k'
        self._max_allowed_distance = 1
        self._allowed_move_orientations = [[1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [0, 1], [-1, 0], [0, -1]]


def main():
    board = ChessVar()
    print('Make moves in the following format "a2a3"')

    while board.get_game_state() == 'UNFINISHED':
        board.print_board()
        turn = board._active_player
        print(f'{turn}, make your move')
        move = input()
        board.make_move(move[:2], move[2:])

    print(board.get_game_state())


if __name__ == '__main__':
    main()



