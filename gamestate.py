'''
Ivor Zalud
CS 5001

Representation of the checkers game state
'''
from piece import Piece
import copy
from copy import deepcopy
import turtle
from move import Move
from ai import AI


class GameState:
    def __init__(self, squares, square_size, test_mode=False):
        self.SQUARES = squares
        self.SQUARE_SIZE = square_size
        self.BOARD_SIZE = self.SQUARES * self.SQUARE_SIZE
        self.CORNER = -1 * (self.BOARD_SIZE / 2)
        self.PIECE_RADIUS = self.SQUARE_SIZE / 2
        self.SQUARE_COLORS = "light gray"
        self.PLAYER_COLOR = {1: "Black", 2: "Red"}
        self.KING_COLOR = "Blue"
        self.PLAYER_DIRECTIONS = {1: [[1, 1], [-1, 1]], 2: [[1, -1], [-1, -1]]}

        self.board_state = []
        self.player_turn = 1
        self.previos_selection = [0, 0]
        self.selected_cell = [0, 0]
        self.valid_moves = []
        self.previous_move_a_capture = False
        self.previous_moved_piece_pos = [0, 0]
        self.test_mode = test_mode

        if not self.test_mode:
            self.setup_board()
            self.create_board()
            self.pen = turtle.Turtle()
            self.pen.penup()
            self.pen.hideturtle()
            self.pen.color("black", "white")
            self.create_screen()
            self.draw_default_board()
            self.draw_players_rows()
            self.screen = turtle.Screen()
            self.screen.onclick(self.click_listen)
            turtle.done()

    def print_board(self):
        """Prints out the board to be user friendly
        """
        lst = deepcopy(self.board_state)
        for y in range(self.SQUARES):
            for x in range(self.SQUARES):
                if self.board_state[y][x] != 0:
                    lst[y][x] = self.board_state[y][x].COLOR[0]
        lst.reverse()
        for i in range(len(lst)):
            print(lst[i])
        return lst

    def print_valid_moves(self, moves):
        """Prints the valid moves

        Args:
            moves (list): the list of moves
        """
        print("Moves: ")
        for move in moves:
            print(move)

    def setup_board(self):
        """Creates the initial board with all empty slots
        """
        for row in range(self.SQUARES):
            self.board_state.append([])
            for cell in range(self.SQUARES):
                self.board_state[row].append(0)

    def create_screen(self):
        """Creates the initial screen
        """
        window_size = self.BOARD_SIZE + self.SQUARE_SIZE
        turtle.setup(window_size, window_size)
        turtle.screensize(self.BOARD_SIZE, self.BOARD_SIZE)
        turtle.bgcolor("white")
        turtle.tracer(0, 0)

    def click_listen(self, x, y):
        """Click listener for turtle class with added functionality for
        checkers

        Args:
            x (float): x cord
            y (float): y cord
        """
        self.selected_cell = self.coords_conversion(x, y)
        xcord = self.selected_cell[0]
        ycord = self.selected_cell[1]
        prev_xcord = self.previos_selection[0]
        prev_ycord = self.previos_selection[1]
        if self.check_out_of_bounds(x, y):
            print("Out of bonds")
        else:
            if self.previous_move_a_capture:
                pieces = self.board_state[self.previous_moved_piece_pos[1]][
                    self.previous_moved_piece_pos[0]]
                moves = self.get_valid_moves([pieces])
            else:
                pieces = self.get_player_pieces()
                moves = self.get_valid_moves(pieces)

            if self.check_if_selection_in_moves(
                    prev_xcord, prev_ycord, xcord, ycord,
                    moves) or self.player_turn == 2:
                move = self.get_current_move(prev_xcord, prev_ycord, xcord,
                                             ycord, moves)
                try:
                    self.move_piece(move)
                except AttributeError:
                    pass
                self.reset_board()
                if self.player_turn == 2:
                    self.ai_move()
                self.reset_board()
        if self.determine_win():
            print("Game over, ", self.player_turn, " loses!")

        self.previos_selection = self.selected_cell

    def determine_win(self):
        """Determines if a win gamestate has been reached

        Returns:
            boolean: True if a win as occured, false if not
        """
        num_player_pieces = len(self.get_player_pieces())
        num_valid_moves = len(self.get_valid_moves(self.get_player_pieces()))
        if num_player_pieces == 0 or num_valid_moves == 0:
            return True
        else:
            self.player_turn == 2
            num_player_pieces = len(self.get_player_pieces())
            num_valid_moves = len(
                self.get_valid_moves(self.get_player_pieces()))
            print(self.get_valid_moves(self.get_player_pieces())[0])
            if num_player_pieces == 0 or num_valid_moves == 0:
                return True
        self.player_turn == 1
        return False

    def ai_move(self):
        """Completes an AI move
        """

        pieces = self.get_player_pieces()
        moves = self.get_valid_moves(pieces)
        ai = AI(moves)
        try:
            self.move_piece(moves[ai.choice])
            if self.previous_move_a_capture:
                self.ai_move()
        except IndexError:
            pass

    def iterate_turn(self):
        """Iterates the game turn
        """
        if self.player_turn == 1:
            self.player_turn += 1
        elif self.player_turn == 2:
            self.player_turn -= 1

    def check_out_of_bounds(self, x, y):
        """Checks if a given coordinate is out of bounds of the game screen

        Args:
            x (float): x coord
            y (float): y coord

        Returns:
            boolean: true if out of bounds, false if not
        """
        if x < -(self.BOARD_SIZE) / 2 or x > (self.BOARD_SIZE) / 2 or y < -(
                self.BOARD_SIZE) / 2 or y > (self.BOARD_SIZE) / 2:
            return True
        else:
            return False

    def move_piece(self, move):
        """Moves a game piece given a chosen Move

        Args:
            move (Move): Move object containing the desired move
        """
        def copy_piece_to_position(move):
            self.board_state[move.end[1]][move.end[0]] = deepcopy(
                self.board_state[move.start[1]][move.start[0]])

            self.board_state[move.end[1]][move.end[0]].position[1] += (
                self.SQUARE_SIZE * (move.end[1] - move.start[1]))
            self.board_state[move.end[1]][move.end[0]].position[0] += (
                self.SQUARE_SIZE * (move.end[0] - move.start[0]))

            self.previous_moved_piece_pos[1] = move.end[1]
            self.previous_moved_piece_pos[0] = move.end[0]
            self.board_state[move.start[1]][move.start[0]] = 0

        def check_move_type(move):
            if move.end[1] == self.SQUARES - 1 or move.end[1] == 0:
                player_direction = self.PLAYER_DIRECTIONS[
                    get_other_player_turn()]
                self.board_state[move.end[1]][move.end[0]].set_king()
                self.board_state[move.end[1]][move.end[0]].direction.append(
                    player_direction[0])
                self.board_state[move.end[1]][move.end[0]].direction.append(
                    player_direction[1])
            if move.capture:
                self.previous_move_a_capture = True
                self.board_state[move.captured_piece[1]][
                    move.captured_piece[0]] = 0
                if not self.check_for_captures(self.previous_moved_piece_pos):
                    self.previous_move_a_capture = False
                    self.iterate_turn()

            else:
                self.iterate_turn()

        def get_other_player_turn():
            if self.player_turn == 1:
                return 2
            else:
                return 1

        copy_piece_to_position(move)
        check_move_type(move)

    def reset_board(self):
        """Resets the board based on the board state
        """
        self.pen.color("black", "white")
        self.draw_default_board()
        self.draw_players_rows()

    def draw_default_board(self):
        """Draws the default checkers board

        Args:
            pen (pen): the pen
        """
        self.pen.setposition(self.CORNER, self.CORNER)
        self.draw_square(self.BOARD_SIZE)
        self.pen.color("black", self.SQUARE_COLORS)
        for col in range(self.SQUARES):
            for row in range(self.SQUARES):
                if col % 2 != row % 2:
                    self.pen.setposition(self.CORNER + self.SQUARE_SIZE * row,
                                         self.CORNER + self.SQUARE_SIZE * col)
                    self.draw_square(self.SQUARE_SIZE)

    def draw_square(self, size):
        '''
            Function -- draw_square
                Draw a square of a given size.
            Parameters:
                a_turtle -- an instance of Turtle
                size -- the length of each side of the square
            Returns:
                Nothing. Draws a square in the graphics window.
        '''
        RIGHT_ANGLE = 90
        self.pen.pendown()
        self.pen.begin_fill()
        for i in range(4):
            self.pen.forward(size)
            self.pen.left(RIGHT_ANGLE)
        self.pen.end_fill()
        self.pen.penup()

    def draw_players_rows(self):
        """Draws the pieces on the board

        Args:
            pen (turtle): the pen
            board (list): the list representation of the game
        """
        for row in range(self.SQUARES):
            for cell in range(self.SQUARES):
                spot = self.board_state[row][cell]
                if spot == 0:
                    pass
                else:
                    self.pen.setposition(spot.position[0], spot.position[1])
                    self.draw_piece(self.PIECE_RADIUS, spot.COLOR)
                    if spot.king:
                        self.pen.setposition(
                            spot.position[0],
                            spot.position[1] + self.SQUARE_SIZE / 4)
                        self.draw_piece(self.PIECE_RADIUS / 2, self.KING_COLOR)

    def draw_piece(self, size, color):
        """Draws a checkers piece

        Args:
            turtle (turtle): the pen
            size (int): the size of the piece
            color (string): the color of the piece
        """
        self.pen.pendown()
        self.pen.begin_fill()
        self.pen.color(color)
        self.pen.circle(size - 1)
        self.pen.end_fill()
        self.pen.penup()

    def get_valid_moves(self, pieces):
        """Gets the valid moves given a set of game pieces

        Args:
            pieces (list): list of game pieces

        Returns:
            list: list of valid move objects
        """
        moves = []
        capture_exist = False
        for piece in pieces:
            converted_pos = self.coords_conversion(piece.position[0],
                                                   piece.position[1])
            x = converted_pos[0]
            y = converted_pos[1]
            capture = 0
            non_capture = 0
            for direction in piece.direction:
                move_x = x + direction[0]
                move_y = y + direction[1]
                if not self.check_out_of_bounds_list(move_x, move_y):
                    if self.board_state[move_y][
                            move_x] == 0 and not self.previous_move_a_capture:
                        move = Move([x, y], [move_x, move_y], False)
                        moves.append(move)
                        non_capture = move
                    elif self.board_state[move_y][
                            move_x] != 0 and self.board_state[move_y][
                                move_x].COLOR != self.PLAYER_COLOR[
                                    self.player_turn]:
                        captured_piece = [move_x, move_y]
                        move_x += direction[0]
                        move_y += direction[1]
                        if not self.check_out_of_bounds_list(move_x, move_y):
                            # Capturing move and adjacent cell is blank
                            if self.board_state[move_y][move_x] == 0:
                                move = Move([x, y], [move_x, move_y], True,
                                            captured_piece)
                                moves.insert(0, move)
                                capture = move
                                capture_exist = True

        if capture_exist:
            capture_moves = self.get_capture_moves(moves)
            return capture_moves
        return moves

    def get_capture_moves(self, moves):
        """Get the capturing moves from a list of given Move objects

        Args:
            moves (list): list of move objects

        Returns:
            list: list of Move objects with capture set to True
        """
        lst = []
        for move in moves:
            if move.capture:
                lst.append(move)
        return lst

    def check_out_of_bounds_list(self, x, y):
        """Checks if a given cell reference is out of bounds of the game board

        Args:
            x (int): x cord related to list
            y (int): y cord related to list

        Returns:
            bool: true if out of bounds, false if in bounds
        """
        if x not in range(self.SQUARES) or y not in range(self.SQUARES):
            return True
        else:
            return False

    def get_player_pieces(self):
        """Returns all the current game pieces of the current player

        Returns:
            list: list of game Pieces objects
        """
        pieces = []
        color = self.PLAYER_COLOR[self.player_turn]
        for y in range(self.SQUARES):

            for x in range(self.SQUARES):
                if self.board_state[y][x] != 0 and self.board_state[y][
                        x].COLOR == color:
                    pieces.append(self.board_state[y][x])

        return pieces

    def coords_conversion(self, x, y):
        """Converts pixel coordinates to list representation coordinates

        Args:
            x (float): x coords for pixels
            y (float): y coords for pixels

        Returns:
            list: x and y coords for list representation
        """
        lst = []
        cell = 0
        if x <= 0:
            difference = self.CORNER - x
            cell = abs(difference // self.SQUARE_SIZE) - 1
            if cell < 0:
                cell = 0
        else:
            difference = abs(self.CORNER) - 1 + x
            cell = abs(difference // self.SQUARE_SIZE)

        row = 0
        if y <= 0:
            difference = self.CORNER - y
            row = abs(difference // self.SQUARE_SIZE) - 1
            if row < 0:
                row = 0
        else:
            difference = abs(self.CORNER) - 1 + y
            row = abs(difference // self.SQUARE_SIZE)

        lst.append(int(cell))
        lst.append(int(row))
        return lst

    def create_board(self):
        """Creates the game board represented as a list of lists
        """
        for row in range(self.SQUARES):
            y = self.CORNER + (self.SQUARE_SIZE * row) + 1
            x = self.CORNER + self.PIECE_RADIUS
            if row % 2 == 0:
                for cell in range(1, self.SQUARES + 1):
                    if cell % 2 == 0:
                        if row < 3:
                            self.board_state[row][cell - 1] = Piece(
                                "Black", [x, y], False, [[1, 1], [-1, 1]])
                        elif row >= 5:
                            self.board_state[row][cell - 1] = Piece(
                                "Red", [x, y], False, [[1, -1], [-1, -1]])
                    else:
                        self.board_state[row][cell - 1] = 0
                    x += self.SQUARE_SIZE
            else:
                for cell in range(1, self.SQUARES + 1):
                    if cell % 2 != 0:
                        if row < 3:
                            self.board_state[row][cell - 1] = Piece(
                                "Black", [x, y], False, [[1, 1], [-1, 1]])
                        elif row >= 5:
                            self.board_state[row][cell - 1] = Piece(
                                "Red", [x, y], False, [[1, -1], [-1, -1]])
                    x += self.SQUARE_SIZE

    def check_if_selection_in_moves(self, prev_x, prev_y, x, y, moves):
        """Checks if the selected move is in the list of valid moves

        Args:
            prev_x (int): previous x coordinate click
            prev_y (int): previous y coordinate click
            x (int): current x coordinate click
            y (int): current y coordinate click
            moves (list): list of Move objects

        Returns:
            bool: True if the move is in the set of valid Moves or false if not
        """
        prev_move = [prev_x, prev_y]
        current_move = [x, y]
        for move in moves:
            if prev_move == move.start and current_move == move.end:
                return True
        return False

    def get_current_move(self, prev_x, prev_y, x, y, moves):
        """Gets the Move object according to the players selected move

        Args:
            prev_x (int): previous x coordinate based on the list
            prev_y (int): previous y coordinate based on the list
            x (int): current x coordinate based on the list
            y (int): current y coordinate based on the list
            moves (list): list of Move objects

        Returns:
            Move: the selected move as a Move object
        """
        prev_move = [prev_x, prev_y]
        current_move = [x, y]
        for move in moves:
            if prev_move == move.start and current_move == move.end:
                return move

    def check_for_captures(self, loc):
        """Checks if the game piece has any capture moves possible

        Args:
            loc (list): list containg the x,y coordinates (list) of the game
            piece

        Returns:
            boolean: True if the move has captures, false if not
        """
        x = loc[0]
        y = loc[1]
        piece = self.board_state[y][x]
        moves = self.get_valid_moves([piece])
        captures = self.get_capture_moves(moves)
        if len(captures) > 0:
            return True
        else:
            return False
