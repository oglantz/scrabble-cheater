import React, { useState } from 'react';

/**
 * TileInput component
 * Lets the user enter up to 7 tiles via individual inputs or a single text box.
 * Emits the current tile array via onTilesChange(Array<string>).
 *
 * @param {{ onTilesChange: (tiles: string[]) => void }} props
 */

const TileInput = ({ onTilesChange }) => {
  const [tiles, setTiles] = useState(['', '', '', '', '', '', '']);
  const [inputMethod, setInputMethod] = useState('individual'); // 'individual' or 'text'
  const [textInput, setTextInput] = useState('');

  const handleIndividualTileChange = (index, value) => {
    const newTiles = [...tiles];
    // Convert to uppercase and only allow single letters or underscore for blank
    const cleanValue = value.toUpperCase().replace(/[^A-Z_]/g, '');
    newTiles[index] = cleanValue.slice(0, 1);
    setTiles(newTiles);
    
    // Update parent component
    const filledTiles = newTiles.filter(tile => tile !== '');
    onTilesChange(filledTiles);
  };

  const handleTextInputChange = (value) => {
    setTextInput(value);
    // Convert to uppercase and split into individual characters
    const cleanValue = value.toUpperCase().replace(/[^A-Z_\s]/g, '').replace(/\s+/g, '');
    const tileArray = cleanValue.split('').slice(0, 7);
    
    // Pad with empty strings to maintain 7-tile structure
    const paddedTiles = [...tileArray, ...Array(7 - tileArray.length).fill('')];
    setTiles(paddedTiles);
    
    // Update parent component
    onTilesChange(tileArray);
  };

  const clearAllTiles = () => {
    setTiles(['', '', '', '', '', '', '']);
    setTextInput('');
    onTilesChange([]);
  };

  const getScrabbleValue = (letter) => {
    const values = {
      'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
      'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
      'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
      'Y': 4, 'Z': 10, '_': 0
    };
    return values[letter] || 0;
  };

  return (
    <div className="space-y-6">
      {/* Input Method Toggle */}
      <div className="flex justify-center">
        <div className="bg-gray-100 p-1 rounded-lg">
          <button
            onClick={() => setInputMethod('individual')}
            className={`px-4 py-2 rounded transition-colors ${
              inputMethod === 'individual'
                ? 'bg-white text-scrabble-brown shadow'
                : 'text-gray-600'
            }`}
          >
            Individual Tiles
          </button>
          <button
            onClick={() => setInputMethod('text')}
            className={`px-4 py-2 rounded transition-colors ${
              inputMethod === 'text'
                ? 'bg-white text-scrabble-brown shadow'
                : 'text-gray-600'
            }`}
          >
            Text Input
          </button>
        </div>
      </div>

      {inputMethod === 'individual' ? (
        /* Individual Tile Inputs */
        <div className="space-y-4">
          <div className="flex justify-center gap-2 flex-wrap">
            {tiles.map((tile, index) => (
              <div key={index} className="relative">
                <input
                  type="text"
                  value={tile}
                  onChange={(e) => handleIndividualTileChange(index, e.target.value)}
                  className="w-16 h-16 text-center text-2xl font-bold border-2 border-scrabble-brown 
                           rounded-lg bg-scrabble-cream focus:outline-none focus:ring-2 
                           focus:ring-scrabble-gold focus:border-transparent
                           shadow-md hover:shadow-lg transition-shadow"
                  placeholder=""
                  maxLength="1"
                />
                {tile && (
                  <span className="absolute -bottom-1 -right-1 bg-scrabble-brown text-white 
                                 text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold">
                    {getScrabbleValue(tile)}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      ) : (
        /* Text Input */
        <div className="space-y-4">
          <div className="max-w-md mx-auto">
            <input
              type="text"
              value={textInput}
              onChange={(e) => handleTextInputChange(e.target.value)}
              placeholder="Enter your tiles (e.g. ABCDEF_)"
              className="w-full px-4 py-3 text-center text-xl font-bold border-2 border-scrabble-brown 
                       rounded-lg bg-scrabble-cream focus:outline-none focus:ring-2 
                       focus:ring-scrabble-gold focus:border-transparent"
              maxLength="7"
            />
          </div>
          
          {/* Preview tiles */}
          <div className="flex justify-center gap-2 flex-wrap">
            {tiles.slice(0, textInput.length).map((tile, index) => (
              <div key={index} className="relative">
                <div className="w-12 h-12 text-center text-lg font-bold border-2 border-scrabble-brown 
                              rounded-lg bg-scrabble-cream shadow-md flex items-center justify-center">
                  {tile}
                </div>
                {tile && (
                  <span className="absolute -bottom-1 -right-1 bg-scrabble-brown text-white 
                                 text-xs rounded-full w-4 h-4 flex items-center justify-center font-bold">
                    {getScrabbleValue(tile)}
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Instructions and Clear Button */}
      <div className="text-center space-y-4">
        <div className="text-sm text-gray-600">
          <p>💡 <strong>Instructions:</strong></p>
          <ul className="list-disc list-inside mt-2 space-y-1">
            <li>Enter letters A-Z for your tiles</li>
            <li>Use underscore (_) for blank tiles</li>
            <li>You can enter up to 7 tiles (standard rack size)</li>
          </ul>
        </div>
        
        {tiles.some(tile => tile !== '') && (
          <button
            onClick={clearAllTiles}
            className="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded transition-colors"
          >
            Clear All Tiles
          </button>
        )}
        
        {/* Tile Count and Total Value */}
        <div className="bg-gray-100 rounded-lg p-3 inline-block">
          <div className="text-sm text-gray-600">
            Tiles: {tiles.filter(tile => tile !== '').length}/7 • 
            Total Value: {tiles.filter(tile => tile !== '').reduce((sum, tile) => sum + getScrabbleValue(tile), 0)} points
          </div>
        </div>
      </div>
    </div>
  );
};

export default TileInput;
