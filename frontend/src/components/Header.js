import React from 'react';

/**
 * Header component for the Scrabble Cheater app.
 * Displays the title and a short description.
 */

const Header = () => {
  return (
    <header className="bg-scrabble-brown text-white shadow-lg">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-2">Scrabble Cheater :D</h1>
            <p className="text-scrabble-cream text-lg">
              Upload your board, enter your tiles, and find the best moves!
            </p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
