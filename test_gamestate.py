from gamestate import GameState
from piece import Piece
from move import Move
from ai import AI


def test_setup_board():
    game = GameState(8, 50, True)
    game.setup_board()
    gamestate = game.board_state
    board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

    assert (board == gamestate)


def test_create_board():
    game = GameState(8, 50, True)
    game.setup_board()
    game.create_board()
    lst = game.print_board()
    board = [['R', 0, 'R', 0, 'R', 0, 'R',
              0], [0, 'R', 0, 'R', 0, 'R', 0, 'R'],
             ['R', 0, 'R', 0, 'R', 0, 'R', 0], [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0], [0, 'B', 0, 'B', 0, 'B', 0, 'B'],
             ['B', 0, 'B', 0, 'B', 0, 'B', 0],
             [0, 'B', 0, 'B', 0, 'B', 0, 'B']]
    assert (board == lst)


def test_determine_win():

    game = GameState(8, 50, True)
    game.setup_board()
    assert (game.determine_win())
    game.create_board()
    assert not (game.determine_win())

    # Remove Red pieces to determine win
    for i in range(len(game.board_state)):
        for j in range(len(game.board_state)):
            try:
                if game.board_state[i][j].COLOR == "Red":
                    game.board_state[i][j] = 0
            except AttributeError:
                pass
    game.player_turn = 2
    assert (game.determine_win())

    # Remove black pieces to determine win
    game.create_board()
    for i in range(len(game.board_state)):
        for j in range(len(game.board_state)):
            try:
                if game.board_state[i][j].COLOR == "Black":
                    game.board_state[i][j] = 0
            except AttributeError:
                pass
    game.player_turn = 1
    assert (game.determine_win())

    # Edge case where 1 piece left and no valid moves for red
    game.create_board()
    for i in range(len(game.board_state)):
        for j in range(len(game.board_state)):
            try:
                if game.board_state[i][j].COLOR == "Red":
                    game.board_state[i][j] = 0
            except AttributeError:
                pass
    # set a red game piece to a locked position
    game.board_state[3][0] = Piece("Red", [-175.0, -49.0], False,
                                   [[1, -1], [-1, -1]])
    game.player_turn = 2
    game.print_board()
    assert (game.determine_win())

    # Edge case where 1 piece left and no valid moves for black
    game.create_board()
    for i in range(len(game.board_state)):
        for j in range(len(game.board_state)):
            try:
                if game.board_state[i][j].COLOR == "Black":
                    game.board_state[i][j] = 0
            except AttributeError:
                pass
    # set a black game piece to a locked position
    game.board_state[4][7] = Piece("Black", [175, 1], False, [[1, 1], [-1, 1]])
    game.player_turn = 1
    assert (game.determine_win())


def test_iterate_turn():
    # Black to red
    game = GameState(8, 50, True)
    game.iterate_turn()
    assert (game.player_turn == 2)
    # Red to Black
    game.iterate_turn()
    assert (game.player_turn == 1)


def test_check_out_of_bounds():
    game = GameState(8, 50, True)
    assert (game.check_out_of_bounds(game.BOARD_SIZE + 5, game.BOARD_SIZE + 5))
    assert not (game.check_out_of_bounds(0, 0))


def test_move_piece():
    game = GameState(8, 50, True)
    game.setup_board()
    game.create_board()
    # Black non capture move
    move = Move([1, 2], [0, 3], False)
    game.move_piece(move)
    assert (game.board_state[3][0].COLOR == "Black")
    # Red non capture move
    move = Move([0, 5], [1, 4], False)
    game.move_piece(move)
    assert (game.board_state[4][1].COLOR == "Red")

    # Black capture move
    game = GameState(8, 50, True)
    game.setup_board()
    game.create_board()
    # move red piece into position to be captured
    move = Move([2, 5], [2, 3], False)
    game.move_piece(move)
    game.player_turn = 1
    pieces = game.get_player_pieces()
    moves = game.get_valid_moves(pieces)
    capture_move = False
    for move in moves:
        if move.capture:
            capture_move = True
    # shows capturing move is available after we moved red piece into position
    assert (capture_move)
    # Red capture move
    game = GameState(8, 50, True)
    game.setup_board()
    game.create_board()
    # move red piece into position to be captured
    move = Move([1, 2], [1, 4], False)
    game.move_piece(move)
    game.player_turn = 2
    pieces = game.get_player_pieces()
    moves = game.get_valid_moves(pieces)
    capture_move = False
    for move in moves:
        if move.capture:
            capture_move = True
    # shows capturing move is available after we moved black piece into
    # position
    assert (capture_move)


def test_get_valid_moves():
    game = GameState(8, 50, True)
    game.setup_board()
    game.create_board()
    pieces = game.get_player_pieces()
    moves = game.get_valid_moves(pieces)
    assert (len(moves) == 7)
    game.player_turn == 2
    assert (len(moves) == 7)


def test_get_capture_moves():
    # Black
    game = GameState(8, 50, True)
    game.setup_board()
    game.create_board()
    # move red piece into position to be captured
    move = Move([2, 5], [2, 3], False)
    game.move_piece(move)
    game.player_turn = 1
    pieces = game.get_player_pieces()
    moves = game.get_valid_moves(pieces)
    capture = game.get_capture_moves(moves)
    assert (len(capture) == 2)
    # Red
    game = GameState(8, 50, True)
    game.setup_board()
    game.create_board()
    # move red piece into position to be captured
    move = Move([1, 2], [1, 4], False)
    game.move_piece(move)
    game.player_turn = 2
    pieces = game.get_player_pieces()
    moves = game.get_valid_moves(pieces)
    capture = game.get_capture_moves(moves)
    assert (len(capture) == 2)


def test_check_out_of_bounds_list():
    game = GameState(8, 50, True)
    game.setup_board()
    game.create_board()
    assert (game.check_out_of_bounds_list(game.SQUARES + 1, 0))
    assert (game.check_out_of_bounds_list(0, game.SQUARES + 1))
    assert not (game.check_out_of_bounds_list(game.SQUARES - 1, 0))
    assert not (game.check_out_of_bounds_list(0, game.SQUARES - 1))


def test_get_player_pieces():
    game = GameState(8, 50, True)
    game.setup_board()
    game.create_board()
    assert (len(game.get_player_pieces()) == 12)
    game.player_turn == 2
    assert (len(game.get_player_pieces()) == 12)
    # Remove a game piece
    game.board_state[0][1] = 0
    game.player_turn == 1
    game.print_board()
    assert (len(game.get_player_pieces()) == 11)


def test_coords_conversion():
    game = GameState(8, 50, True)
    assert (game.coords_conversion((game.BOARD_SIZE) / 2,
                                   (game.BOARD_SIZE) / 2) == [7, 7])


def test_check_if_selection_in_moves():
    moves = [Move([0, 0], [1, 1], False)]
    game = GameState(8, 50, True)
    assert (game.check_if_selection_in_moves(0, 0, 1, 1, moves))
    assert not (game.check_if_selection_in_moves(1, 0, 1, 1, moves))


def test_get_current_move():
    moves = [Move([0, 0], [1, 1], False)]
    game = GameState(8, 50, True)
    assert (isinstance(game.get_current_move(0, 0, 1, 1, moves), Move))


def test_check_for_captures():
    # Black capture
    game = GameState(8, 50, True)
    game.setup_board()
    game.create_board()
    # move red piece into position to be captured
    move = Move([2, 5], [2, 3], False)
    game.move_piece(move)
    game.player_turn = 1
    pieces = game.get_player_pieces()
    moves = game.get_valid_moves(pieces)
    assert (game.check_for_captures([1, 2]))

    # Red Capture
    game = GameState(8, 50, True)
    game.setup_board()
    game.create_board()
    # move red piece into position to be captured
    move = Move([1, 2], [1, 4], False)
    game.move_piece(move)
    game.player_turn = 2
    pieces = game.get_player_pieces()
    moves = game.get_valid_moves(pieces)
    assert (game.check_for_captures([0, 5]))
