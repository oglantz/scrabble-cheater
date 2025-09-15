import React, { useState } from 'react';
import ScrabbleBoard from './ScrabbleBoard';

/**
 * ResultsDisplay component
 * Renders the top moves, details for the selected move, and a visual board.
 *
 * @param {{ results: {
 *   moves: Array<{ word: string, score: number, tiles: Array<[number, number, string, boolean]>, direction: 'right'|'down', start: [number, number] }>,
 *   board_state: any,
 * } }} props
 */

const ResultsDisplay = ({ results }) => {
  const [selectedMove, setSelectedMove] = useState(0);

  if (!results || !results.moves || results.moves.length === 0) {
    return (
      <div className="text-center py-8">
        <div className="text-gray-500 text-lg">
          No optimal moves found. Try different tiles or check the board image.
        </div>
      </div>
    );
  }

  const move = results.moves[selectedMove];

  const formatPosition = (row, col) => {
    return `${row + 1},${col + 1}`;
  };

  const getDirectionIcon = (direction) => {
    return direction === 'right' ? '→' : '↓';
  };

  return (
    <div className="space-y-6">
      {/* Move Selector */}
      {results.moves.length > 1 && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">
            Top {Math.min(5, results.moves.length)} Moves
          </h3>
          <div className="grid gap-2">
            {results.moves.slice(0, 5).map((moveOption, index) => (
              <button
                key={index}
                onClick={() => setSelectedMove(index)}
                className={`text-left p-3 rounded-lg border-2 transition-colors ${
                  selectedMove === index
                    ? 'border-scrabble-green bg-green-50'
                    : 'border-gray-200 hover:border-gray-300 bg-white'
                }`}
              >
                <div className="flex justify-between items-center">
                  <div>
                    <span className="font-bold text-lg">{moveOption.word}</span>
                    <span className="text-gray-600 ml-2">
                      {getDirectionIcon(moveOption.direction)} 
                      {formatPosition(moveOption.start[0], moveOption.start[1])}
                    </span>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-scrabble-green">
                      {moveOption.score}
                    </div>
                    <div className="text-sm text-gray-600">points</div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Selected Move Details */}
      <div className="bg-gradient-to-r from-scrabble-green to-green-600 text-white rounded-lg p-6">
        <div className="text-center">
          <h3 className="text-3xl font-bold mb-2">{move.word}</h3>
          <div className="text-5xl font-bold mb-2">{move.score}</div>
          <div className="text-xl opacity-90">points</div>
        </div>
      </div>

      {/* Move Details */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Placement Information */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="text-lg font-semibold text-gray-800 mb-3">Placement Details</h4>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Starting Position:</span>
              <span className="font-medium">
                {formatPosition(move.start[0], move.start[1])}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Direction:</span>
              <span className="font-medium">
                {getDirectionIcon(move.direction)} {move.direction}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Word Length:</span>
              <span className="font-medium">{move.word.length} letters</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Tiles Used:</span>
              <span className="font-medium">{move.tiles.length} tiles</span>
            </div>
          </div>
        </div>

        {/* Tiles to Place */}
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="text-lg font-semibold text-gray-800 mb-3">Tiles to Place</h4>
          <div className="grid grid-cols-7 gap-1">
            {move.tiles.map((tile, index) => (
              <div key={index} className="text-center">
                <div className="relative">
                  <div className="w-10 h-10 bg-scrabble-cream border-2 border-scrabble-brown 
                                rounded flex items-center justify-center font-bold text-lg">
                    {tile[2]}
                  </div>
                  {tile[3] && (
                    <div className="absolute -top-1 -right-1 w-3 h-3 bg-yellow-400 rounded-full" 
                         title="Blank tile"></div>
                  )}
                </div>
                <div className="text-xs text-gray-600 mt-1">
                  {formatPosition(tile[0], tile[1])}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Score Breakdown */}
      <div className="bg-white border border-gray-200 rounded-lg p-4">
        <h4 className="text-lg font-semibold text-gray-800 mb-3">Score Breakdown</h4>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-gray-600">Base Word Score:</span>
            <span className="font-medium">{move.score} points</span>
          </div>
          {move.tiles.length === 7 && (
            <div className="flex justify-between text-scrabble-green">
              <span>Bingo Bonus (7 tiles):</span>
              <span className="font-medium">+50 points</span>
            </div>
          )}
        </div>
      </div>

      {/* Visual Board Display */}
      <ScrabbleBoard 
        boardState={results.board_state} 
        selectedMove={move} 
      />

      {/* Instructions */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="text-lg font-semibold text-blue-800 mb-2">How to Play This Move</h4>
        <ol className="list-decimal list-inside text-blue-700 space-y-1">
          <li>Place the tiles shown above on the board</li>
          <li>Start at position {formatPosition(move.start[0], move.start[1])}</li>
          <li>Place tiles going {move.direction} to spell "{move.word}"</li>
          <li>Score {move.score} points for this move!</li>
        </ol>
      </div>
    </div>
  );
};

export default ResultsDisplay;
