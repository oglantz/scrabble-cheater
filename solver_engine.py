from wordset_trie import Trie
from board import Tile, BOARD_SIZE

class Solver:
    def __init__(self, board:list[list[Tile]], wordset:Trie, rack, anchors:set):
        self.board = board
        self.wordset = wordset
        self.rack = rack
        self.anchors = anchors
        self.letter_values = {
            'A':1, 'B':3, 'C':3, 'D':2, 'E':1, 'F':4, 'G':2, 'H':4,
            'I':1, 'J':8, 'K':5, 'L':1, 'M':3, 'N':1, 'O':1, 'P':3,
            'Q':10, 'R':1, 'S':1, 'T':1, 'U':1, 'V':4, 'W':4, 'X':8,
            'Y':4, 'Z':10
            }
    
    def build_word(self, board, rack, row, col, prefix, placed, results, direction):
        if row >= BOARD_SIZE or col >= BOARD_SIZE:
            return

        tile = board[row][col]
        is_empty = tile.letter is None

        if not is_empty:
            new_prefix = prefix + tile.letter
            if self.wordset.starts_with(new_prefix):
                next_row = row + 1 if direction == 'down' else row
                next_col = col + 1 if direction == 'right' else col
                self.build_word(board, rack, next_row, next_col,
                        new_prefix, placed, results, direction)
            return

        for i, letter in enumerate(rack):
            remaining_rack = rack[:i] + rack[i+1:]
            is_blank = letter == '_'
            for actual_letter in ([letter] if not is_blank else [chr(c) for c in range(ord('A'), ord('Z')+1)]):
                new_prefix = prefix + actual_letter
                if not self.wordset.starts_with(new_prefix):
                    continue

                board[row][col] = Tile(actual_letter, tile.premium, is_blank)
                placed.append((row, col, actual_letter, is_blank))
                
                if self.wordset.is_word(new_prefix):
                    results.append((new_prefix, placed.copy()))

                next_row = row + 1 if direction == 'down' else row
                next_col = col + 1 if direction == 'right' else col
                self.build_word(board, remaining_rack, next_row, next_col,
                        new_prefix, placed, results, direction)

                board[row][col] = Tile(None, tile.premium)
                placed.pop()

    def score_placement(self, word, placed):
        word_multiplier = 1
        score = 0

        for (r, c, letter, is_blank) in placed:
            value = 0 if is_blank else self.letter_values[letter]
            premium = self.board[r][c].premium

            if premium == 'DL':
                score += value * 2
            elif premium == 'TL':
                score += value * 3
            else:
                score += value

            if premium == 'DW':
                word_multiplier *= 2
            elif premium == 'TW':
                word_multiplier *= 3

        total = score * word_multiplier

        # 50-point bingo bonus
        if len(placed) == 7:
            total += 50

        return total

    def generate_best_move(self, trie, board, rack):
        all_moves = []

        for (row, col) in self.anchors:
            for direction in ['right', 'down']:
                results = []
                max_offset = 7  # Scrabble limit for prefix length

                for offset in range(max_offset + 1):
                    r = row - offset if direction == 'down' else row
                    c = col - offset if direction == 'right' else col

                    if 0 <= r < 15 and 0 <= c < 15:
                        self.build_word(board, rack, r, c, '', [], results, direction)

                for word, placed in results:
                    score = self.score_placement(word, placed)
                    all_moves.append({
                        'word': word,
                        'tiles': placed,
                        'score': score,
                        'direction': direction,
                        'start': (placed[0][0], placed[0][1]) if placed else (row, col)
                    })

        # Sort moves by score descending
        all_moves.sort(key=lambda x: x['score'], reverse=True)

        return all_moves[0] if all_moves else None  # Best move

