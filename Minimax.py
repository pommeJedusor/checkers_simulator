from consts import *
from Checkers import Checkers
from Position import Position
from Settings import Settings
from Move import Move

DEPTH_MAX = 1

def get_board_eval(game: Checkers) -> int:
    score = 0
    for row in game.settings.board:
        for square in row:
            player = square & 0b11
            score += game.current_player == player
            score -= game.current_player == player ^ 0b11
    return score

def minimax(game: Checkers, depth: int=0) -> tuple[Move|None, int]:
    if depth >= DEPTH_MAX:
        return None, get_board_eval(game)

    best_move, best_score = None, -666
    for move in game.get_all_moves():
        game.make_move(move)
        _, score = minimax(game, depth + 1)
        score = -score
        game.cancel_move(move)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move, best_score

def main():
    settings = Settings(10, 10, 4, True, True, True, True, False, True, False)
    settings.generate_board()
    checkers = Checkers(settings)
    checkers.make_move(Move(Position(0, 3), Position(1, 4), [], []))
    checkers.make_move(Move(Position(5, 6), Position(4, 5), [], []))
    checkers.make_move(Move(Position(1, 2), Position(0, 3), [], []))
    checkers.make_move(Move(Position(7, 6), Position(6, 5), [], []))
    checkers.make_move(Move(Position(0, 1), Position(1, 2), [], []))
    checkers.make_move(Move(Position(1, 6), Position(2, 5), [], []))
    checkers.make_move(Move(Position(1, 0), Position(0, 1), [], []))
    checkers.make_move(Move(Position(9, 6), Position(8, 5), [], []))
    checkers.make_move(Move(Position(6, 3), Position(5, 4), [], []))
    checkers.make_move(Move(Position(4, 5), Position(6, 3), [Position(5, 4)], []))
    for row in checkers.settings.board:
        print(row)
    move, score = minimax(checkers)
    print(f"move: ({move.origin.x}, {move.origin.y}), ({move.dest.x}, {move.dest.y})")
    print(score)

if __name__ == "__main__":
    main()
