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
            
            # Calculate score
            score = self._calculate_score(word, placed, direction)
            if score <= 0:
                return None
            
            return {
                'word': word,
                'score': score,
                'tiles': placed,
                'direction': direction,
                'start': (placed[0][0], placed[0][1])
            }
            
        except Exception as e:
            logger.error(f"Error creating move: {e}")
            return None
    
    def _calculate_score(self, word: str, placed: List[Tuple], direction: str) -> int:
        """Calculate the score for a word placement"""
        try:
            # This is a simplified scoring - you can enhance based on your existing logic
            word_multiplier = 1
            score = 0
            
            for row, col, letter, is_blank in placed:
                # Base letter value
                letter_value = 0 if is_blank else self.letter_values.get(letter, 0)
                
                # Apply premium if tile is newly placed on premium square
                tile = self.board[row][col]
                premium = tile.premium if tile.letter is None else None
                
                tile_score = letter_value
                if premium == 'DL':
                    tile_score *= 2
                elif premium == 'TL':
                    tile_score *= 3
                elif premium == 'DW':
                    word_multiplier *= 2
                elif premium == 'TW':
                    word_multiplier *= 3
                
                score += tile_score
            
            # Apply word multiplier
            score *= word_multiplier
            
            # Bonus for using all 7 tiles
            if len(placed) == 7:
                score += 50
            
            return score
            
        except Exception as e:
            logger.error(f"Error calculating score: {e}")
            return 0
    
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
