'''
Ivor Zalud
CS 5001, Fall 2020

Main function for the checkes game
'''
import turtle
from gamestate import GameState

NUM_SQUARES = 8  # The number of squares on each row.
SQUARE = 50  # The size of each square in the checkerboard.
SQUARE_COLORS = ("light gray", "white")
PIECE_RADIUS = SQUARE / 2
BOARD_SIZE = NUM_SQUARES * SQUARE
CORNER = -BOARD_SIZE / 2


def main():
    # draws the initial board
    board = GameState(NUM_SQUARES, SQUARE)


if __name__ == "__main__":
    main()
