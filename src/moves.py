"""
Some moves getter functions
"""
from typing import List, Dict, Tuple
from src.util import position_to_coords

Board = List[List[int]]
Position = Tuple[int, int]
GameData = Dict[str, Board | int | str | Position | Dict[str, bool]]


def get_bishop_moves(board: Board, position: Position) -> List[Position]:
    """
    Return a list of move that the bishop can do

    :param board:
    :param position:
    :return:
    """
    x, y = position
    moves = []

    # diagonal moves
    for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        i, j = x + dx, y + dy
        while 0 <= i < 8 and 0 <= j < 8:
            if board[i][j] is None:
                moves.append((i, j))
            elif board[i][j] < 7 <= board[x][y] or board[i][j] >= 7 > board[x][y]:
                moves.append((i, j))
                break
            else:
                break
            i, j = i + dx, j + dy

    return moves


def get_rook_moves(board: Board, position: Position) -> List[Position]:
    """
    Return a list of move that the rook can do

    :param board:
    :param position:
    :return:
    """
    x, y = position
    moves = []

    # vertical/horizontal moves
    for dx, dy in [(1, 0), (0, -1), (0, 1), (-1, 0)]:
        i, j = x + dx, y + dy
        while 0 <= i < 8 and 0 <= j < 8:
            if board[i][j] is None:
                moves.append((i, j))
            elif board[i][j] < 7 <= board[x][y] or board[i][j] >= 7 > board[x][y]:
                moves.append((i, j))
                break
            else:
                break
            i, j = i + dx, j + dy

    return moves


def get_king_moves(board: Board, position: Position, castles: Dict[str, bool]) -> List[Position]:
    """
    Return a list of move that the king can do

    :param board:
    :param position:
    :param castles:
    :return:
    """
    x, y = position
    moves = []

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            i, j = x + dx, y + dy
            if not (0 <= i < 8 and 0 <= j < 8):
                continue
            piece = board[i][j]
            if piece is None or piece < 7 <= board[x][y] or piece >= 7 > board[x][y]:
                moves.append((i, j))

    # Castles
    if board[x][y] < 7:  # White
        if castles['K'] and board[7][5] is None and board[7][6] is None:
            if len(get_black_checks(board)) == 0 and len(get_black_checks(simulate_move(board, (7, 4), (7, 5)))) == 0:
                moves.append((7, 6))

        if castles['Q'] and board[7][3] is None and board[7][2] is None and board[7][1] is None:
            if len(get_black_checks(board)) == 0 and len(
                    get_black_checks(simulate_move(board, (7, 4), (7, 3)))) == 0 and len(
                get_black_checks(simulate_move(board, (7, 4), (7, 1)))) == 0:
                moves.append((7, 2))

    else:  # Black
        if castles['k'] and board[0][5] is None and board[0][6] is None:
            if len(get_white_checks(board)) == 0 and len(get_white_checks(simulate_move(board, (0, 4), (0, 5)))) == 0:
                moves.append((0, 6))

        if castles['q'] and board[0][3] is None and board[0][2] is None and board[0][1] is None:
            if len(get_white_checks(board)) == 0 and len(
                    get_white_checks(simulate_move(board, (0, 4), (0, 3)))) == 0 and len(
                get_white_checks(simulate_move(board, (0, 4), (0, 1)))) == 0:
                moves.append((0, 2))

    return moves


def get_knight_moves(board: Board, position: Position) -> List[Position]:
    """
    Return a list of move that the knight can do

    :param board:
    :param position:
    :return:
    """
    x, y = position
    moves = []

    for dx in (-2, -1, 1, 2):
        for dy in (-2, -1, 1, 2):
            if dx == dy or dx + dy == 0:
                continue
            i, j = x + dx, y + dy
            if not (0 <= i < 8 and 0 <= j < 8):
                continue
            piece = board[i][j]
            if piece is None or piece < 7 <= board[x][y] or piece >= 7 > board[x][y]:
                moves.append((i, j))

    return moves


def get_pawn_moves(board: Board, position: Position, en_passant: Position | None) -> List[Position]:
    """
    Return a list of move that the pawn can do

    :param board:
    :param position:
    :param en_passant:
    :return:
    """
    x, y = position
    moves = []

    fact = -1 if board[x][y] < 7 else 1  # Black 1, white -1
    if board[x + fact][y] is None:
        moves.append((x + fact, y))
        if ((x == 1 and fact == 1) or (x == 6 and fact == -1)) and board[x + fact * 2][y] is None:
            moves.append((x + fact * 2, y))

    for dy in (-1, 1):
        i, j = x + fact, y + dy
        if not (0 <= i < 8 and 0 <= j < 8):
            continue
        if (board[i][j] is not None and (board[x][y] < 7 <= board[i][j] or board[i][j] < 7 <= board[x][y])) or (
                i, j) == en_passant:
            moves.append((i, j))

    return moves


def get_moves(board: Board, position: Position, en_passant: Position | None, castles: Dict[str, bool]) -> List[
                                                                                                              Position] | None:
    """
    Return a list of moves at the given position, not legal

    :param board:
    :param position:
    :param en_passant:
    :param castles:
    :return:
    """
    x, y = position
    match (board[x][y]):
        case 3 | 9:  # Bishop
            return get_bishop_moves(board, position)
        case 4 | 10:  # Rooks
            return get_rook_moves(board, position)
        case 5 | 11:  # Queens
            return get_rook_moves(board, position) + get_bishop_moves(board, position)
        case 6 | 12:  # Kings
            return get_king_moves(board, position, castles)
        case 2 | 8:  # Knights
            return get_knight_moves(board, position)
        case 1 | 7:  # Pawns
            return get_pawn_moves(board, position, en_passant)


def get_legal_moves(board: Board, position: Position, en_passant: Position, castles: Dict[str, bool]) -> List[
                                                                                                             Position] | None:
    """
    Return a list of legals moves at the given position, basically just filter the return of get_moves depending on checks

    :param board:
    :param position:
    :param en_passant:
    :param castles:
    :return:
    """
    x, y = position
    moves = get_moves(board, position, en_passant, castles)
    if moves is None:
        return None
    legal_moves = []

    if board[x][y] < 7:  # White
        for move in moves:
            board_copy = simulate_move(board, position, move)
            if len(get_black_checks(board_copy)) == 0:
                legal_moves.append(move)
    else:
        for move in moves:
            board_copy = simulate_move(board, position, move)
            if len(get_white_checks(board_copy)) == 0:
                legal_moves.append(move)

    return legal_moves


def make_move(board: Board, pos1: Position, pos2: Position) -> Board:
    """
    Make a move into the board, return the board itself
    Doesn't check is the move is legal
    Handle castles en en-passant

    :param board:
    :param pos1:
    :param pos2:
    :return:
    """
    x1, y1 = pos1
    x2, y2 = pos2

    board[x1][y1], board[x2][y2] = None, board[x1][y1]
    return board

def make_move_smooth(board: Board, pos1: Position, pos2: Position, en_passant: Position, castles: Dict[str, bool]) -> GameData:
    """
    Make a move considering game data, and returning the new game data

    :param board:
    :param pos1:
    :param pos2:
    :param en_passant:
    :param castles:
    :return:
    """
    x1, y1 = pos1
    x2, y2 = pos2
    old_tiles = {
        pos1: board[x1][y1],
        pos2: board[x2][y2]
    }

    # Checking castles
    if (0, 0) == pos1 or (0, 0) == pos2:
        castles['q'] = False
    if (0, 7) == pos1 or (0, 7) == pos2:
        castles['k'] = False
    if (7, 0) == pos1 or (7, 0) == pos2:
        castles['Q'] = False
    if (7, 7) == pos1 or (7, 7) == pos2:
        castles['K'] = False
    if (0, 4) == pos1:
        castles['q'], castles['k'] = False, False
    if (7, 4) == pos1:
        castles['Q'], castles['K'] = False, False

    # Checking en-passant
    en_passant = None
    if board[x1][y1] == 1:
        if pos1[0] == 6 and pos2[0] == 4:
            en_passant = (5, pos1[1])
    if board[x1][y1] == 7:
        if pos1[0] == 1 and pos2[0] == 3:
            en_passant = (2, pos1[1])

    # Pawns things (promote, en-passant)
    if board[x1][y1] == 1 or board[x1][y1] == 7:
        if y1 != y2 and board[x2][
            y2] is None:  # En-passants, assuming that they are legal if there isn't a piece on a diagonal move from a pawn
            old_tiles[(x1, y2)] = board[x1][y2]
            board[x1][y2] = None
        if x2 == 7 or x2 == 0:  # Queen promotion, assuming that a pawn on the first or the last line can promote
            board[x1][y1] += 4  # From pawn to queen id

    # Castles, assuming that they are legal if the king love two tiles on a side
    if board[x1][y1] == 6 or board[x1][y1] == 12:
        if y2 - y1 == 2:  # King side
            old_tiles[(x1, 7)] = board[x1][7]
            old_tiles[(x1, 5)] = board[x1][5]
            make_move(board, (x1, 7), (x1, 5))
        elif y1 - y2 == 2:  # Queen side
            old_tiles[(x1, 0)] = board[x1][0]
            old_tiles[(x1, 3)] = board[x1][3]
            make_move(board, (x1, 0), (x1, 3))

    make_move(board, pos1, pos2)
    return {
        "board": board,
        "castles": castles,
        "en_passant": en_passant,
        "old_tiles": old_tiles
    }

def reverse_moves(board: Board, old_tiles: Dict[Position, int]) -> Board:
    """
    Just reverse moves, basically just assign dict values
    Return the board itself

    :param board:
    :param old_tiles:
    :return:
    """
    for pos in old_tiles:
        board[pos[0]][pos[1]] = old_tiles[pos]
    return board



def simulate_move(board: Board, pos1: Position, pos2: Position) -> Board:
    """
    Create a new board and make the move in it

    :param board:
    :param pos1:
    :param pos2:
    :return:
    """
    new_board = []
    for l in board:
        new_board.append(l.copy())
    return make_move(new_board, pos1, pos2)


def get_all_legal_moves(board: Board, player: int, en_passant: Position, castles: Dict[str, bool]) -> Dict[
    Position, List[Position]]:
    """
    Get all the legal moves available for the player

    :param board:
    :param player:
    :param en_passant:
    :param castles:
    :return:
    """
    pieces, legal_moves = [], {}
    for i in range(8):
        for j in range(8):
            if board[i][j] is not None and ((player == 0 and board[i][j] < 7) or (player == 1 and board[i][j] >= 7)):
                pieces.append((i, j))
    for piece_pos in pieces:
        moves = get_legal_moves(board, piece_pos, en_passant, castles)
        if len(moves) > 0:
            # legal_moves[position_to_coords(piece_pos)] = moves
            legal_moves[piece_pos] = moves
    return legal_moves


def is_legal(board: Board, pos1: Position, pos2: Position, en_passant: Position, castles: Dict[str, bool]) -> bool:
    """
    Return whether the move is legal or not

    :param board:
    :param pos1:
    :param pos2:
    :param en_passant:
    :param castles:
    :return:
    """
    return pos2 in get_legal_moves(board, pos1, en_passant, castles)


def get_white_checks(board: Board) -> List[Position]:
    """
    Return the list of checks that the white player is giving

    :param board:
    :return:
    """
    pieces_pos = []
    black_king = None
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece is not None:
                if piece == 12:
                    black_king = (i, j)
                elif piece < 7:
                    pieces_pos.append((i, j))
    checks = []
    for piece_pos in pieces_pos:
        for move in get_moves(board, piece_pos, None, {'q': False, 'Q': False, 'K': False, 'k': False}):
            if move == black_king:
                checks.append(piece_pos)
    return checks


def get_black_checks(board: Board) -> List[Position]:
    """
    Return the list of checks that the black player is giving

    :param board:
    :return:
    """
    pieces_pos = []
    white_king = None
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece is not None:
                if piece == 6:
                    white_king = (i, j)
                elif piece >= 7:
                    pieces_pos.append((i, j))
    checks = []
    for piece_pos in pieces_pos:
        for move in get_moves(board, piece_pos, None, {'q': False, 'Q': False, 'K': False, 'k': False}):
            if move == white_king:
                checks.append(piece_pos)
    return checks
