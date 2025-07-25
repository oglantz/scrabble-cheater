from board import *
from solver_engine import *
from wordset_trie import *



# def main():
#     # Load the dictionary into a Trie
#     trie = load_dictionary('wordset.txt')

#     # Initialize the board
#     board = Board()

#     # Example rack
#     rack = ['S', 'O', 'L', 'V', 'E', '_', '_']

#     # Find anchors on the board
#     board.find_anchors()

#     # Generate best moves based on the current board and rack
#     solver = Solver(board.board, trie, rack, board.anchors)
#     best_move = solver.generate_best_move(trie, board.board, rack)

#     # Print the best move found
    
#     print(f"Word: {best_move['word']},\nScore: {best_move['score']},\nTiles: {best_move['tiles']}")


def main():
    # Load the dictionary into a Trie
    trie = load_dictionary('wordset.txt')

    # Initialize the board
    board = Board()

    # Example rack
    rack = ['P', 'A', 'S', 'S', 'E', '_', '_']

    # Find anchors on the board
    board.find_anchors()

    # Generate best moves based on the current board and rack
    solver = Solver(board.board, trie, rack, board.anchors)

    temp = [Tile('A', 'DW', False))]
    best_move = solver.generate_best_move(trie, board.board, rack)

    # Print the best move found
    
    print(f"Word: {best_move['word']},\nScore: {best_move['score']},\nTiles: {best_move['tiles']}")

if __name__ == "__main__":
    main()