"""
Basic unittest scaffold for quickly exercising the legacy solver.

These tests are intentionally lightweight and geared toward manual inspection
and iteration during early development.
"""

import unittest
from board import Board, Tile
from solver_engine import Solver
from wordset_trie import load_dictionary

class TestScrabbleSolver(unittest.TestCase):
    def setUp(self):
        """Create a fresh board and dictionary for each test."""
        self.trie = load_dictionary("wordset.txt")
        self.board = Board()

    def place_word(self, word, row, col, direction):
        """Helper to stamp a fixed word on the board without validation."""
        for i, ch in enumerate(word):
            r, c = (row, col + i) if direction == 'right' else (row + i, col)
            self.board.board[r][c] = Tile(ch)

    def run_solver(self, rack):
        """Run the solver using current board and return the best move dict."""
        self.board.find_anchors()
        self.board.print_board()
        solver = Solver(self.board.board, self.trie, rack, self.board.anchors)
        return solver.generate_best_move(self.trie, self.board.board, rack)

    def test_simple_horizontal_word(self):
        """Ensure solver returns a move for a simple rack on empty board."""
        rack = ['H', 'E', 'L', 'L', 'O', '_', '_']
        move = self.run_solver(rack)
        print(move)
        # self.assertIsNotNone(move)
        # self.assertIn(move['word'], ['HELLO', 'HOLE', 'HELL', 'OLE'])

    

if __name__ == '__main__':
    unittest.main()