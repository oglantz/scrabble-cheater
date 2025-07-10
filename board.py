'''
Houses Scrabble Board class and related functions/objects.
'''
BOARD_SIZE = 15  # Standard Scrabble board size

class Tile:
    def __init__(self, letter=None, premium=None, is_blank=False):
        self.letter = letter  # E.g. 'A', 'B', None
        self.premium = premium  # E.g. 'TW', 'DL', None
        self.is_blank = is_blank  # If a blank tile was used

class Board:
    def __init__(self):
        self.premium_map = {
            # Triple Word (TW) - dark red
            (0, 0): 'TW', (0, 7): 'TW', (0, 14): 'TW',
            (7, 0): 'TW', (7, 14): 'TW',
            (14, 0): 'TW', (14, 7): 'TW', (14, 14): 'TW',

            # Double Word (DW) - light red
            (1, 1): 'DW', (2, 2): 'DW', (3, 3): 'DW', (4, 4): 'DW',
            (10, 10): 'DW', (11, 11): 'DW', (12, 12): 'DW', (13, 13): 'DW',
            (1, 13): 'DW', (2, 12): 'DW', (3, 11): 'DW', (4, 10): 'DW',
            (10, 4): 'DW', (11, 3): 'DW', (12, 2): 'DW', (13, 1): 'DW',
            (7, 7): 'DW',  # Center star tile

            # Triple Letter (TL) - dark blue
            (1, 5): 'TL', (1, 9): 'TL',
            (5, 1): 'TL', (5, 5): 'TL', (5, 9): 'TL', (5, 13): 'TL',
            (9, 1): 'TL', (9, 5): 'TL', (9, 9): 'TL', (9, 13): 'TL',
            (13, 5): 'TL', (13, 9): 'TL',

            # Double Letter (DL) - light blue
            (0, 3): 'DL', (0, 11): 'DL',
            (2, 6): 'DL', (2, 8): 'DL',
            (3, 0): 'DL', (3, 7): 'DL', (3, 14): 'DL',
            (6, 2): 'DL', (6, 6): 'DL', (6, 8): 'DL', (6, 12): 'DL',
            (7, 3): 'DL', (7, 11): 'DL',
            (8, 2): 'DL', (8, 6): 'DL', (8, 8): 'DL', (8, 12): 'DL',
            (11, 0): 'DL', (11, 7): 'DL', (11, 14): 'DL',
            (12, 6): 'DL', (12, 8): 'DL',
            (14, 3): 'DL', (14, 11): 'DL',
        }
        self.board = [[Tile() for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.__initBoard()
        self.anchors = set()
        

    def __initBoard(self):
        for (r, c), premium in self.premium_map.items():
            self.board[r][c].premium = premium
    
    def print_board(self):
        for r in range(BOARD_SIZE):
            print(' '.join(self.board[r][c].premium or '--' for c in range(BOARD_SIZE)))

    def find_anchors(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c].letter is not None:
                    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                            if self.board[nr][nc].letter is None:
                                self.anchors.add((nr, nc))
        # Special case: empty board, must place on center
        if not any(tile.letter for row in self.board for tile in row):
            self.anchors.add((7, 7))

