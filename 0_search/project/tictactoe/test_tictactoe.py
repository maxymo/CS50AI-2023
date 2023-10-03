import unittest
import random

from tictactoe import player, actions, result, winner, terminal, utility, minimax

X = "X"
O = "O"
EMPTY = None

class TestPlayer(unittest.TestCase):

    def test_empty_board_turn_for_X(self):
        board = [[EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(player(board), 'X')

    def test_board_with_1_X_return_O(self):
        board = [[EMPTY, EMPTY, EMPTY],
                [EMPTY, X, EMPTY],
                [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(player(board), 'O')

    def test_board_with_1_X_and_1_O_return_X(self):
        board = [[EMPTY, EMPTY, O],
                [EMPTY, X, EMPTY],
                [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(player(board), 'X')

class TestActions(unittest.TestCase):

    def test_empty_board_returns_all_9_actions(self):
        board = [[EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY]]
        possible_actions = actions(board)
        self.assertEqual(len(possible_actions), 9)
        assert (0,0) in possible_actions
        assert (0,1) in possible_actions
        assert (0,2) in possible_actions
        assert (1,0) in possible_actions
        assert (1,1) in possible_actions
        assert (1,2) in possible_actions
        assert (2,0) in possible_actions
        assert (2,1) in possible_actions
        assert (2,2) in possible_actions

    def test_full_boars_returns_empty(self):
        board = [[X, O, X],
                [X, X, O],
                [O, O, X]]
        possible_actions = actions(board)
        self.assertEqual(len(possible_actions), 0)

class TestResult(unittest.TestCase):

    def test_returned_board_is_deepcopy(self):
        original_board = [[EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY]]
        new_board = result(original_board, (0,0))
        new_board[2][2] = X
        self.assertNotEqual(original_board[2][2], new_board[2][2])

    def test_first_move_on_empty_board(self):
        original_board = [[EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY]]
        expected_board = [[EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, X]]
        new_board = result(original_board, (2,2))
        self.assertEqual(new_board, expected_board)

    def test_second_move(self):
        original_board = [[EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, X]]
        expected_board = [[EMPTY, EMPTY, EMPTY],
                [EMPTY, O, EMPTY],
                [EMPTY, EMPTY, X]]
        new_board = result(original_board, (1,1))
        self.assertEqual(new_board, expected_board)

class TestWinner(unittest.TestCase):

    def test_X_wins_return_X(self):
        board = [[X, O, O],
                [EMPTY, X, EMPTY],
                [EMPTY, EMPTY, X]]
        win_player = winner(board)
        self.assertEqual(win_player, 'X')

    def test_O_wins_return_O(self):
        board = [[O, EMPTY, EMPTY],
                [O, X, EMPTY],
                [O, EMPTY, X]]
        win_player = winner(board)
        self.assertEqual(win_player, 'O')

    def test_no_wineer_return_none(self):
        board = [[O, X, O],
                [O, X, X],
                [X, O, X]]
        win_player = winner(board)
        self.assertEqual(win_player, None)

class TestTerminal(unittest.TestCase):
    
    def test_winner_returns_true(self):
        board = [[X, O, O],
                [EMPTY, X, EMPTY],
                [EMPTY, EMPTY, X]]
        over = terminal(board)
        self.assertEqual(over, True)

    def test_full_board_returns_true(self):
        board = [[X, O, X],
                 [O, X, X],
                 [O, X, O]]
        over = terminal(board)
        self.assertEqual(over, True)

    def test_empty_board_returns_false(self):
        board = [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        over = terminal(board)
        self.assertEqual(over, False)

    def test_board_with_empty_cells_returns_false(self):
        board = [[X, EMPTY, EMPTY],
                 [EMPTY, O, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]
        over = terminal(board)
        self.assertEqual(over, False)

class TestUtility(unittest.TestCase):

    def test_X_wins_returns_1(self):
        board = [[X, O, O],
                [EMPTY, X, EMPTY],
                [EMPTY, EMPTY, X]]
        result = utility(board)
        self.assertEqual(result, 1)

    def test_O_wins_returns_minus1(self):
        board = [[X, O, O],
                [X, X, O],
                [EMPTY, X, O]]
        result = utility(board)
        self.assertEqual(result, -1)

    def test_no_winner_returns_0(self):
        board = [[X, O, O],
                 [O, X, X],
                 [X, X, O]]
        result = utility(board)
        self.assertEqual(result, 0)


class TestMinimax(unittest.TestCase):

    def test_terminal_board_returns_none(self):
        board = [[X, O, O],
                 [O, X, X],
                 [X, X, O]]
        move = minimax(board)
        self.assertIsNone(move)

if __name__ == '__main__':
    unittest.main()