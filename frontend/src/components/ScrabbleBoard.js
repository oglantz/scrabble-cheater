import React from 'react';

const ScrabbleBoard = ({ boardState, selectedMove }) => {
  const BOARD_SIZE = 15;
  
  // Premium square mappings
  const premiumSquares = {
    // Triple Word (TW) - dark red
    'TW': [[0,0], [0,7], [0,14], [7,0], [7,14], [14,0], [14,7], [14,14]],
    // Double Word (DW) - light red
    'DW': [[1,1], [2,2], [3,3], [4,4], [10,10], [11,11], [12,12], [13,13], 
           [1,13], [2,12], [3,11], [4,10], [10,4], [11,3], [12,2], [13,1], [7,7]],
    // Triple Letter (TL) - dark blue
    'TL': [[1,5], [1,9], [5,1], [5,5], [5,9], [5,13], [9,1], [9,5], [9,9], [9,13], [13,5], [13,9]],
    // Double Letter (DL) - light blue
    'DL': [[0,3], [0,11], [2,6], [2,8], [3,0], [3,7], [3,14], [6,2], [6,6], [6,8], [6,12], 
           [7,3], [7,11], [8,2], [8,6], [8,8], [8,12], [11,0], [11,7], [11,14], [12,6], [12,8], [14,3], [14,11]]
  };

  // Create a lookup for premium squares
  const premiumLookup = {};
  Object.entries(premiumSquares).forEach(([type, positions]) => {
    positions.forEach(([row, col]) => {
      premiumLookup[`${row}-${col}`] = type;
    });
  });

  // Create board with existing tiles and new move tiles
  const createBoardDisplay = () => {
    const board = Array(BOARD_SIZE).fill(null).map(() => Array(BOARD_SIZE).fill(null));
    
    // Place existing tiles from board state
    if (boardState && boardState.board) {
      for (let row = 0; row < BOARD_SIZE; row++) {
        for (let col = 0; col < BOARD_SIZE; col++) {
          const tile = boardState.board[row][col];
          if (tile && tile.letter) {
            board[row][col] = {
              letter: tile.letter,
              isBlank: tile.is_blank || false,
              isExisting: true,
              premium: tile.premium
            };
          }
        }
      }
    }
    
    // Place new move tiles
    if (selectedMove && selectedMove.tiles) {
      selectedMove.tiles.forEach(([row, col, letter, isBlank]) => {
        board[row][col] = {
          letter: letter,
          isBlank: isBlank || false,
          isExisting: false,
          premium: null
        };
      });
    }
    
    return board;
  };

  const board = createBoardDisplay();

  const getPremiumClass = (premium) => {
    switch (premium) {
      case 'TW':
        return 'bg-red-800 text-white text-xs font-bold';
      case 'DW':
        return 'bg-red-400 text-white text-xs font-bold';
      case 'TL':
        return 'bg-blue-800 text-white text-xs font-bold';
      case 'DL':
        return 'bg-blue-400 text-white text-xs font-bold';
      default:
        return 'bg-green-100';
    }
  };

  const getPremiumText = (premium) => {
    switch (premium) {
      case 'TW': return 'TRIPLE\nWORD\nSCORE';
      case 'DW': return 'DOUBLE\nWORD\nSCORE';
      case 'TL': return 'TRIPLE\nLETTER\nSCORE';
      case 'DL': return 'DOUBLE\nLETTER\nSCORE';
      default: return '';
    }
  };

  const getLetterScore = (letter) => {
    const scores = {
      'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8,
      'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1,
      'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
    };
    return scores[letter?.toUpperCase()] || 0;
  };

  return (
    <div className="bg-white border border-gray-300 rounded-lg p-4">
      <h4 className="text-lg font-semibold text-gray-800 mb-3 text-center">
        Board with Optimal Move
      </h4>
      
      <div className="flex justify-center">
        <div className="grid grid-cols-15 gap-px bg-gray-400 p-2 rounded-lg" 
             style={{gridTemplateColumns: 'repeat(15, 1fr)'}}>
          {board.map((row, rowIndex) => 
            row.map((cell, colIndex) => {
              const premium = premiumLookup[`${rowIndex}-${colIndex}`];
              const hasTile = cell && cell.letter;
              
              return (
                <div
                  key={`${rowIndex}-${colIndex}`}
                  className={`
                    w-8 h-8 flex items-center justify-center relative border border-gray-300
                    ${hasTile 
                      ? (cell.isExisting 
                          ? 'bg-yellow-100 border-yellow-400' 
                          : 'bg-green-200 border-green-500 shadow-lg') 
                      : (premium 
                          ? getPremiumClass(premium)
                          : 'bg-green-50')
                    }
                    ${rowIndex === 7 && colIndex === 7 && !hasTile ? 'bg-red-200' : ''}
                  `}
                >
                                     {hasTile ? (
                     <div className="w-full h-full flex flex-col items-center justify-center bg-yellow-50 border border-gray-400 rounded relative">
                       <span className="text-lg font-bold text-gray-800">
                         {cell.letter}
                       </span>
                                               <span className="absolute bottom-0 right-0 text-[8px] text-gray-600 leading-none">
                          {cell.isBlank ? 0 : getLetterScore(cell.letter)}
                        </span>
                       {!cell.isExisting && (
                         <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border border-white"></div>
                       )}
                     </div>
                   ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      {premium && (
                        <span className="text-center leading-none whitespace-pre-line" style={{fontSize: '6px'}}>
                          {getPremiumText(premium)}
                        </span>
                      )}
                      {rowIndex === 7 && colIndex === 7 && !premium && (
                        <span className="text-yellow-600 text-xl">★</span>
                      )}
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>
      </div>
      
      {/* Legend */}
      <div className="mt-4 flex flex-wrap justify-center gap-4 text-sm">
        <div className="flex items-center gap-1">
          <div className="w-4 h-4 bg-yellow-100 border border-yellow-400 rounded"></div>
          <span>Existing tiles</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-4 h-4 bg-green-200 border border-green-500 rounded relative">
            <div className="absolute -top-1 -right-1 w-2 h-2 bg-green-500 rounded-full border border-white"></div>
          </div>
          <span>New move tiles</span>
        </div>
      </div>
    </div>
  );
};

export default ScrabbleBoard;
