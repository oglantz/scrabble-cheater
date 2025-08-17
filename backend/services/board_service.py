"""
Board Service
Handles board state management and manipulation
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from models.board_state import BoardState, BoardTile

logger = logging.getLogger(__name__)

class BoardService:
    """Service for managing board state"""
    
    def __init__(self):
        pass
    
    def create_empty_board(self) -> BoardState:
        """Create a new empty board"""
        return BoardState.create_empty()
    
    def create_test_board(self) -> BoardState:
        """Create a board with test data for development"""
        return BoardState.create_test_board()
    
    def validate_board_state(self, board_state: BoardState) -> Optional[str]:
        """
        Validate board state for consistency
        
        Returns:
            None if valid, error message string if invalid
        """
        try:
            # Check board dimensions
            if len(board_state.board) != BoardState.BOARD_SIZE:
                return "Invalid board height"
            
            for row in board_state.board:
                if len(row) != BoardState.BOARD_SIZE:
                    return "Invalid board width"
            
            # Validate tiles
            for r in range(BoardState.BOARD_SIZE):
                for c in range(BoardState.BOARD_SIZE):
                    tile = board_state.board[r][c]
                    
                    # Check letter validity
                    if tile.letter is not None:
                        if not isinstance(tile.letter, str) or len(tile.letter) != 1:
                            return f"Invalid letter at ({r}, {c}): {tile.letter}"
                        
                        if tile.letter not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                            return f"Invalid letter at ({r}, {c}): {tile.letter}"
                    
                    # Check premium validity
                    if tile.premium is not None:
                        if tile.premium not in ['TW', 'DW', 'TL', 'DL']:
                            return f"Invalid premium at ({r}, {c}): {tile.premium}"
            
            return None  # Valid
            
        except Exception as e:
            logger.error(f"Error validating board state: {e}")
            return f"Board validation error: {str(e)}"
    
    def place_word(self, board_state: BoardState, word: str, start_row: int, 
                   start_col: int, direction: str, tiles_from_rack: List[str]) -> bool:
        """
        Place a word on the board
        
        Args:
            board_state: Board to modify
            word: Word to place
            start_row: Starting row position
            start_col: Starting column position  
            direction: 'right' or 'down'
            tiles_from_rack: Which tiles come from user's rack (vs already on board)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if direction not in ['right', 'down']:
                return False
            
            # Validate positions
            positions = []
            for i, letter in enumerate(word):
                if direction == 'right':
                    row, col = start_row, start_col + i
                else:
                    row, col = start_row + i, start_col
                
                if not board_state._is_valid_position(row, col):
                    return False
                
                positions.append((row, col, letter))
            
            # Check if placement is valid (some tiles may already be on board)
            rack_index = 0
            for row, col, letter in positions:
                tile = board_state.get_tile(row, col)
                
                if tile.is_empty():
                    # Need to place from rack
                    if rack_index >= len(tiles_from_rack):
                        return False
                    
                    rack_tile = tiles_from_rack[rack_index]
                    is_blank = rack_tile == '_'
                    
                    if not is_blank and rack_tile.upper() != letter.upper():
                        return False
                    
                    board_state.place_tile(row, col, letter, is_blank, True)
                    rack_index += 1
                    
                elif tile.letter.upper() != letter.upper():
                    # Letter doesn't match existing tile
                    return False
            
            # Update anchors
            board_state.find_anchors()
            return True
            
        except Exception as e:
            logger.error(f"Error placing word: {e}")
            return False
    
    def get_board_summary(self, board_state: BoardState) -> Dict[str, Any]:
        """Get summary information about the board state"""
        try:
            total_tiles = 0
            filled_positions = []
            
            for r in range(BoardState.BOARD_SIZE):
                for c in range(BoardState.BOARD_SIZE):
                    tile = board_state.get_tile(r, c)
                    if not tile.is_empty():
                        total_tiles += 1
                        filled_positions.append({
                            "row": r,
                            "col": c,
                            "letter": tile.letter,
                            "is_blank": tile.is_blank,
                            "premium": tile.premium
                        })
            
            return {
                "total_tiles": total_tiles,
                "is_empty": board_state.is_empty(),
                "anchors": list(board_state.anchors),
                "filled_positions": filled_positions
            }
            
        except Exception as e:
            logger.error(f"Error getting board summary: {e}")
            return {"error": str(e)}
