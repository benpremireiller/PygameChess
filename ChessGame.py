import re
import pygame
from Parameters import square_size, outer_margin


class ChessMove:
    """
    Represents a chess move.
    """

    def __init__(self, color, type, move_piece, remove_piece, move_from, move_to, remove_from):
        """
        :param color: The color of the player moving
        :param type: The type of move (move, capture, castle-queen-side, castle-king-side, en-passant)
        :param move_piece: The piece that is moving
        :param remove_piece: The piece that is being removed. None if the move doesn't result in a capture.
        :param move_from: The origin coordinates of the moving piece
        :param move_to: The destination coordinates of the moving piece
        :param remove_from: The coordinates of the piece being removed. None if move is not capture.
        """

        self.color = color
        self.type = type
        self.move_piece = move_piece
        self.remove_piece = remove_piece
        self.move_from = move_from
        self.move_to = move_to
        self.remove_from = remove_from

    def get_color(self):
        """Return the color of the moving piece"""

        return self.color

    def get_type(self):
        """Return the move type"""

        return self.type

    def get_move_piece(self):
        """Return the moving piece object"""

        return self.move_piece

    def get_remove_piece(self):
        """Return the remove piece object. Will be none if move is not a capture"""

        return self.remove_piece

    def get_move_from(self):
        """Return the move from position"""

        return self.move_from

    def get_move_to(self):
        """Return the move to position"""

        return self.move_to

    def get_remove_from(self):
        """Return the remove from position. Will be none if move is not a capture"""

        return self.remove_from

    def get_move(self) -> tuple:
        """Return the move data as a tuple"""

        return self.color, self.type, self.move_piece, self.remove_piece, self.move_from, self.move_to, self.remove_from


class ChessBoard:
    """
    Represents a chess board

    Change the self._chess_board data member to the test_board for testing purposes
    """

    def __init__(self, game):

        # Define the boards
        main_board = [
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
            [Rook('black'), Knight('black'), Bishop('black'), None, King('black'), None, None, None],
            [None, Pawn('black'), None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, Queen('black'), None, None, None, None, None],
            [Pawn('black'), None, None, None, None, None, None, None],
            [None, Pawn('white'), None, None, None, Pawn('black'), None, None],
            [Pawn('white'), Pawn('white'), None, None, None, None, None, None],
            [King('white'), Knight('white'), None, None, None, None, None, None]
        ]

        self._game = game
        self._chess_board = main_board
        self._column_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}  # Map col letters to list indices

    def get_board(self):
        """Return the chess board"""

        return self._chess_board

    def get_cell_at_position(self, position):
        """Return the cell at the position passed as an argument"""

        row, col = position
        return self._chess_board[row][col]

    def get_column_map(self):
        """Return the column map"""

        return self._column_map

    def get_piece_positions(self, color: str, piece_name=None) -> list:
        """
        Return the positions of the pieces for the passed color
        Can also specify a piece name to only return pieces which match the name
        """

        positions = []

        for i, row in enumerate(self._chess_board):
            for j, cell in enumerate(row):
                if cell is not None and cell.get_color() == color and (piece_name is None or cell.get_class_name() == piece_name):
                    positions.append((i, j))

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
        Prints the board with row and column headers to the console
        """

        # Print columns first
        print('  ', end='')  # Need a spot for the row header
        for letter in self._column_map:
            print(letter, end=' ')
        print()  # New line

        # Print the row header then the rows
        for i, row in enumerate(self._chess_board):
            print(8 - i, end=' ')  # Row header
            for cell in row:
                if cell is None:
                    print(' ', end=' ')
                else:
                    print(cell.get_visual(), end=' ')
            print()

    def add_piece_at_position(self, piece, position) -> None:
        """Add a piece at the passed position"""

        row, col = position

        self._chess_board[row][col] = piece
        piece.update_position((row, col))

    def update_board_positions(self, move_object: ChessMove) -> None:
        """
        Update the position of a piece on the board based on the passed move object.
        """
        
        color, move_type, moving_piece, remove_piece, from_position, to_position, remove_position = move_object.get_move()

        # Get the moving coordinates
        from_row, from_col = from_position
        to_row, to_col = to_position

        # Move the piece to the new position
        self._chess_board[from_row][from_col] = None
        self._chess_board[to_row][to_col] = moving_piece
        moving_piece.update_position(to_position)

        # Apply logic based on move type
        if move_type == 'queen':  # Pawn has reached the end
            queen = Queen(color)
            queen.set_game(self._game)
            self.add_piece_at_position(queen, to_position)

        elif move_type == 'move':
            return # Nothing else to do

        elif move_type == 'capture':
            # remove_piece.update_position(None)
            return # Nothing to do as we've already 'replaced' the piece from the board

        elif move_type == 'en-passant': # Need to remove a piece
            remove_row, remove_col = remove_position
            self._chess_board[remove_row][remove_col] = None
            # remove_piece.update_position(None)

        elif move_type.startswith('castle'):

            # Get the direction the king is moving
            orientation = -1 if move_type == 'castle-queen-side' else 1
            rook_col = 0 if move_type == 'castle-queen-side' else 7

            # Form the rook move
            rook_from_position = (from_row, rook_col)
            rook_to_position = (from_row, to_col - orientation)  # Right before or after the king col
            rook_piece = self.get_cell_at_position(rook_from_position)
            rook_move = ChessMove(color, 'move', rook_piece, None, rook_from_position, rook_to_position, None)

            # Recurse this method to move the rook
            self.update_board_positions(rook_move)


class ChessPiece(pygame.sprite.Sprite):
    """
    Represents a chess piece in a game of chess.
    There are 6 distinct pieces: Pawn, Knight, Rook, Bishop, Queen and King
    """

    def __init__(self, color: str):

        super().__init__()
        self._game = None # This will hold the game ChessGame object
        self._color = color  # white or black
        self._visual = ''  # A placeholder for the letter which will represent a piece (for printing the board to the console)
        self._already_moved = False  # If the piece has already moved
        self._max_allowed_distance = 0  # How far a piece is allowed to go at most
        self._allowed_move_orientations = [] # Which directions the piece is allowed to move
        self._position = (None, None)  # Position on the board (row, col)
        self.image = None # The image which represents the piece
        self.rect = pygame.Rect((0, 0, square_size, square_size)) # The pygame rect object used to represent the piece

    def set_game(self, game):
        """Set the game variable. Should only be called once at the beginning of the game init."""

        self._game = game

    def update_position(self, position: tuple) -> None:
        """Update the position variable"""

        self._position = position

        y, x = self._position
        self.rect.y = y * square_size + outer_margin
        self.rect.x = x * square_size + outer_margin
        
    def move_results_in_check(self, move) -> bool:
        """Return if a potential valid move will result in check for the player"""

        game = self._game
        board = game.get_board_object()

        # Make the move, check for check then revert the move
        board.update_board_positions(move)
        game.add_move(move)
        check_player_is_in_check = game.check_player_is_in_check(self._color)
        game.revert_last_move()

        return check_player_is_in_check

    def get_available_moves(self, check_for_checks=True) -> list:
        """
        Get the available moves for a particular piece on the board.
        This method will fetch the available moves for this piece based on its allowed movement rules.

        Returns a list of ChessMoves.

        The default rules for a piece are that it can move in straight lines.
        """

        moves = []
        board = self._game.get_board_object()
        from_row, from_col = self._position

        for orientation in self._allowed_move_orientations:

            vertical_direction, horizontal_direction = orientation

            # Get the first position that will be checked for legality
            position_offset = (from_row + vertical_direction, from_col + horizontal_direction)
            position_offset_on_board = board.position_is_on_board(position_offset)
            dist = 1

            # Loop until we reach the pieces max allowed distance or the position is not on the board anymore
            while dist <= self._max_allowed_distance and position_offset_on_board:

                cell_at_position = board.get_cell_at_position(position_offset)

                cell_is_players_piece = cell_at_position is not None and cell_at_position.get_color() == self._color
                if cell_is_players_piece:
                    break  # Stop looping as we've hit a 'wall'

                cell_is_opponent_piece = cell_at_position is not None and cell_at_position.get_color() != self._color
                if cell_is_opponent_piece:
                    move = ChessMove(self._color, 'capture', self, cell_at_position, self._position, position_offset, position_offset)
                    
                    # Make sure the move doesn't result in check (if we are checking check)
                    if check_for_checks:
                        if not self.move_results_in_check(move):
                            moves.append(move)
                    else:
                        moves.append(move)
                        
                    break  # Hit a wall again (that we can capture)

                # If we've reached here, the cell is empty
                move = ChessMove(self._color, 'move', self, None, self._position, position_offset, None)
                if check_for_checks:
                    if not self.move_results_in_check(move):
                        moves.append(move)
                else:
                    moves.append(move)

                dist += 1

                # Advance the position offset by one cell in the direction we are checking
                position_offset = (from_row + (vertical_direction * dist), from_col + (horizontal_direction * dist))
                position_offset_on_board = board.position_is_on_board(position_offset)

        return moves

    def get_already_moved(self) -> bool:
        """Return if the piece has already moved"""

        return self._already_moved

    def get_position(self) -> tuple:
        """Return the pieces current position"""

        return self._position

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

    def get_image(self) -> pygame.image:
        """Return the pygame image"""

        return self.image

    def get_class_name(self) -> str:
        """Get the name of the class"""

        return self.__class__.__name__

    def __str__(self):
        """Override the string dunder method to print a user-friendly output"""

        return self._color + ' ' + self.__class__.__name__ + ' id: ' + str(id(self))


class Pawn(ChessPiece):
    """Represents a chess pawn"""

    def __init__(self, color: str):
        super().__init__(color)
        self._max_allowed_distance = 2
        self._visual = 'p'
        self.image = pygame.transform.scale(pygame.image.load('Assets/chess_sprites/' + color + '_pawn.png'), (square_size, square_size))

        if color == 'white':
            self._allowed_move_orientations = [[-1, 0]]
            self._end_row = 0
        else:
            self._allowed_move_orientations = [[1, 0]]
            self._end_row = 7

    def get_available_moves(self, check_for_checks=True) -> list:
        """
        Pawns move differently than the 'default' chess piece. They move forward and capture diagonally.
        They are also able to perform en passant moves.
        """

        moves = []
        board = self._game.get_board_object()

        vert_direct = self._allowed_move_orientations[0][0]  # The vertical direction (1 or -1)
        from_row, from_col = self._position

        ## Get regular moves
        dist = 1
        move_type = 'move'
        while dist <= self._max_allowed_distance:
            forward_row = from_row + (dist * vert_direct)
            forward_position = (forward_row, from_col)
            forward_cell = board.get_cell_at_position(forward_position)

            if forward_cell is not None:
                break # Stop if there is a piece in front
            else:
                if self.get_end_row() == forward_row: # Check if move reaches opponent end
                    move_type = 'queen'

                move = ChessMove(self._color, move_type, self, None, self._position, forward_position, None) # There is a move
                if check_for_checks:
                    if not self.move_results_in_check(move):
                        moves.append(move)
                else:
                    moves.append(move)
            dist += 1

        # Get captures
        move_type = 'capture'
        for diag_direct in [1, -1]:  # Right then left

            # Check if capture position has an opponent piece
            forward_diagonal_position = (from_row + vert_direct, from_col + diag_direct)
            if board.position_is_on_board(forward_diagonal_position):

                cell_at_position = board.get_cell_at_position(forward_diagonal_position)
                forward_cell_is_opponent = cell_at_position is not None and cell_at_position.get_color() != self._color

                if forward_cell_is_opponent:
                    if self.get_end_row() == (from_row + vert_direct): # Check if move reaches opponent end
                        move_type = 'queen'

                    move = ChessMove(self._color, move_type, self, cell_at_position, self._position, forward_diagonal_position, forward_diagonal_position)
                    if check_for_checks:
                        if not self.move_results_in_check(move):
                            moves.append(move)
                    else:
                        moves.append(move)

        ## Get en passant moves
        move_type = 'en-passant'
        current_game_move_number = self._game.get_current_move_number()

        # If a move hasn't been made yet no en passant so return
        if current_game_move_number == 1:
            return moves

        last_move_object = self._game.get_last_move_object()
        last_moving_piece = last_move_object.get_move_piece()
        last_move_from = last_move_object.get_move_from()
        last_move_to = last_move_object.get_move_to()

        # If the piece that last moved isn't a pawn no en passant
        if not isinstance(last_moving_piece, Pawn):
            return moves

        last_to_row, last_to_col = last_move_to
        last_from_row, last_from_col = last_move_from
        vertical_distance_moved_is_two = abs(last_from_row - last_to_row) == 2
        pawn_is_adjacent = last_to_row == from_row and abs(last_to_col - from_col) == 1

        # If the pawn that last moved, moved two spaces and is adjacent to this pawn, it is a valid en passant
        if vertical_distance_moved_is_two and pawn_is_adjacent:
            move_coordinate = (from_row + vert_direct, last_to_col)
            move = ChessMove(self._color, move_type, self, last_moving_piece, self._position, move_coordinate, last_move_to)
            if check_for_checks:
                if not self.move_results_in_check(move):
                    moves.append(move)
            else:
                moves.append(move)

        return moves

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
        self.image = pygame.transform.scale(pygame.image.load('Assets/chess_sprites/' + color + '_bishop.png'), (square_size, square_size))


class Rook(ChessPiece):
    """Represents a rook which can move vertically and horizontally"""

    def __init__(self, color: str):
        super().__init__(color)
        self._visual = 'r'
        self._max_allowed_distance = 8
        self._allowed_move_orientations = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        self.image = pygame.transform.scale(pygame.image.load('Assets/chess_sprites/' + color + '_rook.png'), (square_size, square_size))


class Knight(ChessPiece):
    """Represents a knight which can move in an L shape two spaces in one direction then one space in another direction"""

    def __init__(self, color: str):
        super().__init__(color)
        self._visual = 'h'
        self.image = pygame.image.load('Assets/chess_sprites/' + color + '_knight.png')

    def get_available_moves(self, check_for_checks=True) -> list:
        """Knights move differently than the 'default' piece. They move in an L shape"""

        moves = []
        board = self._game.get_board_object()
        from_row, from_col = self._position

        def add_knight_move(position_to_check: tuple) -> None:
            """Add valid moves based on what is present at the position_to_check"""

            # Make sure the position is a valid one (since we are checking all L offsets)
            position_on_board = board.position_is_on_board(position_to_check)

            if position_on_board:

                # Get the cell. If opponent, add a capture move, if empty add regular move.
                cell_at_position = board.get_cell_at_position(position_to_check)
                position_is_opponent = cell_at_position is not None and cell_at_position.get_color() != self._color
                position_is_empty = cell_at_position is None

                if position_is_opponent:  # A capture
                    move = ChessMove(self._color, 'capture', self, cell_at_position, self._position, position_to_check, position_to_check)
                    if check_for_checks:
                        if not self.move_results_in_check(move):
                            moves.append(move)
                    else:
                        moves.append(move)
                elif position_is_empty:  # A move
                    move = ChessMove(self._color, 'move', self, None, self._position, position_to_check, None)
                    if check_for_checks:
                        if not self.move_results_in_check(move):
                            moves.append(move)
                    else:
                        moves.append(move)

        # Loop through all possible sets of moves for knights
        for i in [1, -1]:
            for j in [2, -2]:
                # First check for moves that move one cell vertically then two cells horizontally
                add_knight_move((from_row + i, from_col + j))

                # Next check for moves that move two cells vertically then one cell horizontally
                add_knight_move((from_row + j, from_col + i))

        return moves


class Queen(ChessPiece):
    """Represents a queen which can move vertically, horizontally or diagonally a maximum of eight spaces"""

    def __init__(self, color: str):
        super().__init__(color)
        self._visual = 'q'
        self._max_allowed_distance = 8
        self._allowed_move_orientations = [[1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [0, 1], [-1, 0], [0, -1]]
        self.image = pygame.transform.scale(pygame.image.load('Assets/chess_sprites/' + color + '_queen.png'), (square_size, square_size))


class King(ChessPiece):
    """Represents a king which can move vertically, horizontally or diagonally a maximum of one space"""

    def __init__(self, color: str):
        super().__init__(color)
        self._visual = 'k'
        self._max_allowed_distance = 1
        self._allowed_move_orientations = [[1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [0, 1], [-1, 0], [0, -1]]
        self.image = pygame.transform.scale(pygame.image.load('Assets/chess_sprites/' + color + '_king.png'), (square_size, square_size))

    def get_available_moves(self, check_for_checks=True) -> list:
        """Kings have the same move set as the 'standard' piece but can also castle"""

        board = self._game.get_board_object()
        from_row, from_col = self._position

        # Use the logic for the standard piece
        moves = super().get_available_moves(check_for_checks)

        # Check if the king has already moved
        if not self._already_moved:

            # If not, add castling
            rook_positions = board.get_piece_positions(self._color, 'Rook')

            # Check if the rook can castle
            for rook_position in rook_positions:

                rook_piece = board.get_cell_at_position(rook_position)

                # If the rook has already moved, castling in not legal
                if rook_piece.get_already_moved():
                    continue

                rook_row, rook_col = rook_position
                col_difference = rook_col - from_col

                # Get orientation to determine queen side or king side castling
                orientation = (col_difference > 0) - (col_difference < 0)
                castle_type = 'queen-side' if orientation == -1 else 'king-side'

                # Check if the path is clear between the king and rook
                path_is_clear = True
                offset = 1
                while offset < abs(col_difference):
                    offset_position = (from_row, from_col + (offset * orientation))
                    cell = board.get_cell_at_position(offset_position)
                    if cell is not None:
                        path_is_clear = False
                        break
                    offset += 1

                # If the path is clear, the king hasn't moved and the rook hasn't moved, castling is legal
                if path_is_clear:
                    king_move_to_position = (from_row, from_col + ((offset - 1) * orientation))
                    move_type = 'castle-' + castle_type
                    move = ChessMove(self._color, move_type, self, None, self._position, king_move_to_position, None)
                    if check_for_checks:
                        if not self.move_results_in_check(move):
                            moves.append(move)
                    else:
                        moves.append(move)

        return moves


class ChessGame:
    """
    Represents a game of chess:
    The game is over once a king is put into check mate.

    This class serves as the main controller for the game.
    Use the make_move() method to alter the state of the board
    """

    def __init__(self):

        self._board = ChessBoard(self)
        self._piece_sprites = pygame.sprite.Group()
        self._initialize_piece_data()        # Update the piece objects
        self._colors = {'white', 'black'}
        self._active_player = 'white'       # White starts
        self._opponent_player = 'black'
        self._current_move_number = 1              # The current move we are on
        self._moves = []                    # Store the game moves
        self._game_state = 'UNFINISHED'     

    def _initialize_piece_data(self):
        """Add the game reference and positions to the piece objects. Also add the piece to the sprite group."""

        for i, row in enumerate(self._board.get_board()):
            for j, cell in enumerate(row):
                if cell is not None: # A piece
                    cell.set_game(self)
                    cell.update_position((i, j))
                    self._piece_sprites.add(cell)
    
    def add_move(self, move_object):
        """Add a move to the move list"""

        self._moves.append(move_object)
        
    def get_last_move_object(self):
        """Return the last move"""

        return self._moves[len(self._moves)-1]

    def get_current_move_number(self):
        """Return the current move number"""

        return self._current_move_number

    def update_piece_sprites(self, move_object):
        """Update the sprite group based on the move"""

        move_type = move_object.get_type()
        move_to = move_object.get_move_to()
        remove_piece = move_object.get_remove_piece()
        move_piece = move_object.get_move_piece()

        if move_type == 'capture':
            self._piece_sprites.remove(remove_piece)

        elif move_type == 'queen':
            self._piece_sprites.remove(move_piece)
            queen_piece = self._board.get_cell_at_position(move_to)
            self._piece_sprites.add(queen_piece)

    def get_opponent_color(self, color):
        """
        Return the 'other' color
        If the color argument is 'black', return 'white'
        If the color argument is 'white', return 'black'
        """

        return list(self._colors - {color})[0]  # Set difference operation

    def get_piece_sprites(self):
        """Return the list of piece sprites"""

        return self._piece_sprites
        
    def get_game_state(self):
        """Return the game state"""

        return self._game_state
    
    def get_board_object(self):
        """Return the ChessBoard object"""

        return self._board

    def get_active_player(self):
        """Return the active player"""

        return self._active_player

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

        row_index = 8 - int(move[1])  # 8 minus because the board is reversed
        col_index = self._board.get_column_map()[move[0].lower()]

        return row_index, col_index,

    def make_move(self, move_from: str, move_to: str, numeric=False) -> bool:
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
        from_position = self.decode_player_input(move_from)
        to_position = self.decode_player_input(move_to)

        # Get the cells at the coordinates
        from_cell = self._board.get_cell_at_position(from_position)

        if from_cell is None:  # No piece
            print('No piece at position entered')
            return False

        if from_cell.get_color() != self._active_player:  # Piece is not the players
            print('Piece does not belong to you')
            return False

        # Check if the move is in the set of available moves for the piece
        moves = from_cell.get_available_moves()

        # Also get the move object associated with the player move
        valid = False
        for move in moves:
            if to_position == move.get_move_to():
                valid_move = move
                valid = True

        if not valid:
            print('Invalid move')
            return False

        # Update board positions as move is valid
        self._board.update_board_positions(valid_move)
        self.add_move(valid_move)
        self._current_move_number += 1

        # Update sprites object
        self.update_piece_sprites(valid_move)

        # Update that the piece has already moved
        from_cell.update_has_already_moved()

        # Check if there is a checkmate and end game if so
        is_check_mate = self.check_player_is_mated()

        if is_check_mate:
            print('Check mate!')
            self.end_game()
            return True

        # Update player turns
        self._active_player, self._opponent_player = self._opponent_player, self._active_player

    def revert_last_move(self) -> None:
        """Revert the board list and move list to their state right before the last move that occurred"""

        move_object = self.get_last_move_object()
        color, move_type, moving_piece, remove_piece, from_position, to_position, remove_position = move_object.get_move()

        # Invert the move and send it to update_board_positions
        reversion_move = ChessMove(color, 'move', moving_piece, None, to_position, from_position, None)
        self._board.update_board_positions(reversion_move)

        # Move rook back if castle move
        if move_type.startswith('castle'):

            rook_col = 2 if move_type == 'castle-queen-side' else 5
            rook_old_col = 0 if move_type == 'castle-queen-side' else 7
            move_row, _ = from_position
            rook_position = (move_row, rook_col)
            rook_piece = self._board.get_cell_at_position(rook_position)
            rook_old_position = (move_row, rook_old_col)
            reversion_rook_move = ChessMove(color, 'move', rook_piece, None, rook_position, rook_old_position, None)
            self._board.update_board_positions(reversion_rook_move)

        # If the move resulted in a capture, add the piece back
        if remove_piece:
            self._board.add_piece_at_position(remove_piece, remove_position)

        self._moves.pop()

    def check_player_is_in_check(self, color: str) -> bool:
        """Return if the kings position is in the set of available moves of the opponent's pieces"""

        # Get the 'color' player
        try:
            players_king_position, = self._board.get_piece_positions(color, 'King')  # Only one value will be returned so unpack
        except:
            raise('Error: No king or multiple kings for one color on board')

        # Create a set we will fill with the opponents moves
        opponent_color = self.get_opponent_color(color)
        opponent_piece_positions = self._board.get_piece_positions(opponent_color)

        # Get the distinct set of moves that the opponent pieces can make
        for opponent_position in opponent_piece_positions:

            piece = self._board.get_cell_at_position(opponent_position)
            moves = piece.get_available_moves(check_for_checks=False)

            for move in moves:
                to_position = move.get_move_to()

                # If the players king position is in the set of available moves for any opponent piece, the king is in check
                if players_king_position == to_position:
                    return True

        # If we've reached here, the opponent does not have a move at the active player's king position
        return False

    def check_player_is_mated(self) -> bool:
        """
        Returns true if the opponent (non-active) player is mated and false otherwise
        This method checks if a move that the opponents pieces can make results in the king still being in check

        The opponent could move their king, capture a piece that has the king in check or move a piece in front of
        a piece that has the king in check. This method checks every possible move for simplicity.
        """

        # Check if the non-active player's (opponent) king is currently in check
        king_in_check = self.check_player_is_in_check(self._opponent_player)

        if not king_in_check:
            return False

        # Get the opponent's piece positions then loop through them
        opponent_piece_positions = list(self._board.get_piece_positions(self._opponent_player)) # Copy

        for opponent_position in opponent_piece_positions:

            piece = self._board.get_cell_at_position(opponent_position)

            # Get the available moves for the piece taking into account if the king remains in check
            moves = piece.get_available_moves(check_for_checks=True)

            # If there are any moves which result in the king not being in check then no mate
            if moves:
                return False

        return True


def main():
    game = ChessGame()
    print('Make moves in the following format "a2a3"')

    while game.get_game_state() == 'UNFINISHED':
        game.get_board_object().print_board()
        turn = game.get_active_player()
        print(f'{turn}, make your move')
        move = input()
        game.make_move(move[:2], move[2:])

    print(game.get_game_state())


if __name__ == '__main__':
    main()



