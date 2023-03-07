# !/usr/bin/env python3
"""
A chess game written in Python.
"""
from typing import List, Dict, Tuple
from src.util import draw_board, load_fen, coords_to_position, position_to_coords, input_valid_coords
from src.moves import get_all_legal_moves, make_move, get_white_checks, get_black_checks

Board = List[List[int]]
Position = Tuple[int, int]
GameData = Dict[str, Board | int | str | Position | Dict[str, bool]]


def console_game(fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
    """
    Start a game in the console

    :param fen:
    :return:
    """
    data = load_fen(fen)
    board = data['board']
    en_passant = data['en_passant']
    turn = data['turn']  # 0 for white, 1 for black
    castles = data['castles']

    legal_moves_dict = get_all_legal_moves(board, turn, en_passant, castles)
    while True:
        draw_board(board)
        piece_tile = None

        while not coords_to_position(piece_tile) in legal_moves_dict:
            piece_tile = input(
                f'{"White" if turn == 0 else "Black"} turn\'s, choose a valid piece to move (e.g e{2 if turn == 0 else 7}):\n')
        piece_pos = coords_to_position(piece_tile)
        piece = board[piece_pos[0]][piece_pos[1]]
        legal_moves = legal_moves_dict[piece_pos]

        move_pos = None
        while move_pos not in legal_moves:
            move_chosen = input_valid_coords(
                f'Chose one of this tiles to move on:\n{" ".join(position_to_coords(move) for move in legal_moves)}\n')
            move_pos = coords_to_position(move_chosen)

        # Checking castles
        if (0, 0) == piece_pos or (0, 0) == move_pos:
            castles['q'] = False
        if (0, 7) == piece_pos or (0, 7) == move_pos:
            castles['k'] = False
        if (7, 0) == piece_pos or (7, 0) == move_pos:
            castles['Q'] = False
        if (7, 7) == piece_pos or (7, 7) == move_pos:
            castles['K'] = False
        if (0, 4) == piece_pos:
            castles['q'], castles['k'] = False, False
        if (7, 4) == piece_pos:
            castles['Q'], castles['K'] = False, False

        # Checking en-passant
        en_passant = None
        if piece == 1:
            if piece_pos[0] == 6 and move_pos[0] == 4:
                en_passant = (5, piece_pos[1])
        if piece == 7:
            if piece_pos[0] == 1 and move_pos[0] == 3:
                en_passant = (2, piece_pos[1])

        make_move(board, piece_pos, move_pos)
        legal_moves_dict = get_all_legal_moves(board, 1 - turn, en_passant, castles)
        if len(legal_moves_dict) == 0:
            draw_board(board)
            if len(get_white_checks(board) if turn == 0 else get_black_checks(board)) == 0:
                print('Stalemate!')
            else:
                print(f'{"White" if turn == 0 else "Black"} won by checkmate!')
            break
        turn = 1 - turn


def main(fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
    """
    The main entry, start a game in a pygame window

    :param fen:
    :return:
    """
    import pygame
    from src.app import App

    pygame.init()

    WIDTH = 900
    HEIGHT = 900

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    app = App(screen, load_fen(fen))
    app.run()

    pygame.quit()


if __name__ == '__main__':
    try:
        # main('2r4k/2b5/8/8/8/8/5PPP/2Q3K1 w KQkq - 0 1')
        main()
    except KeyboardInterrupt as e:
        print('\n\nBye, have a nice day!')
