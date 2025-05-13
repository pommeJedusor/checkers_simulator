from Position import Position

class Move:
    def __init__(self, origin: Position, dest: Position, takes: list[Position], taken_pieces: list[int]):
        self.origin = origin
        self.dest = dest
        self.takes = takes
        self.taken_pieces = taken_pieces
