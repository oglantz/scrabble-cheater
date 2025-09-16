/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        scrabble: {
          brown: '#8B4513',
          cream: '#F5F5DC',
          gold: '#FFD700',
          green: '#228B22',
          blue: '#4169E1',
          red: '#DC143C'
        }
      },
      gridTemplateColumns: {
        '15': 'repeat(15, minmax(0, 1fr))',
      }
    },
  },
  plugins: [],
}
