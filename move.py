'''
Ivor Zalud
CS 5001

Representation of a move in checkers game
'''


class Move:
    def __init__(self, start, end, capture, captured_piece=None):
        self.start = start
        self.end = end
        self.capture = capture
        self.captured_piece = captured_piece

    def __str__(self):
        return str([self.start, self.end])