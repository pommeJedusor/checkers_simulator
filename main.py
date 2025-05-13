import random

EMPTY       = 0
WHITE       = 1
BLACK       = 2
MAN         = 4
KING        = 8
FLYING_KING = 16

class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def is_valid_position(self, width: int, height: int) -> bool:
        return 0 <= self.x < width and 0 <= self.y < height

class Move:
    def __init__(self, origin: Position, dest: Position, takes: list[Position]):
        self.origin = origin
        self.dest = dest
        self.takes = takes

class Settings:
    def __init__(self, width: int, height: int, nb_pieces_row_by_side: int, is_white_starting: bool, is_bottom_right_light: bool, must_take: bool, must_take_longest_sequence: bool, passing_promotion: bool, backward_capture: bool, orthogonal_captures: bool):
        self.width = width
        self.height = height
        self.nb_pieces_row_by_side = nb_pieces_row_by_side
        self.is_white_starting = is_white_starting
        self.is_bottom_right_light = is_bottom_right_light
        self.must_take = must_take
        self.must_take_longest_sequence = must_take_longest_sequence
        self.passing_promotion = passing_promotion
        self.backward_capture = backward_capture
        self.orthogonal_captures = orthogonal_captures
        self.board = []

    def generate_board(self) -> list[list[int]]:
        # empty board
        self.board = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]
        # white pieces
        for y in range(self.nb_pieces_row_by_side):
            self.board[y] = []
            for x in range(self.width):
                if x % 2 == y % 2:
                    self.board[y].append(EMPTY)
                else:
                    self.board[y].append(MAN | WHITE)
        # black pieces
        for y in range(self.height - self.nb_pieces_row_by_side, self.height):
            self.board[y] = []
            for x in range(self.width):
                if x % 2 == y % 2:
                    self.board[y].append(EMPTY)
                else:
                    self.board[y].append(MAN | BLACK)
        return self.board

class Checkers:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.current_player = WHITE
        if not settings.is_white_starting:
            self.current_player = BLACK

    def get_all_pieces_of_color(self, color) -> list[Position]:
        pieces = []
        for y in range(self.settings.height):
            for x in range(self.settings.width):
                if not self.settings.board[y][x] & color:
                    continue
                if self.settings.board[y][x]:
                    pieces.append(Position(x, y))
        return pieces

    def get_single_takes(self, last_piece_take_position: Position|None=None, taker: int|None=None) -> list[Move]:
        direction = 1
        if self.current_player == BLACK:
            direction = -1

        if last_piece_take_position:
            pieces = [last_piece_take_position]
        else:
            pieces = self.get_all_pieces_of_color(self.current_player)

        final_moves: list[Move] = []
        for piece in pieces:
            if not taker:
                taker = self.settings.board[piece.y][piece.x]

            moves: list[tuple[Position, Position]] = []
            if taker & MAN:
                moves.append((Position(piece.x - 1, piece.y + direction), Position(piece.x - 2, piece.y + direction * 2)))
                moves.append((Position(piece.x + 1, piece.y + direction), Position(piece.x + 2, piece.y + direction * 2)))
                if self.settings.backward_capture:
                    moves.append((Position(piece.x - 1, piece.y - direction), Position(piece.x - 2, piece.y - direction * 2)))
                    moves.append((Position(piece.x + 1, piece.y - direction), Position(piece.x + 2, piece.y - direction * 2)))
            elif taker & KING:
                moves.append((Position(piece.x - 1, piece.y + direction), Position(piece.x - 2, piece.y + direction * 2)))
                moves.append((Position(piece.x + 1, piece.y + direction), Position(piece.x + 2, piece.y + direction * 2)))
                moves.append((Position(piece.x - 1, piece.y - direction), Position(piece.x - 2, piece.y - direction * 2)))
                moves.append((Position(piece.x + 1, piece.y - direction), Position(piece.x + 2, piece.y - direction * 2)))
            elif taker & FLYING_KING:
                # TODO implement
                pass

            # filter out unvalid positions
            moves = [move for move in moves]

            for move in moves:
                if not move[0].is_valid_position(self.settings.width, self.settings.height):
                    continue
                if not move[1].is_valid_position(self.settings.width, self.settings.height):
                    continue
                if self.settings.board[move[1].y][move[1].x] != EMPTY:
                    continue
                if self.settings.board[move[0].y][move[0].x] & 0b11 == self.current_player ^ 0b11:
                    final_moves.append(Move(piece, move[1], [move[0]]))

        return final_moves

    def get_not_take_moves(self) -> list[Move]:
        """
        get all the moves except takes
        """
        direction = 1
        if self.current_player == BLACK:
            direction = -1

        final_moves: list[Move] = []
        pieces = self.get_all_pieces_of_color(self.current_player)
        for piece in pieces:
            moves: list[Position] = []
            if self.settings.board[piece.y][piece.x] & MAN:
                moves.append(Position(piece.x - 1, piece.y + direction))
                moves.append(Position(piece.x + 1, piece.y + direction))
            elif self.settings.board[piece.y][piece.x] & KING:
                moves.append(Position(piece.x - 1, piece.y + direction))
                moves.append(Position(piece.x + 1, piece.y + direction))
                moves.append(Position(piece.x - 1, piece.y - direction))
                moves.append(Position(piece.x + 1, piece.y - direction))
            elif self.settings.board[piece.y][piece.x] & FLYING_KING:
                # TODO implement
                pass

            for move in moves:
                if not move.is_valid_position(self.settings.width, self.settings.height):
                    continue
                if self.settings.board[move.y][move.x] != EMPTY:
                    continue
                final_moves.append(Move(piece, move, []))

        return final_moves

    def explore_take(self, take: Move, longest_sequences: list[list[Position]]|None=None, taker: int|None=None, longest_destinations: list[Position]|None=None) -> tuple[list[list[Position]], list[Position]]:
        if not longest_sequences:
            longest_sequences = []
        if not longest_destinations:
            longest_destinations = []
        must_put_back_taker = False
        if not taker:
            must_put_back_taker = True
            taker = self.settings.board[take.origin.y][take.origin.x]
            self.settings.board[take.origin.y][take.origin.x] = EMPTY

        previous_takes = [(previous_take.x, previous_take.y) for previous_take in take.takes]
        next_takes = self.get_single_takes(Position(take.dest.x, take.dest.y), taker)
        # filter out takes that have already been done
        next_takes = [next_take for next_take in next_takes if not (next_take.takes[0].x, next_take.takes[0].y) in previous_takes]

        for next_take in next_takes:
            take.takes.append(next_take.takes[0])

            dest, take.dest = take.dest, next_take.dest
            sequences, destinations = self.explore_take(take, longest_sequences, taker)
            take.dest, dest = dest, take.dest

            for i, sequence in enumerate(sequences):
                if not longest_sequences or len(sequence) > len(longest_sequences[0]):
                    longest_sequences = [sequence]
                    longest_destinations = [destinations[i]]
                elif len(sequence) == len(longest_sequences[0]):
                    longest_sequences.append(sequence)
                    longest_destinations.append(destinations[i])
            if not sequences:
                sequence = take.takes
                if not longest_sequences or len(sequence) > len(longest_sequences[0]):
                    longest_sequences = [[take for take in sequence]]
                    longest_destinations = [dest]
                elif len(sequence) == len(longest_sequences[0]):
                    longest_sequences.append([take for take in sequence])
                    longest_destinations.append(dest)
            take.takes.pop()

        if must_put_back_taker:
            self.settings.board[take.origin.y][take.origin.x] = taker
        return (longest_sequences or [], longest_destinations)

    def get_all_moves(self) -> list[Move]:
        single_takes = self.get_single_takes()
        if not single_takes:
            return self.get_not_take_moves()

        moves = []
        for take in single_takes:
            sequences, destinations = self.explore_take(take)
            for i in range(len(sequences)):
                sequence = sequences[i]
                destination = destinations[i]
                move = Move(take.origin, destination, sequence)
                moves.append(move)

        return moves or single_takes

    def make_move(self, move: Move):
        self.settings.board[move.origin.y][move.origin.x], self.settings.board[move.dest.y][move.dest.x] = self.settings.board[move.dest.y][move.dest.x], self.settings.board[move.origin.y][move.origin.x]
        for take in move.takes:
            self.settings.board[take.y][take.x] = EMPTY
        self.current_player ^= 0b11

    def cancel_move(self, move: Move):
        self.settings.board[move.origin.y][move.origin.x], self.settings.board[move.dest.y][move.dest.x] = self.settings.board[move.dest.y][move.dest.x], self.settings.board[move.origin.y][move.origin.x]
        for take in move.takes:
            self.settings.board[take.y][take.x] = EMPTY
        self.current_player ^= 0b11

def main():
    settings = Settings(10, 10, 4, True, True, True, True, False, True, False)
    settings.generate_board()
    checkers = Checkers(settings)
    checkers.make_move(Move(Position(0, 3), Position(2, 5), []))
    checkers.make_move(Move(Position(4, 7), Position(7, 4), []))
    
    while True:
        for row in checkers.settings.board:
            print(row)
        moves = checkers.get_all_moves()
        print("-- moves --")
        for move in moves:
            print(f"({move.origin.x}, {move.origin.y}), ({move.dest.x}, {move.dest.y})")

        if moves:
            next_move = random.choice(moves)
        else:
            print("no more move available")
            exit(0)
        print(f"next_move: ({next_move.origin.x}, {next_move.origin.y}), ({next_move.dest.x}, {next_move.dest.y})")
        input()
        checkers.make_move(next_move)

if __name__ == "__main__":
    main()
