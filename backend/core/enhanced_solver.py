"""
Enhanced Solver
Improved version of your existing solver_engine.py with better performance and API
"""

import logging
from typing import List, Dict, Any, Tuple, Set
from core.wordset_trie import Trie
from models.legacy_tile import LegacyTile

logger = logging.getLogger(__name__)

class EnhancedSolver:
    """Enhanced Scrabble move solver with improved performance and features"""
    
    BOARD_SIZE = 15
    
    def __init__(self, board: List[List[LegacyTile]], wordset: Trie, 
                 rack: List[str], anchors: Set[Tuple[int, int]]):
        self.board = board
        self.wordset = wordset
        self.rack = rack
        self.anchors = anchors
        
        # Scrabble letter values
        self.letter_values = {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
            'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
            'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
            'Y': 4, 'Z': 10
        }
        self.center = (7, 7)
    
    def generate_best_moves(self, max_moves: int = 10) -> List[Dict[str, Any]]:
        """
        Generate the best possible moves
        
        Args:
            max_moves: Maximum number of moves to return
            
        Returns:
            List of move dictionaries sorted by score
        """
        try:
            logger.info(f"Generating moves for rack: {self.rack}")
            logger.info(f"Anchors: {self.anchors}")
            
            all_moves = []
            
            # Generate moves for each anchor position
            for anchor_row, anchor_col in self.anchors:
                logger.debug(f"Processing anchor: ({anchor_row}, {anchor_col})")
                
                for direction in ['right', 'down']:
                    moves = self._generate_moves_from_anchor(anchor_row, anchor_col, direction)
                    all_moves.extend(moves)
            
            # Sort by score and return top moves
            all_moves.sort(key=lambda x: x['score'], reverse=True)
            
            # Remove duplicates and limit results
            unique_moves = []
            seen_moves = set()
            
            for move in all_moves:
                move_key = (move['word'], tuple(move['tiles']), move['direction'])
                if move_key not in seen_moves:
                    seen_moves.add(move_key)
                    unique_moves.append(move)
                    
                    if len(unique_moves) >= max_moves:
                        break
            
            logger.info(f"Generated {len(unique_moves)} unique moves")
            return unique_moves
            
        except Exception as e:
            logger.error(f"Error generating moves: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return []
    
    def _generate_moves_from_anchor(self, anchor_row: int, anchor_col: int, 
                                   direction: str) -> List[Dict[str, Any]]:
        """Generate moves starting from a specific anchor position"""
        moves = []
        max_offset = min(7, len(self.rack))  # Reasonable search limit
        
        try:
            for offset in range(max_offset + 1):
                if direction == 'right':
                    start_row = anchor_row
                    start_col = max(0, anchor_col - offset)
                else:  # down
                    start_row = max(0, anchor_row - offset)
                    start_col = anchor_col
                
                if self._is_valid_position(start_row, start_col):
                    anchor_moves = self._build_words_from_position(
                        start_row, start_col, direction
                    )
                    moves.extend(anchor_moves)
            
        except Exception as e:
            logger.error(f"Error generating moves from anchor ({anchor_row}, {anchor_col}): {e}")
        
        return moves
    
    def _build_words_from_position(self, start_row: int, start_col: int, 
                                  direction: str) -> List[Dict[str, Any]]:
        """Build words starting from a specific position"""
        results = []
        
        try:
            self._build_word_recursive(
                start_row, start_col, direction, '', [], self.rack.copy(), results
            )
        except Exception as e:
            logger.error(f"Error building words from ({start_row}, {start_col}): {e}")
        
        return results
    
    def _build_word_recursive(self, row: int, col: int, direction: str, 
                            prefix: str, placed: List[Tuple], remaining_rack: List[str], 
                            results: List[Dict]):
        """Recursively build words by placing tiles"""
        
        # Boundary check
        if not self._is_valid_position(row, col):
            return
        
        tile = self.board[row][col]
        
        # If position is occupied, must use existing tile
        if tile.letter is not None:
            new_prefix = prefix + tile.letter
            if self.wordset.starts_with(new_prefix):
                next_row = row + (1 if direction == 'down' else 0)
                next_col = col + (1 if direction == 'right' else 0)
                
                self._build_word_recursive(
                    next_row, next_col, direction, new_prefix, 
                    placed, remaining_rack, results
                )
            return
        
        # Try placing each available tile
        for i, rack_tile in enumerate(remaining_rack):
            new_remaining = remaining_rack[:i] + remaining_rack[i+1:]
            is_blank = rack_tile == '_'
            
            # For blank tiles, try all letters
            letters_to_try = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
                             'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
                             'U', 'V', 'W', 'X', 'Y', 'Z'] if is_blank else [rack_tile]
            
            for letter in letters_to_try:
                new_prefix = prefix + letter
                
                # Check if this prefix could lead to a valid word
                if not self.wordset.starts_with(new_prefix):
                    continue
                
                # Validate perpendicular cross-word formed by this placement
                if not self._validate_perpendicular_at(row, col, letter, direction):
                    continue
                
                # Place tile temporarily
                new_placed = placed + [(row, col, letter, is_blank)]
                
                # Check if current prefix is a valid word
                if len(new_prefix) > 1 and self.wordset.is_word(new_prefix):
                    move = self._create_move(new_prefix, new_placed, direction)
                    if move and self._is_valid_move(move):
                        results.append(move)
                
                # Continue building if we have more tiles and space
                if new_remaining and len(new_prefix) < 15:
                    next_row = row + (1 if direction == 'down' else 0)
                    next_col = col + (1 if direction == 'right' else 0)
                    
                    self._build_word_recursive(
                        next_row, next_col, direction, new_prefix,
                        new_placed, new_remaining, results
                    )
    
    def _create_move(self, word: str, placed: List[Tuple], direction: str) -> Dict[str, Any]:
        """Create a move dictionary from word and placement info"""
        try:
            if not placed:
                return None
            
            # Build the full main word as it will appear on the board, including
            # any pre-existing adjacent letters. If the contiguous path does not
            # actually cover all placed tiles, treat as invalid.
            full_word, covers_all = self._build_main_word(placed, direction)
            if not covers_all:
                return None

            # Calculate score
            score, score_breakdown = self._calculate_score(word, placed, direction)
            if score <= 0:
                return None
            
            return {
                'word': full_word or word,
                'score': score,
                'tiles': placed,
                'direction': direction,
                'start': (placed[0][0], placed[0][1]),
                'score_breakdown': score_breakdown
            }
            
        except Exception as e:
            logger.error(f"Error creating move: {e}")
            return None
    
    def _calculate_score(self, word: str, placed: List[Tuple], direction: str) -> Tuple[int, Dict[str, Any]]:
        """Calculate the score for a word placement and return detailed breakdown.

        Includes existing letters in the main word span at face value (no premiums),
        applies letter multipliers only to newly placed tiles, and applies word
        multipliers from newly placed tiles landing on DW/TW.
        """
        try:
            from models.move import TileScore, ScoreBreakdown

            # Map of newly placed tiles for fast lookup
            placed_map: Dict[Tuple[int, int], Tuple[str, bool]] = {
                (r, c): (ch, is_blank) for r, c, ch, is_blank in placed
            }

            # Determine iteration vectors
            if direction == 'right':
                dr_back, dc_back = 0, -1
                dr_fwd, dc_fwd = 0, 1
                seed_row, seed_col = min(((r, c) for r, c, _, _ in placed), key=lambda t: t[1])
            else:  # down
                dr_back, dc_back = -1, 0
                dr_fwd, dc_fwd = 1, 0
                seed_row, seed_col = min(((r, c) for r, c, _, _ in placed), key=lambda t: t[0])

            # Walk backwards to start of contiguous main word (consume existing letters)
            r, c = seed_row, seed_col
            while self._is_valid_position(r + dr_back, c + dc_back) and self.board[r + dr_back][c + dc_back].letter is not None:
                r += dr_back
                c += dc_back

            word_multiplier = 1
            tile_scores: List[TileScore] = []
            base_word_score = 0

            # Iterate forward across the contiguous main word
            steps = 0
            while self._is_valid_position(r, c) and steps < self.BOARD_SIZE:
                steps += 1

                is_newly_placed = (r, c) in placed_map
                if self.board[r][c].letter is not None and not is_newly_placed:
                    # Existing board tile
                    letter = self.board[r][c].letter
                    is_blank = self.board[r][c].is_blank
                    premium = None  # premiums do not apply to pre-existing tiles
                elif is_newly_placed:
                    # Newly placed tile
                    letter, is_blank = placed_map[(r, c)]
                    tile = self.board[r][c]
                    premium = tile.premium if tile.letter is None else None
                else:
                    # Neither existing letter nor newly placed; end of word span
                    break

                # Base letter value
                letter_value = 0 if is_blank else self.letter_values.get(letter, 0)

                # Apply letter multipliers only for newly-placed tiles
                premium_multiplier = 1
                if is_newly_placed:
                    if premium == 'DL':
                        premium_multiplier = 2
                    elif premium == 'TL':
                        premium_multiplier = 3

                    # Track word multipliers from newly placed tiles
                    if premium == 'DW':
                        word_multiplier *= 2
                    elif premium == 'TW':
                        word_multiplier *= 3

                tile_total = letter_value * premium_multiplier
                base_word_score += tile_total

                # Record tile score entry (show premium badge only for new tiles)
                tile_scores.append(
                    TileScore(
                        letter=letter,
                        base_value=letter_value,
                        premium_multiplier=premium_multiplier,
                        final_value=tile_total,
                        premium_type=premium if is_newly_placed else None,
                        position=(r, c),
                        is_blank=is_blank,
                    )
                )

                # Advance to next cell if it continues the word span
                nr, nc = r + dr_fwd, c + dc_fwd
                if not self._is_valid_position(nr, nc):
                    break
                if self.board[nr][nc].letter is None and (nr, nc) not in placed_map:
                    # Next is empty and not part of placement → end of word
                    break
                r, c = nr, nc

            # Apply word multiplier to the main word total
            final_word_score = base_word_score * word_multiplier

            # Calculate cross words created by each newly-placed tile
            cross_words_total = 0
            cross_words_details: List[Dict[str, Any]] = []

            # Helper to score a single cross word given origin (r,c)
            def _score_cross_word_at(r: int, c: int) -> Tuple[int, List[TileScore], str]:
                # Determine perpendicular direction
                if direction == 'right':
                    dr_back, dc_back = -1, 0
                    dr_fwd, dc_fwd = 1, 0
                else:
                    dr_back, dc_back = 0, -1
                    dr_fwd, dc_fwd = 0, 1

                # Walk to start of cross word
                sr, sc = r, c
                while self._is_valid_position(sr + dr_back, sc + dc_back) and self.board[sr + dr_back][sc + dc_back].letter is not None:
                    sr += dr_back
                    sc += dc_back

                # Build and score cross word; premiums apply only to the placed tile at (r,c)
                cw_chars = []
                cw_tile_scores: List[TileScore] = []
                cw_base = 0
                cur_r, cur_c = sr, sc
                while self._is_valid_position(cur_r, cur_c):
                    is_new = (cur_r, cur_c) in placed_map
                    if self.board[cur_r][cur_c].letter is not None and not is_new:
                        ch = self.board[cur_r][cur_c].letter
                        is_blank = self.board[cur_r][cur_c].is_blank
                        premium = None
                    elif is_new:
                        ch, is_blank = placed_map[(cur_r, cur_c)]
                        tile = self.board[cur_r][cur_c]
                        # Only the newly placed tile may receive premium multipliers
                        premium = tile.premium if tile.letter is None and (cur_r == r and cur_c == c) else None
                    else:
                        break

                    cw_chars.append(ch)
                    val = 0 if is_blank else self.letter_values.get(ch, 0)
                    mult = 1
                    if is_new and cur_r == r and cur_c == c:
                        if premium == 'DL':
                            mult = 2
                        elif premium == 'TL':
                            mult = 3
                    # Note: DW/TW do NOT apply to cross words (only to main word)
                    tile_total = val * mult
                    cw_base += tile_total
                    cw_tile_scores.append(
                        TileScore(
                            letter=ch,
                            base_value=val,
                            premium_multiplier=mult,
                            final_value=tile_total,
                            premium_type=premium if (is_new and cur_r == r and cur_c == c) else None,
                            position=(cur_r, cur_c),
                            is_blank=is_blank,
                        )
                    )

                    nr, nc = cur_r + dr_fwd, cur_c + dc_fwd
                    if not self._is_valid_position(nr, nc):
                        break
                    if self.board[nr][nc].letter is None and (nr, nc) not in placed_map:
                        break
                    cur_r, cur_c = nr, nc

                cw_word = ''.join(cw_chars)
                if len(cw_word) <= 1:
                    return 0, [], ''
                return cw_base, cw_tile_scores, cw_word

            for pr, pc, _, _ in placed:
                cw_score, cw_tiles, cw_word = _score_cross_word_at(pr, pc)
                if cw_score > 0 and cw_word and self.wordset.is_word(cw_word):
                    cross_words_total += cw_score
                    cross_words_details.append({
                        'word': cw_word,
                        'score': cw_score,
                        'tile_scores': cw_tiles,
                        'origin': (pr, pc)
                    })

            # Bingo bonus for using all 7 tiles from rack
            bingo_bonus = 50 if len(placed) == 7 else 0
            total_score = final_word_score + cross_words_total + bingo_bonus

            score_breakdown = ScoreBreakdown(
                tile_scores=tile_scores,
                word_multiplier=word_multiplier,
                base_word_score=base_word_score,
                final_word_score=final_word_score,
                bingo_bonus=bingo_bonus,
                cross_words_total=cross_words_total,
                cross_words=cross_words_details,
                total_score=total_score,
            )

            return total_score, score_breakdown

        except Exception as e:
            logger.error(f"Error calculating score: {e}")
            return 0, None
    
    def _is_valid_move(self, move: Dict[str, Any]) -> bool:
        """Validate that a move is legal"""
        try:
            placed = move['tiles']
            
            # Must place at least one tile
            if not placed:
                return False
            
            # Check center placement for first move
            if self._is_empty_board():
                center_covered = any(row == 7 and col == 7 for row, col, _, _ in placed)
                if not center_covered:
                    return False
            else:
                # Must connect to existing tiles (simplified check)
                connects = False
                for row, col, _, _ in placed:
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = row + dr, col + dc
                        if (self._is_valid_position(nr, nc) and 
                            self.board[nr][nc].letter is not None):
                            connects = True
                            break
                    if connects:
                        break
                
                if not connects:
                    return False
            
            # Validate the full main word created by this placement
            main_word, covers_all = self._build_main_word(placed, move['direction'])
            if not covers_all:
                return False
            if len(main_word) > 1 and not self.wordset.is_word(main_word):
                return False

            # All perpendicular cross-words created must be valid
            if not self._are_all_cross_words_valid(placed, move['direction']):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating move: {e}")
            return False
    
    def _is_empty_board(self) -> bool:
        """Check if the board is empty"""
        for row in self.board:
            for tile in row:
                if tile.letter is not None:
                    return False
        return True
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board bounds"""
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE

    def _validate_perpendicular_at(self, row: int, col: int, letter: str, direction: str) -> bool:
        """Validate the perpendicular (cross) word formed by placing a letter at (row,col).
        Returns True if either no cross word is formed (length == 1) or the formed
        word exists in the dictionary.
        """
        try:
            word = self._build_perpendicular_word(row, col, letter, direction)
            if len(word) <= 1:
                return True
            return self.wordset.is_word(word)
        except Exception:
            return False

    def _build_perpendicular_word(self, row: int, col: int, letter: str, direction: str) -> str:
        """Construct the perpendicular word string formed at placement (row,col)."""
        if direction == 'right':
            dr_back, dc_back = -1, 0  # move up
            dr_fwd, dc_fwd = 1, 0     # move down
        else:  # down
            dr_back, dc_back = 0, -1  # move left
            dr_fwd, dc_fwd = 0, 1     # move right

        # Move backwards to the start of the perpendicular word
        r, c = row, col
        while self._is_valid_position(r + dr_back, c + dc_back) and self.board[r + dr_back][c + dc_back].letter is not None:
            r += dr_back
            c += dc_back

        # Build the word from start to end, inserting the new letter at (row,col)
        chars = []
        cur_r, cur_c = r, c
        while self._is_valid_position(cur_r, cur_c):
            if cur_r == row and cur_c == col:
                chars.append(letter)
            else:
                existing = self.board[cur_r][cur_c].letter
                if existing is None:
                    break
                chars.append(existing)
            cur_r += dr_fwd
            cur_c += dc_fwd

        return ''.join(chars)

    def _are_all_cross_words_valid(self, placed: List[Tuple[int, int, str, bool]], direction: str) -> bool:
        """Check that for each placed tile, its perpendicular word is valid (if length > 1)."""
        for row, col, letter, _ in placed:
            if not self._validate_perpendicular_at(row, col, letter, direction):
                return False
        return True

    def _build_main_word(self, placed: List[Tuple[int, int, str, bool]], direction: str) -> Tuple[str, bool]:
        """Construct the full main word along `direction` including adjacent
        existing letters. Also verify that the contiguous path covers every
        placed tile position. Returns (word, covers_all_placed).

        This prevents illegal attachments such as placing 'PILFERS' beneath an
        existing 'H' to form 'HPILFERS' unless that full word is valid.
        """
        if not placed:
            return '', False

        placed_map = {(r, c): ch for r, c, ch, _ in placed}

        if direction == 'right':
            dr_back, dc_back = 0, -1
            dr_fwd, dc_fwd = 0, 1
            seed_row, seed_col = min(((r, c) for r, c, _, _ in placed), key=lambda t: t[1])
        else:  # down
            dr_back, dc_back = -1, 0
            dr_fwd, dc_fwd = 1, 0
            seed_row, seed_col = min(((r, c) for r, c, _, _ in placed), key=lambda t: t[0])

        # Extend backwards to the start of the contiguous word by consuming existing tiles
        r, c = seed_row, seed_col
        while self._is_valid_position(r + dr_back, c + dc_back) and self.board[r + dr_back][c + dc_back].letter is not None:
            r += dr_back
            c += dc_back

        # Walk forward building the contiguous word
        chars = []
        visited_placed = set()
        steps = 0
        while self._is_valid_position(r, c) and steps < self.BOARD_SIZE:
            steps += 1
            if self.board[r][c].letter is not None:
                chars.append(self.board[r][c].letter)
            elif (r, c) in placed_map:
                chars.append(placed_map[(r, c)])
                visited_placed.add((r, c))
            else:
                break

            nr, nc = r + dr_fwd, c + dc_fwd
            if not self._is_valid_position(nr, nc):
                break
            if self.board[nr][nc].letter is None and (nr, nc) not in placed_map:
                # Next cell would be empty and not part of placement; word ends
                r, c = nr, nc
                break
            r, c = nr, nc

        covers_all = visited_placed == set((r, c) for r, c, _, _ in placed)
        return ''.join(chars), covers_all
