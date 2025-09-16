import React, { useState } from 'react';
import PhotoUpload from './components/PhotoUpload';
import TileInput from './components/TileInput';
import ResultsDisplay from './components/ResultsDisplay';
import LiveTester from './components/LiveTester';
import Header from './components/Header';
import './App.css';

/**
 * Root application component.
 * Manages uploaded image, tile state, analysis calls, and renders UI sections.
 */
function App() {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [userTiles, setUserTiles] = useState([]);
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [mode, setMode] = useState('image'); // 'image' | 'manual'

  const handleImageUpload = (imageFile) => {
    setUploadedImage(imageFile);
    // Reset results when new image is uploaded
    setResults(null);
  };

  const handleTilesChange = (tiles) => {
    setUserTiles(tiles);
  };

  const handleAnalyze = async () => {
    if (!uploadedImage || userTiles.length === 0) {
      alert('Please upload a board image and enter your tiles');
      return;
    }

    setIsLoading(true);
    
    try {
      // Create FormData for multipart upload
      const formData = new FormData();
      formData.append('board_image', uploadedImage);
      formData.append('user_tiles', JSON.stringify(userTiles));

      // This will connect to the Flask backend once it's ready
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze board');
      }

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error analyzing board:', error);
      alert('Error analyzing board. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Mode Switch - Debug Test */}
          <div className="bg-red-500 p-4 mb-6">
            <h2 className="text-white text-xl font-bold mb-2">DEBUG: Mode Switcher</h2>
            <p className="text-white mb-2">Current mode: {mode}</p>
            <button
              onClick={() => setMode('image')}
              className="bg-blue-500 text-white px-4 py-2 mr-2"
            >
              Image Mode
            </button>
            <button
              onClick={() => setMode('manual')}
              className="bg-green-500 text-white px-4 py-2"
            >
              Manual Mode
            </button>
          </div>

          {mode === 'image' ? (
            <>
              {/* Upload Section */}
              <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                  Upload Scrabble Board
                </h2>
                <PhotoUpload onImageUpload={handleImageUpload} />
              </div>

              {/* Tiles Input Section */}
              <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                  Your Tiles
                </h2>
                <TileInput onTilesChange={handleTilesChange} />
              </div>

              {/* Analyze Button */}
              <div className="text-center mb-6">
                <button
                  onClick={handleAnalyze}
                  disabled={isLoading || !uploadedImage || userTiles.length === 0}
                  className="bg-scrabble-green hover:bg-green-600 disabled:bg-gray-400 text-white font-bold py-3 px-8 rounded-lg text-lg transition-colors duration-200 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Analyzing...
                    </>
                  ) : (
                    'Find Best Moves'
                  )}
                </button>
              </div>

              {/* Results Section */}
              {results && (
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h2 className="text-2xl font-semibold text-gray-800 mb-4">Optimal Moves</h2>
                  <ResultsDisplay results={results} />
                </div>
              )}
            </>
          ) : (
            <LiveTester />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
