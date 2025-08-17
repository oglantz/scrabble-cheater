# Scrabble Cheater Frontend

A React-based frontend for the Scrabble Cheater application that helps users find optimal Scrabble moves.

## Features

- **Photo Upload**: Drag-and-drop interface for uploading Scrabble board images
- **Tile Input**: Flexible tile entry with individual inputs or text mode
- **Results Display**: Beautiful visualization of optimal moves with detailed scoring
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, Scrabble-themed design with Tailwind CSS

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) to view the app in your browser.

### Building for Production

```bash
npm run build
```

## Usage

1. **Upload Board Image**: Take a clear photo of your Scrabble board from above and upload it
2. **Enter Your Tiles**: Use either the individual tile inputs or text input to enter your available tiles
3. **Analyze**: Click "Find Best Moves" to get optimal placement suggestions
4. **Review Results**: Browse through the top moves and see detailed placement instructions

## API Integration

The frontend is configured to work with a Flask backend running on `localhost:5000`. The main API endpoint expected is:

```
POST /api/analyze
Content-Type: multipart/form-data

Parameters:
- board_image: Image file of the Scrabble board
- user_tiles: JSON array of user's available tiles
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)

## Technologies Used

- React 18
- Tailwind CSS
- Axios for API calls
- Create React App

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
