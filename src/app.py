"""
The pygame app of the chess game
"""
import pygame
import os
from time import sleep
from src.util import pieces_ids
from src.moves import get_all_legal_moves, make_move_smooth, get_black_checks, get_white_checks
from src.bot import create_decision_tree, minimax, minimax_root
from typing import List, Dict, Tuple

Board = List[List[int]]
Position = Tuple[int, int]
GameData = Dict[str, Board | int | str | Position | Dict[str, bool]]


class App:
    """
    The pygame app.
    """

    def __init__(self, screen: pygame.Surface, game_data, **kwargs):
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
        self.hand_grab_cursor = pygame.cursors.load_xbm('./assets/cursor-hand-grab.xbm', './assets/cursor-hand-grab.xbm')

        self.board = game_data['board']
        self.en_passant = game_data['en_passant']
        self.turn = game_data['turn']  # 0 for white, 1 for black
        self.castles = game_data['castles']

        self.all_legal_moves = get_all_legal_moves(self.board, self.turn, self.en_passant, self.castles)
        self.legal_moves, self.selected_piece, self.drag_piece = [], None, False

        self.assets = {}
        for file in os.scandir('./assets/white'):
            self.assets[pieces_ids[file.name[0]]] = pygame.transform.scale(
                pygame.image.load(f'./assets/white/{file.name}'), (self.width / 8, self.height / 8))
        for file in os.scandir('./assets/black'):
            self.assets[pieces_ids[file.name[0]]] = pygame.transform.scale(
                pygame.image.load(f'./assets/black/{file.name}'), (self.width / 8, self.height / 8))
        self.update()

        self.players_bot = [False, False]
        if 'white' in kwargs:
            if kwargs['white'] == 'bot':
                self.players_bot[0] = True
        if 'black' in kwargs:
            if kwargs['black'] == 'bot':
                self.players_bot[1] = True

        if self.players_bot[self.turn]:
            self.bot_play()

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    j, i = x // self.tile_width, y // self.tile_height
                    if self.players_bot[self.turn] or self.selected_piece == self.board[i][j]:
                        continue
                    if (i, j) in self.all_legal_moves:
                        self.selected_piece = (i, j)
                        self.legal_moves = self.all_legal_moves[(i, j)]
                        self.drag_piece = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.players_bot[self.turn]:
                        continue
                    if self.selected_piece is not None:
                        x, y = pygame.mouse.get_pos()
                        j, i = x // self.tile_width, y // self.tile_height
                        if (i, j) == self.selected_piece:
                            self.drag_piece = False
                            continue
                        if (i, j) in self.legal_moves:
                            selected = self.selected_piece
                            self.legal_moves, self.selected_piece, self.drag_piece = [], None, False
                            self.player_play(selected, (i, j))
                        else:
                            self.legal_moves, self.selected_piece, self.drag_piece = [], None, False

            # Update
            self.update()

            # Limit the frame rate to n FPS
            self.clock.tick(40)

    def update(self):
        """
        Update the screen

        :return:
        """
        x, y = pygame.mouse.get_pos()
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(self.screen, (238, 238, 210) if (i + j) % 2 == 0 else (118, 150, 86),
                                 pygame.Rect(self.tile_width * i, self.tile_height * j, self.tile_width,
                                             self.tile_height))
                if self.board[j][i] is not None and not (self.drag_piece and (j, i) == self.selected_piece):
                    self.screen.blit(self.assets[self.board[j][i]], (i * self.tile_width, j * self.tile_height))
                if (j, i) in self.legal_moves:
                    self.screen.blit(self.point, (i * self.tile_width, j * self.tile_height))
        if self.drag_piece:
            pygame.mouse.set_cursor(*self.hand_grab_cursor)
            self.screen.blit(self.assets[self.board[self.selected_piece[0]][self.selected_piece[1]]], (x - self.tile_width / 2, y - self.tile_height / 2))
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.display.update()

    def on_click(self, event: pygame.event.Event):
        """
        On click event

        :param event:
        :return:
        """
        if self.players_bot[self.turn]:
            return
        x, y = pygame.mouse.get_pos()
        j, i = x // self.tile_width, y // self.tile_height
        if (i, j) in self.all_legal_moves:
            self.legal_moves = self.all_legal_moves[(i, j)]
            self.selected_piece = (i, j)
        elif (i, j) in self.legal_moves:
            selected = self.selected_piece
            self.legal_moves, self.selected_piece = [], None
            self.player_play(selected, (i, j))
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
            if self.players_bot[self.turn]:
                self.bot_play()

    def bot_play(self):
        """
        A bot play a turn!

        :return:
        """
        pos1, pos2 = minimax_root({
            "board": self.board,
            "castles": self.castles,
            "en_passant": self.en_passant,
            "turn": self.turn
        }, 4)

        if self.play_move(pos1, pos2):
            if self.players_bot[self.turn]:
                self.bot_play()

    def play_move(self, pos1, pos2):
        """
        Play a move, check castles, en-passant, checkmates
        Returns True if the game continues

        :return:
        """
        data = make_move_smooth(self.board, pos1, pos2, self.en_passant, self.castles)
        self.castles = data['castles']
        self.en_passant = data['en_passant']

        self.turn = 1 - self.turn
        self.all_legal_moves = get_all_legal_moves(self.board, self.turn, self.en_passant, self.castles)
        self.update()
        if len(self.all_legal_moves) == 0:
            if len(get_black_checks(self.board) if self.turn == 0 else get_white_checks(self.board)):
                print(f'{"White" if self.turn == 1 else "Black"} won by checkmate!')
            else:
                print("Stalemate!")
            sleep(5)
            self.running = False
            return False
        return True
