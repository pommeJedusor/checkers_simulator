class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def is_valid_position(self, width: int, height: int) -> bool:
        return 0 <= self.x < width and 0 <= self.y < height
