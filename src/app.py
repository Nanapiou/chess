"""
The pygame app of the chess game
"""
import pygame
import os
from src.util import pieces_ids, position_to_coords, coords_to_position, evaluate_position
from src.moves import get_all_legal_moves, make_move, get_black_checks, get_white_checks, simulate_move
from typing import List, Dict, Tuple

Board = List[List[int]]
Position = Tuple[int, int]
GameData = Dict[str, Board | int | str | Position | Dict[str, bool]]


class App:
    """
    The pygame app.
    """

    def __init__(self, screen: pygame.Surface, game_data):
        # Set the screen
        self.screen = screen
        self.width, self.height = screen.get_width(), screen.get_height()
        self.tile_width, self.tile_height = self.width // 8, self.height // 8

        # Set the clock
        self.clock = pygame.time.Clock()

        # Set the title
        self.title = "Chess"
        pygame.display.set_caption(self.title)

        # Set the running flag to True
        self.running = True

        # Set a semi-transparent point, to use it in update()
        self.point = pygame.Surface((self.tile_width, self.tile_height), pygame.SRCALPHA)
        pygame.draw.circle(self.point, (0, 0, 0, 100), (self.tile_width / 2, self.tile_height / 2), self.tile_width / 5)

        self.board = game_data['board']
        self.en_passant = game_data['en_passant']
        self.turn = game_data['turn']  # 0 for white, 1 for black
        self.castles = game_data['castles']

        self.all_legal_moves = get_all_legal_moves(self.board, self.turn, self.en_passant, self.castles)
        self.legal_moves, self.selected_piece = [], None

        self.assets = {}
        for file in os.scandir('./assets/white'):
            self.assets[pieces_ids[file.name[0]]] = pygame.transform.scale(
                pygame.image.load(f'./assets/white/{file.name}'), (self.width / 8, self.height / 8))
        for file in os.scandir('./assets/black'):
            self.assets[pieces_ids[file.name[0]]] = pygame.transform.scale(
                pygame.image.load(f'./assets/black/{file.name}'), (self.width / 8, self.height / 8))

    def run(self):
        """
        Run the app

        :return:
        """
        while self.running:
            # Handling events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.on_click(event)

            # Update
            self.update()

            # Limit the frame rate to n FPS
            self.clock.tick(40)

    def update(self):
        """
        Update the screen

        :return:
        """
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(self.screen, (238, 238, 210) if (i + j) % 2 == 0 else (118, 150, 86),
                                 pygame.Rect(self.tile_width * i, self.tile_height * j, self.tile_width,
                                             self.tile_height))
                if self.board[j][i] is not None:
                    self.screen.blit(self.assets[self.board[j][i]], (i * self.tile_width, j * self.tile_height))
                if (j, i) in self.legal_moves:
                    self.screen.blit(self.point, ( i * self.tile_width , j * self.tile_height))
        pygame.display.update()

    def on_click(self, event: pygame.event.Event):
        """
        On click event

        :param event:
        :return:
        """
        x, y = pygame.mouse.get_pos()
        j, i = x // self.tile_width, y // self.tile_height
        coords = position_to_coords((i, j))
        if coords in self.all_legal_moves:
            self.legal_moves = self.all_legal_moves[coords]
            self.selected_piece = (i, j)
        elif (i, j) in self.legal_moves:
            self.player_play(self.selected_piece, (i, j))
            self.legal_moves, self.selected_piece = [], None
        else:
            self.legal_moves = []
            self.selected_piece = None

    def player_play(self, pos1, pos2):
        """
        Assuming that the move can be done

        :param pos1:
        :param pos2:
        :return:
        """
        if self.play_move(pos1, pos2):
            self.bot_play()

    def bot_play(self):
        """
        A bot play a turn!

        :return:
        """
        pos1, pos2 = None, None
        best_eval = None
        for key in self.all_legal_moves:
            piece_pos = coords_to_position(key)
            for move in self.all_legal_moves[key]:
                current_eval = evaluate_position(simulate_move(self.board, piece_pos, move))
                if best_eval is None:
                    best_eval = current_eval
                    pos1, pos2 = piece_pos, move
                else:
                    if self.turn == 0:
                        if best_eval < current_eval:
                            best_eval = current_eval
                            pos1, pos2 = piece_pos, move
                    else:
                        if best_eval > current_eval:
                            best_eval = current_eval
                            pos1, pos2 = piece_pos, move

        self.play_move(pos1, pos2)

    def play_move(self, pos1, pos2):
        """
        Play a move, check castles, en-passant, checkmates
        Returns True if the game continues

        :return:
        """
        piece = self.board[pos1[0]][pos1[1]]
        make_move(self.board, pos1, pos2)

        # Checking castles
        if (0, 0) == pos1 or (0, 0) == pos2:
            self.castles['q'] = False
        if (0, 7) == pos1 or (0, 7) == pos2:
            self.castles['k'] = False
        if (7, 0) == pos1 or (7, 0) == pos2:
            self.castles['Q'] = False
        if (7, 7) == pos1 or (7, 7) == pos2:
            self.castles['K'] = False
        if (0, 4) == pos1:
            self.castles['q'], self.castles['k'] = False, False
        if (7, 4) == pos1:
            self.castles['Q'], self.castles['K'] = False, False

        # Checking en-passant
        self.en_passant = None
        if piece == 1:
            if pos1[0] == 6 and pos2[0] == 4:
                self.en_passant = (5, pos1[1])
        if piece == 7:
            if pos1[0] == 1 and pos2[0] == 3:
                self.en_passant = (2, pos1[1])

        self.turn = 1 - self.turn
        self.all_legal_moves = get_all_legal_moves(self.board, self.turn, self.en_passant, self.castles)
        if len(self.all_legal_moves) == 0:
            self.running = False
            if len(get_black_checks(self.board) if self.turn == 0 else get_white_checks(self.board)):
                print(f'{"White" if self.turn == 1 else "Black"} won by checkmate!')
            else:
                print("Stalemate!")
            return False
        return True
