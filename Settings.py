from consts import *

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
