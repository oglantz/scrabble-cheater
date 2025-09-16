import React, { useState } from 'react';
import BoardEditor from './BoardEditor';
import TileInput from './TileInput';
import ResultsDisplay from './ResultsDisplay';

/**
 * LiveTester
 * Manual board + rack tester. Lets you edit the board and tiles, then calls /api/analyze with JSON.
 */
const LiveTester = () => {
  const [boardState, setBoardState] = useState(null);
  const [tiles, setTiles] = useState([]);
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const canAnalyze = tiles.length > 0 && boardState && boardState.board;

  const analyze = async () => {
    if (!canAnalyze) return;
    setIsLoading(true);
    setResults(null);
    try {
      const resp = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_tiles: tiles, board_state: boardState }),
      });
      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        throw new Error(err.error || 'Request failed');
      }
      const data = await resp.json();
      setResults(data);
    } catch (e) {
      console.error(e);
      alert(`Analyze failed: ${e.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Manual Board & Rack</h2>
        <BoardEditor onChange={setBoardState} />
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Your Tiles</h2>
        <TileInput onTilesChange={setTiles} />
      </div>

      <div className="text-center">
        <button
          onClick={analyze}
          disabled={!canAnalyze || isLoading}
          className="bg-scrabble-green hover:bg-green-600 disabled:bg-gray-400 text-white font-bold py-3 px-8 rounded-lg text-lg transition-colors"
        >
          {isLoading ? 'Analyzing…' : 'Analyze Manual Board'}
        </button>
      </div>

      {results && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Results</h2>
          <ResultsDisplay results={results} />
        </div>
      )}
    </div>
  );
};

export default LiveTester;


