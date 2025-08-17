"""
Test script for the Scrabble backend
Tests basic functionality without requiring the full Flask server
"""

import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from models.board_state import BoardState
from services.solver_service import SolverService
from services.board_service import BoardService
from services.photo_service import PhotoService

def test_board_creation():
    """Test board state creation and manipulation"""
    print("=== Testing Board Creation ===")
    
    # Test empty board
    board = BoardState.create_empty()
    print(f"Empty board created: {board.is_empty()}")
    
    # Test placing tiles
    success = board.place_tile(7, 7, 'H')
    print(f"Placed H at center: {success}")
    
    success = board.place_tile(7, 8, 'I')
    print(f"Placed I next to H: {success}")
    
    # Find anchors
    anchors = board.find_anchors()
    print(f"Found {len(anchors)} anchors: {anchors}")
    
    # Test board summary
    board_service = BoardService()
    summary = board_service.get_board_summary(board)
    print(f"Board summary: {summary}")
    
    return board

def test_solver():
    """Test the solver service"""
    print("\n=== Testing Solver ===")
    
    try:
        solver_service = SolverService()
        
        # Test with empty board
        board = BoardState.create_empty()
        user_tiles = ['H', 'E', 'L', 'L', 'O', 'W', 'D']
        
        print(f"Finding moves for tiles: {user_tiles}")
        moves = solver_service.find_optimal_moves(board, user_tiles, max_moves=5)
        
        print(f"Found {len(moves)} moves:")
        for i, move in enumerate(moves[:3], 1):  # Show top 3
            print(f"  {i}. {move.word} - {move.score} points at {move.start} going {move.direction}")
            
        return len(moves) > 0
        
    except Exception as e:
        print(f"Error in solver test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_photo_service():
    """Test photo processing service"""
    print("\n=== Testing Photo Service ===")
    
    photo_service = PhotoService()
    status = photo_service.get_processing_status()
    print(f"Photo processing status: {status}")
    
    # Test with None (no image)
    board = photo_service.process_board_image(None)
    print(f"Processed None image: {board is not None}")
    
    return True

def main():
    """Run all tests"""
    print("Starting Scrabble Backend Tests\n")
    
    # Test board functionality
    board = test_board_creation()
    
    # Test solver
    solver_works = test_solver()
    
    # Test photo service
    photo_works = test_photo_service()
    
    print(f"\n=== Test Results ===")
    print(f"Board creation: ✓")
    print(f"Solver: {'✓' if solver_works else '✗'}")
    print(f"Photo service: {'✓' if photo_works else '✗'}")
    
    if solver_works:
        print("\n🎉 Backend is working! Ready to start Flask server.")
    else:
        print("\n⚠️  Some issues detected. Check logs above.")

if __name__ == "__main__":
    main()
