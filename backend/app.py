"""
Scrabble Cheater Flask Backend
Main application entry point with API endpoints.

Exposes endpoints for analyzing a Scrabble board state and returning optimal
moves given user-provided rack tiles. Can accept JSON (manual board) or
multipart form with an image (future CV support).
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import traceback
from typing import Dict, Any, List, Optional

from services.board_service import BoardService
from services.solver_service import SolverService
from services.photo_service import PhotoService
from models.board_state import BoardState
from utils.validators import validate_tiles, validate_board_state

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize services
board_service = BoardService()
solver_service = SolverService()
photo_service = PhotoService()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "scrabble-cheater-backend"})


@app.route('/api/analyze', methods=['POST'])
def analyze_board():
    """
    Main endpoint for analyzing Scrabble board and finding optimal moves
    
    Accepts either:
    1. Manual board state (JSON) + user tiles
    2. Board image + user tiles (for future photo processing)
    """
    try:
        # Extract user tiles from request
        user_tiles = None
        board_state = None
        
        if request.is_json:
            # Manual board state input (JSON)
            data = request.get_json()
            user_tiles = data.get('user_tiles', [])
            board_state_data = data.get('board_state', None)
            
            if board_state_data:
                board_state = BoardState.from_dict(board_state_data)
            else:
                # Create empty board for testing
                board_state = BoardState.create_empty()
                
        else:
            # Multipart form data (image + tiles)
            user_tiles_json = request.form.get('user_tiles')
            if user_tiles_json:
                import json
                user_tiles = json.loads(user_tiles_json)
            
            board_image = request.files.get('board_image')
            
            if board_image:
                # Process image to extract board state
                board_state = photo_service.process_board_image(board_image)
            else:
                # Create empty board for testing without image
                board_state = BoardState.create_empty()
        
        # Validate inputs
        if not user_tiles:
            return jsonify({"error": "user_tiles is required"}), 400
            
        validation_error = validate_tiles(user_tiles)
        if validation_error:
            return jsonify({"error": validation_error}), 400
            
        if not board_state:
            return jsonify({"error": "Could not determine board state"}), 400
            
        validation_error = validate_board_state(board_state)
        if validation_error:
            return jsonify({"error": validation_error}), 400
        
        logger.info(f"Analyzing board with tiles: {user_tiles}")
        
        # Find optimal moves
        moves = solver_service.find_optimal_moves(board_state, user_tiles)
        
        # Format response
        response = {
            "moves": [move.to_dict() for move in moves],
            "board_state": board_state.to_dict(),
            "user_tiles": user_tiles
        }
        
        logger.info(f"Found {len(moves)} possible moves")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error analyzing board: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/board/manual', methods=['POST'])
def set_manual_board():
    """
    Endpoint for manually setting up board state (for testing/development)
    """
    try:
        data = request.get_json()
        board_state = BoardState.from_dict(data)
        
        validation_error = validate_board_state(board_state)
        if validation_error:
            return jsonify({"error": validation_error}), 400
        
        return jsonify({
            "success": True,
            "board_state": board_state.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error setting manual board: {str(e)}")
        return jsonify({"error": "Invalid board state"}), 400


@app.route('/api/test/empty-board', methods=['POST'])
def test_empty_board():
    """
    Test endpoint for analyzing moves on an empty board
    Useful for development and testing
    """
    try:
        data = request.get_json()
        user_tiles = data.get('user_tiles', [])
        
        if not user_tiles:
            return jsonify({"error": "user_tiles is required"}), 400
            
        validation_error = validate_tiles(user_tiles)
        if validation_error:
            return jsonify({"error": validation_error}), 400
        
        # Create empty board
        board_state = BoardState.create_empty()
        
        # Find optimal moves
        moves = solver_service.find_optimal_moves(board_state, user_tiles)
        
        response = {
            "moves": [move.to_dict() for move in moves],
            "board_state": board_state.to_dict(),
            "user_tiles": user_tiles
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in test endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
