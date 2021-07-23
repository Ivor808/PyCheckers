'''
Ivor Zalud
CS 5001

Representation of a move in checkers game
'''
import random


class AI:
    def __init__(self, moves):
        self.choice = 0
        self.moves = moves
        self.determine_move()

    def determine_move(self):
        """Determines the move the AI will choose
        """
        number_of_moves = range(len(self.moves))
        try:
            choice = random.choice(number_of_moves)
            self.choice = choice
        except IndexError:
            pass
