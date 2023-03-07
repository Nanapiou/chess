"""
Some bot functions
"""
from typing import List, Dict, Tuple
from src.util import evaluate_position, load_fen
from src.moves import get_all_legal_moves, make_move_smooth, get_black_checks, get_white_checks

Board = List[List[int]]
Position = Tuple[int, int]
GameData = Dict[str, Board | int | str | Position | Dict[str, bool]]
DecisionTree = Dict[str, int | float | str | Dict[any, any] | Tuple[Position, Position]]


def create_decision_tree(game_data: GameData, dept: int, move: Tuple[Position, Position] = None) -> DecisionTree:
    """
    Create a decision tree that looks like
    {
        "game_data": The current game_data,
        "value": The board evaluation,
        "move": Tuple[Position, Position], the move that lead to this node,
        "children": List[DecisionTree],
    }

    :param game_data:
    :param dept:
    :param move:
    :return:
    """
    node = {
        "game_data": game_data,
        "value": evaluate_position(game_data['board']),
        "move": move
    }

    if dept > 0:
        all_legal_moves = get_all_legal_moves(game_data['board'], game_data['turn'], game_data['en_passant'],
                                              game_data['castles'])
        if len(all_legal_moves) == 0:
            if len(get_black_checks(game_data['board']) if game_data['turn'] == 0 else get_white_checks(
                    game_data['board'])) > 0:
                node['value'] = -10000 if game_data['turn'] == 0 else 10000
            else:
                node['value'] = 0
        else:
            node['children'] = []
            for piece_pos in all_legal_moves:
                for move in all_legal_moves[piece_pos]:
                    new_board = []
                    for l in game_data['board']:
                        new_board.append(l.copy())
                    new_data = make_move_smooth(new_board, piece_pos, move, game_data['en_passant'],
                                                game_data['castles'].copy())
                    child = create_decision_tree({
                        "board": new_board,
                        "turn": 1 - game_data["turn"],
                        "castles": new_data["castles"],
                        "en_passant": new_data["en_passant"]
                    }, dept - 1, (piece_pos, move))
                    node['children'].append(child)

    return node


def minimax(tree: DecisionTree, dept: int) -> Tuple[Position, Position]:
    """
    Return the best move for the root player

    :param tree:
    :param dept:
    :return:
    """
    if dept == 0 or 'children' not in tree:
        return tree

    if tree['game_data']['turn'] == 0:
        value = -10001
        best_child = None
        for child in tree['children']:
            current = minimax(child, dept - 1)
            if current['value'] > value:
                value = current['value']
                best_child = child
        tree['value'] = best_child['value']
        return best_child
    else:
        value = 10001
        best_child = None
        for child in tree['children']:
            current = minimax(child, dept - 1)
            if current['value'] < value:
                value = current['value']
                best_child = child
        tree['value'] = best_child['value']
        return best_child


if __name__ == '__main__':
    data = load_fen('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1')
    t = create_decision_tree(data, 3)
    import json

    with open('tree.json', 'w') as f:
        json.dump(t, f)
