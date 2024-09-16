from ChessGame import ChessGame
import pygame
import time
from Parameters import square_size, outer_margin, board_size

pygame.init()

# Create a chess game
game = ChessGame()
chess_board = game.get_board_object()

width, height = board_size, board_size
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chess')

# Define board headers
header_font = pygame.font.Font(None, int(square_size/4))

number_list = ['8', '7', '6', '5', '4', '3', '2', '1']
letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# Define the board background colors
square_color_1 = pygame.Color(160, 84, 28)
square_color_2 = pygame.Color(216, 188, 152)
board_background = [[None]*8]*8

# White window
window_color = pygame.Color((255, 255, 255))
window.fill(window_color)


def get_square_color(top, left):

    return square_color_1 if (top - left) % 2 == 0 else square_color_2


def get_offset_position(index):

    return index * square_size + outer_margin


def draw_background():

    # Draw the board and load the background list
    for top in range(8): # top = row
        for left in range(8): # left = col

            if top == 0:  # Column headers
                header = header_font.render(letter_list[left], True, (0, 0, 0))
                window.blit(header, (left * square_size + outer_margin + (square_size / 2), outer_margin / 2))
            if left == 0:  # Row headers
                header = header_font.render(number_list[top], True, (0, 0, 0))
                window.blit(header, (outer_margin / 2, top * square_size + outer_margin + (square_size / 2)))

            top_offset = get_offset_position(top)
            left_offset = get_offset_position(left)

            square_color_choice = get_square_color(top, left)
            board_background[top][left] = square_color_choice

            rect = pygame.Rect((left_offset, top_offset, square_size, square_size))
            pygame.draw.rect(window, square_color_choice, rect)


def draw_sprites():
    all_chess_piece_sprites = game.get_piece_sprites()
    all_chess_piece_sprites.draw(window)


def draw_player_turn():
    # Draw player turn
    turn_surface = header_font.render('Turn: ' + game.get_active_player(), True, (0, 0, 0))
    turn_rect = pygame.Rect((board_size/2, board_size-(outer_margin/2)) + turn_surface.get_size())
    window.fill(window_color, turn_rect)
    window.blit(turn_surface, turn_rect)


draw_background()
draw_sprites()
draw_player_turn()

circle_color = (119, 136, 153)

moves = []
piece_clicked = False
game_active = True

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player left clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if not piece_clicked:
                active_player = game.get_active_player()
                for sprite in game.get_piece_sprites():
                    if sprite.rect.collidepoint(event.pos) and sprite.get_color() == active_player: # The players piece is clicked
                        piece_clicked = True
                        moves = sprite.get_available_moves()
                        for move in moves:
                            move_to = move.get_move_to()
                            raw_move_top, raw_move_left = move_to
                            move_left, move_top = get_offset_position(raw_move_left), get_offset_position(raw_move_top)

                            available_move_color = get_square_color(raw_move_top, raw_move_left)

                            # Draw small circles where there are available moves
                            circle_center = move_left+(square_size/2), move_top+(square_size/2)
                            pygame.draw.circle(window, circle_color, circle_center, square_size/18)

                        break

            # Check for move to position if a piece is clicked
            else:
                for move in moves:

                    move_to = move.get_move_to()
                    # Get the move rect on the pygame board
                    move_left, move_top = get_offset_position(move_to[1]), get_offset_position(move_to[0])
                    move_rect = pygame.Rect((move_left, move_top, square_size, square_size))

                    # Redraw the background where the available move circle is
                    background_square_color = get_square_color(*move_to)
                    pygame.draw.rect(window, background_square_color, move_rect)

                    draw_sprites()

                    if move_rect.collidepoint(event.pos):

                        # Convert the move into the string the game's make_move method takes
                        y, x = move_to
                        move_from_str = letter_list[sprite.get_position()[1]] + str(8-sprite.get_position()[0])
                        move_to_str = letter_list[x] + str(8-y)

                        # Make the move
                        game.make_move(move_from_str, move_to_str)

                        # Draw background, overlay the pieces then redraw the player turn
                        draw_background()
                        draw_sprites()
                        draw_player_turn()

                        if game.get_game_state() != 'UNFINISHED':
                            game_active = False

                        break

                # Unclick the piece so the player can click on other pieces and get their available moves
                piece_clicked = False

    # Draw/Render the screen
    pygame.display.flip()

    # When the game is over, add 'GAME OVER' to the screen for 3 seconds the close window
    if not game_active:
        end_game_font = pygame.font.Font(None, square_size)
        end_game_surface = end_game_font.render('GAME OVER', True, (0, 0, 0))
        end_game_rect = pygame.Rect((board_size / 4, board_size / 2) + end_game_surface.get_size())
        window.fill(window_color, end_game_rect)
        window.blit(end_game_surface, end_game_rect)
        pygame.display.update(end_game_rect)
        time.sleep(3)
        break

# Quit Pygame when the game loop is exited
pygame.quit()



