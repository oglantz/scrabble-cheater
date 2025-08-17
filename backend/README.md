# Scrabble Cheater Backend

A Flask-based backend for the Scrabble Cheater application that finds optimal Scrabble moves.

## Features

- **RESTful API**: Clean endpoints for board analysis
- **Modular Architecture**: Separate services for different concerns
- **Photo Processing Ready**: Stub implementation ready for computer vision
- **Enhanced Solver**: Improved version of existing Scrabble solver
- **Flexible Board Input**: Supports manual board state or image upload
- **Comprehensive Validation**: Input validation and error handling

## Architecture

### Core Components

- **Flask App** (`app.py`): Main application with API endpoints
- **Models**: Data structures for board state, moves, and tiles
- **Services**: Business logic separated into focused services
  - `BoardService`: Board state management
  - `SolverService`: Move finding and optimization
  - `PhotoService`: Image processing (stub for future CV implementation)
- **Core Logic**: Enhanced versions of existing solver algorithms
- **Utilities**: Validation and helper functions

### Directory Structure

```
backend/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── wordset.txt          # Dictionary file
├── models/              # Data models
│   ├── board_state.py   # Board representation
│   ├── move.py          # Move representation
│   └── legacy_tile.py   # Compatibility with existing code
├── services/            # Business logic services
│   ├── board_service.py
│   ├── solver_service.py
│   └── photo_service.py
├── core/                # Core algorithms
│   ├── enhanced_solver.py
│   ├── wordset_trie.py
│   └── wordset_loader.py
└── utils/               # Utilities
    └── validators.py
```

## API Endpoints

### Health Check
```
GET /health
```
Returns server status.

### Analyze Board
```
POST /api/analyze
Content-Type: application/json
{
    "user_tiles": ["H", "E", "L", "L", "O", "W", "_"],
    "board_state": {...}  // Optional manual board state
}
```

Or with image upload:
```
POST /api/analyze
Content-Type: multipart/form-data
- board_image: Image file
- user_tiles: JSON array of tiles
```

Returns optimal moves with scores and placement instructions.

### Test Empty Board
```
POST /api/test/empty-board
{
    "user_tiles": ["H", "E", "L", "L", "O", "W", "_"]
}
```
Test endpoint for finding moves on an empty board.

## Installation

1. **Create Virtual Environment** (recommended):
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Test Backend**:
   ```bash
   python test_backend.py
   ```

4. **Start Development Server**:
   ```bash
   python app.py
   ```

The server will run on `http://localhost:5000`

## Configuration

Environment variables for customization:

- `DEBUG`: Enable debug mode (default: True)
- `SECRET_KEY`: Flask secret key
- `WORDSET_FILE`: Path to dictionary file (default: wordset.txt)
- `MAX_MOVES_RETURNED`: Maximum moves to return (default: 10)
- `ENABLE_PHOTO_PROCESSING`: Enable CV processing (default: False)
- `CORS_ORIGINS`: Allowed CORS origins (default: http://localhost:3000)

## Photo Processing

The photo service is designed with a modular interface for future computer vision implementation:

### Current State
- Accepts image uploads
- Validates file types and sizes
- Returns test/empty board for development
- Ready for CV integration

### Future Implementation
The `PhotoService._extract_board_state_cv()` method is a placeholder for:

1. **Image Preprocessing**: Perspective correction, noise reduction
2. **Board Detection**: Identify board boundaries and grid
3. **Square Extraction**: Extract individual board squares
4. **Letter Recognition**: OCR or CNN-based letter detection
5. **Premium Square Detection**: Color-based premium square identification
6. **Board State Construction**: Build `BoardState` object from detected tiles

### Integration Points
```python
# When CV is ready, simply:
photo_service.enable_vision_processing()

# The API will automatically use CV processing for uploaded images
```

## Solver Engine

The enhanced solver builds upon your existing code with improvements:

### Features
- **Better Performance**: Optimized search algorithms
- **Flexible Input**: Works with new board state system
- **Comprehensive Scoring**: Handles all Scrabble scoring rules
- **Move Validation**: Ensures legal moves only
- **Multiple Move Generation**: Returns top N moves

### Algorithm
1. **Anchor Detection**: Find positions adjacent to existing tiles
2. **Word Building**: Recursively build words from each anchor
3. **Validation**: Check word validity and move legality
4. **Scoring**: Calculate complete scores including bonuses
5. **Ranking**: Sort moves by score and return best options

## Testing

### Unit Tests
```bash
python test_backend.py
```

### API Testing
With the server running:

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test empty board analysis
curl -X POST http://localhost:5000/api/test/empty-board \
  -H "Content-Type: application/json" \
  -d '{"user_tiles": ["H", "E", "L", "L", "O", "W", "_"]}'
```

## Development

### Adding New Features

1. **Models**: Add new data structures in `models/`
2. **Services**: Add business logic in `services/`
3. **API Endpoints**: Add routes in `app.py`
4. **Validation**: Add input validation in `utils/validators.py`

### Computer Vision Integration

When ready to add photo processing:

1. Install CV dependencies: `pip install opencv-python pytesseract`
2. Implement detection algorithms in `PhotoService`
3. Enable processing: Set `ENABLE_PHOTO_PROCESSING=True`
4. Test with real board images

## Troubleshooting

### Common Issues

1. **Wordset not found**: Ensure `wordset.txt` is in the backend directory
2. **Import errors**: Check that all required packages are installed
3. **CORS errors**: Verify `CORS_ORIGINS` includes your frontend URL
4. **Memory issues**: Reduce `MAX_MOVES_RETURNED` for large searches

### Logging

The backend uses Python logging. Increase verbosity by setting log level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Follow PEP 8 style guidelines
2. Add type hints to new functions
3. Include docstrings for public methods
4. Add tests for new features
5. Update this README for significant changes
