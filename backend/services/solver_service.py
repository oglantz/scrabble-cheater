"""
Solver Service
Finds optimal Scrabble moves by orchestrating board conversion, wordset access,
and the enhanced solver implementation. Provides a clean service API for views.
"""

import logging
from typing import List, Dict, Any
from models.board_state import BoardState
from models.move import Move
from core.enhanced_solver import EnhancedSolver
from core.wordset_loader import load_dictionary

logger = logging.getLogger(__name__)

class SolverService:
    """Service for finding optimal Scrabble moves."""
    
    def __init__(self):
        self.wordset = None
        self._load_wordset()
    
    def _load_wordset(self):
        """Load the dictionary/wordset into memory for fast lookups."""
        try:
            self.wordset = load_dictionary('wordset.txt')
            logger.info("Wordset loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load wordset: {e}")
            # For development, create a small test wordset
            self._create_test_wordset()
    
    def _create_test_wordset(self):
        """Create a minimal wordset for testing when main wordset is unavailable."""
        from core.wordset_trie import Trie
        
        logger.warning("Creating test wordset - limited functionality")
        self.wordset = Trie()
        
        # Add some common test words
        test_words = [
            'HELLO', 'WORLD', 'TEST', 'WORD', 'PLAY', 'GAME', 'SCORE',
            'TILES', 'BOARD', 'MOVE', 'BEST', 'FIND', 'OPTIMAL', 'SEARCH',
            'CAT', 'DOG', 'HOUSE', 'TREE', 'BOOK', 'WATER', 'LIGHT',
            'A', 'I', 'AM', 'IS', 'THE', 'AND', 'OR', 'BUT', 'FOR',
            'HE', 'SHE', 'IT', 'WE', 'THEY', 'GO', 'DO', 'BE', 'HAVE'
        ]
        
        for word in test_words:
            self.wordset.insert(word.upper())
    
    def find_optimal_moves(self, board_state: BoardState, user_tiles: List[str], 
                          max_moves: int = 10) -> List[Move]:
        """
        Find the best possible moves for given board state and tiles.
        
        Args:
            board_state: Current board state
            user_tiles: List of available tiles (A-Z, _ for blanks)
            max_moves: Maximum number of moves to return
            
        Returns:
            List of Move objects sorted by score (highest first)
        """
        try:
            if not self.wordset:
                logger.error("Wordset not available")
                return []
            
            if not user_tiles:
                logger.warning("No user tiles provided")
                return []
            
            # Convert to format expected by existing solver
            legacy_board = board_state.get_legacy_board()
            anchors = board_state.find_anchors()
            
            logger.info(f"Finding moves for tiles: {user_tiles}")
            logger.info(f"Board anchors: {anchors}")
            
            # Use enhanced solver
            solver = EnhancedSolver(legacy_board, self.wordset, user_tiles, anchors)
            
            # Generate moves
            best_moves = solver.generate_best_moves(max_moves)
            
            # Convert to Move objects
            moves = []
            for move_data in best_moves:
                if move_data and 'word' in move_data:
                    move = Move.from_legacy(move_data)
                    moves.append(move)
            
            logger.info(f"Found {len(moves)} valid moves")
            return moves
            
        except Exception as e:
            logger.error(f"Error finding optimal moves: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return []
    
    def validate_move(self, board_state: BoardState, move: Move) -> bool:
        """
        Validate that a move is legal on the given board.
        
        Args:
            board_state: Current board state
            move: Move to validate
            
        Returns:
            True if move is valid, False otherwise
        """
        try:
            # Check if positions are empty
            for row, col, letter, is_blank in move.tiles:
                if not board_state._is_valid_position(row, col):
                    return False
                
                tile = board_state.get_tile(row, col)
                if tile and not tile.is_empty():
                    return False
            
            # Additional validation could be added here
            # (word validity, connectivity, etc.)
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating move: {e}")
            return False
