import unittest
from board import Board, Tile
from solver_engine import Solver
from wordset_trie import load_dictionary

class TestScrabbleSolver(unittest.TestCase):
    def setUp(self):
        self.trie = load_dictionary("wordset.txt")
        self.board = Board()

    def place_word(self, word, row, col, direction):
        for i, ch in enumerate(word):
            r, c = (row, col + i) if direction == 'right' else (row + i, col)
            self.board.board[r][c] = Tile(ch)

    def run_solver(self, rack):
        self.board.find_anchors()
        self.board.print_board()
        solver = Solver(self.board.board, self.trie, rack, self.board.anchors)
        return solver.generate_best_move(self.trie, self.board.board, rack)

    def test_simple_horizontal_word(self):
        rack = ['H', 'E', 'L', 'L', 'O', '_', '_']
        move = self.run_solver(rack)
        print(move)
        # self.assertIsNotNone(move)
        # self.assertIn(move['word'], ['HELLO', 'HOLE', 'HELL', 'OLE'])

    

if __name__ == '__main__':
    unittest.main()