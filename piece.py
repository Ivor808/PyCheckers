'''
Ivor Zalud
CS 5001

Representation of the checkers game piece
'''


class Piece:
    def __init__(self, color, position, king, direction):
        self.COLOR = color
        self.position = position
        self.king = king
        self.direction = direction

    def set_king(self):
        self.king = True

    def __str__(self):
        return self.COLOR
