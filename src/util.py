"""
Useful things
"""
from typing import List, Dict, Tuple

Board = List[List[int]]
Position = Tuple[int, int]
GameData = Dict[str, Board | int | str | Position | Dict[str, bool]]

pieces_ids = {
    'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
    'p': 7, 'n': 8, 'b': 9, 'r': 10, 'q': 11, 'k': 12,
    ' ': None
}
for key in tuple(e for e in pieces_ids):
    pieces_ids[pieces_ids[key]] = key

pieces_values = [None, 10, 30, 30, 50, 90, 900, -10, -30, -30, -50, -90, -900]

# Scores on position
pawn_table = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
    [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
    [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
    [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
    [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
    [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
]

knight_table = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
    [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
    [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
    [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
    [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
    [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
    [-5.0, 4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
]

bishop_table = [
    [-2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
    [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
    [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
    [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
    [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
    [-2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -2.0]
]

rook_table = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
]

queen_table = [
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
    [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
    [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
    [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]

king_table = [
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
    [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
]


def draw_matrix(mat: List[List[any]], src: Dict[any, any]) -> None:
    """
    Draw a matrix.
    """
    line = "+---" * len(mat[0]) + "+"
    print(line)
    for l in mat:
        print('| ', end='')
        for e in l:
            print(src[e] if e in src else e, end=' | ')
        print()
        print(line)


def draw_board(board: Board):
    """
    Draw a chess board

    :param board:
    :return:
    """
    return draw_matrix(board, pieces_ids)


def load_fen(string: str) -> GameData:
    """
    Load a fen format

    :param string:
    :return:
    """
    board, last = [[]], None
    for i in range(len(string)):
        e = string[i]
        if e == ' ':
            last = string[i + 1:]
            break
        if e.isdigit():
            board[-1].extend([None] * int(e))
        elif e == '/':
            board.append([])
        else:
            board[-1].append(pieces_ids[e])
    if last is None:
        raise SyntaxError('Invalid FEN')

    parts = last.split(' ')
    if len(parts) != 5:
        raise SyntaxError('Invalid FEN')

    turn, castles, en_passant, count_b, count = parts
    return {
        'board': board,
        'turn': 0 if turn == 'w' else 1,
        'castles': {
            'K': 'K' in castles,
            'Q': 'Q' in castles,
            'k': 'k' in castles,
            'q': 'q' in castles,
        },
        'en_passant': coords_to_position(en_passant) if en_passant != '-' else None,
        'count_b': int(count_b),
        'count': int(count),
    }

def create_fen(game_data: GameData) -> str:
    """
    Create a FEN string from a game data

    :param game_data:
    :return:
    """
    string = ""
    for l in game_data['board']:
        void_count = 0
        for e in l:
            if e is None:
                void_count += 1
            else:
                if void_count != 0:
                    string += str(void_count)
                    void_count = 0
                string += pieces_ids[e]
        if void_count != 0:
            string += str(void_count)
        string += '/'
    return string[:-1] + f' {"w" if game_data["turn"] == 0 else "b"} {"".join(e for e in game_data["castles"] if game_data["castles"] and e in "KQkq")} {"-" if game_data["en_passant"] is None else position_to_coords(game_data["en_passant"])} {game_data["count_b"]} {game_data["count"]}'



def coords_to_position(coords: str) -> Position:
    """
    Convert something like 'e4' in (4, 4), into a matrix coordinates

    :param coords:
    :return:
    """
    return 8 - int(coords[1]), 'abcdefgh'.index(coords[0])


def position_to_coords(pos: Position) -> str:
    """
    Convert something like (4, 4) in 'e4', into a check tile name

    :param pos:
    :return:
    """
    return 'abcdefgh'[pos[1]] + str(8 - pos[0])


def input_valid_coords(text):
    """
    Ask for valid coords

    :param text:
    :return:
    """
    coords = '__'
    while len(coords) != 2 or coords[0] not in 'abcdefgh' or not coords[1].isdigit():
        coords = input(text)
    return coords


def evaluate_position(board: Board):
    """
    Evaluate the board position
    Negative is good for black, positive is good for white

    :param board:
    :return:
    """
    total = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] is not None:
                total += pieces_values[board[i][j]]
                match board[i][j]:
                    case 1:
                        total += pawn_table[i][j]
                    case 2:
                        total += knight_table[i][j]
                    case 3:
                        total += bishop_table[i][j]
                    case 4:
                        total += rook_table[i][j]
                    case 5:
                        total += queen_table[i][j]
                    case 6:
                        total += king_table[i][j]
                    case 7:
                        total -= pawn_table[7 - i][j]
                    case 8:
                        total -= knight_table[7 - i][j]
                    case 9:
                        total -= bishop_table[7 - i][j]
                    case 10:
                        total -= rook_table[7 - i][j]
                    case 11:
                        total -= queen_table[7 - i][j]
                    case 12:
                        total -= king_table[7 - i][j]

    return total


if __name__ == '__main__':
    data = load_fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    print(data)
    fen = create_fen(data)
    print(fen)
