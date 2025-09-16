import React, { useMemo, useState } from 'react';

/**
 * BoardEditor
 * Interactive 15x15 Scrabble board editor. Click a cell to edit its letter and blank state.
 * Emits a backend-compatible board_state via onChange.
 *
 * @param {{ onChange?: (boardState: any) => void, initialBoardState?: any }} props
 */
const BoardEditor = ({ onChange, initialBoardState }) => {
  const BOARD_SIZE = 15;

  const premiumSquares = useMemo(() => ({
    'TW': [[0,0], [0,7], [0,14], [7,0], [7,14], [14,0], [14,7], [14,14]],
    'DW': [[1,1], [2,2], [3,3], [4,4], [10,10], [11,11], [12,12], [13,13],
           [1,13], [2,12], [3,11], [4,10], [10,4], [11,3], [12,2], [13,1], [7,7]],
    'TL': [[1,5], [1,9], [5,1], [5,5], [5,9], [5,13], [9,1], [9,5], [9,9], [9,13], [13,5], [13,9]],
    'DL': [[0,3], [0,11], [2,6], [2,8], [3,0], [3,7], [3,14], [6,2], [6,6], [6,8], [6,12],
           [7,3], [7,11], [8,2], [8,6], [8,8], [8,12], [11,0], [11,7], [11,14], [12,6], [12,8], [14,3], [14,11]]
  }), []);

  const premiumLookup = useMemo(() => {
    const map = {};
    Object.entries(premiumSquares).forEach(([type, positions]) => {
      positions.forEach(([row, col]) => {
        map[`${row}-${col}`] = type;
      });
    });
    return map;
  }, [premiumSquares]);

  const makeEmptyBoard = () => {
    const board = Array(BOARD_SIZE).fill(null).map(() => Array(BOARD_SIZE).fill(null));
    for (let r = 0; r < BOARD_SIZE; r++) {
      for (let c = 0; c < BOARD_SIZE; c++) {
        const premium = premiumLookup[`${r}-${c}`] || null;
        board[r][c] = { letter: null, is_blank: false, premium, is_placed_this_turn: false };
      }
    }
    return board;
  };

  const initialBoard = useMemo(() => {
    if (initialBoardState && initialBoardState.board && initialBoardState.board.length === BOARD_SIZE) {
      // Normalize incoming board to the expected shape
      const b = makeEmptyBoard();
      for (let r = 0; r < BOARD_SIZE; r++) {
        for (let c = 0; c < BOARD_SIZE; c++) {
          const tile = initialBoardState.board[r][c] || {};
          b[r][c] = {
            letter: tile.letter || null,
            is_blank: !!tile.is_blank,
            premium: b[r][c].premium,
            is_placed_this_turn: false,
          };
        }
      }
      return b;
    }
    return makeEmptyBoard();
  }, [initialBoardState]);

  const [board, setBoard] = useState(initialBoard);
  const [editingCell, setEditingCell] = useState(null); // {row, col}
  const [tempLetter, setTempLetter] = useState('');
  const [tempBlank, setTempBlank] = useState(false);

  const emitChange = (newBoard) => {
    onChange && onChange({ board: newBoard });
  };

  const startEdit = (row, col) => {
    const tile = board[row][col];
    setEditingCell({ row, col });
    setTempLetter(tile.letter || '');
    setTempBlank(!!tile.is_blank);
  };

  const commitEdit = () => {
    if (!editingCell) return;
    const { row, col } = editingCell;
    const newBoard = board.map((r, ri) => r.map((t, ci) => (ri === row && ci === col ? { ...t } : t)));
    const letter = tempLetter.trim().toUpperCase();
    if (letter === '') {
      newBoard[row][col].letter = null;
      newBoard[row][col].is_blank = false;
    } else {
      // Allow only A-Z
      const clean = letter.replace(/[^A-Z]/g, '').slice(0, 1);
      newBoard[row][col].letter = clean || null;
      newBoard[row][col].is_blank = tempBlank && !!clean;
    }
    setBoard(newBoard);
    setEditingCell(null);
    emitChange(newBoard);
  };

  const clearBoard = () => {
    const b = makeEmptyBoard();
    setBoard(b);
    emitChange(b);
  };

  const getPremiumClass = (premium) => {
    switch (premium) {
      case 'TW': return 'bg-red-800 text-white text-[9px] font-bold';
      case 'DW': return 'bg-red-400 text-white text-[9px] font-bold';
      case 'TL': return 'bg-blue-800 text-white text-[9px] font-bold';
      case 'DL': return 'bg-blue-400 text-white text-[9px] font-bold';
      default: return 'bg-green-100';
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
    const scores = { 'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,'J':8,'K':5,'L':1,'M':3,'N':1,'O':1,'P':3,'Q':10,'R':1,'S':1,'T':1,'U':1,'V':4,'W':4,'X':8,'Y':4,'Z':10 };
    return scores[letter?.toUpperCase()] || 0;
  };

  return (
    <div className="bg-white border border-gray-300 rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <h4 className="text-lg font-semibold text-gray-800">Manual Board Editor</h4>
        <button onClick={clearBoard} className="text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 px-3 py-1 rounded">Clear Board</button>
      </div>

      <div className="flex justify-center">
        <div className="grid grid-cols-15 gap-px bg-gray-400 p-2 rounded-lg">
          {board.map((row, ri) => row.map((cell, ci) => {
            const premium = premiumLookup[`${ri}-${ci}`];
            const hasTile = !!cell.letter;
            const isEditing = editingCell && editingCell.row === ri && editingCell.col === ci;
            return (
              <div
                key={`${ri}-${ci}`}
                className={`w-8 h-8 relative border border-gray-300 cursor-pointer ${hasTile ? 'bg-yellow-100 border-yellow-400' : (premium ? getPremiumClass(premium) : 'bg-green-50')} ${ri===7 && ci===7 && !hasTile ? 'bg-red-200' : ''}`}
                onClick={() => startEdit(ri, ci)}
              >
                {!isEditing && hasTile && (
                  <div className="w-full h-full flex flex-col items-center justify-center bg-yellow-50 border border-gray-400 rounded">
                    <span className="text-lg font-bold text-gray-800">{cell.letter}</span>
                    <span className="absolute bottom-0 right-0 text-[8px] text-gray-600 leading-none">{cell.is_blank ? 0 : getLetterScore(cell.letter)}</span>
                    {cell.is_blank && <span className="absolute top-0 left-0 text-[10px] text-blue-700 px-0.5">BL</span>}
                  </div>
                )}
                {!isEditing && !hasTile && (
                  <div className="w-full h-full flex items-center justify-center pointer-events-none">
                    {premium && (
                      <span className="text-center leading-none whitespace-pre-line" style={{ fontSize: '6px' }}>{getPremiumText(premium)}</span>
                    )}
                    {ri===7 && ci===7 && !premium && (
                      <span className="text-yellow-600 text-xl">★</span>
                    )}
                  </div>
                )}
                {isEditing && (
                  <div className="absolute inset-0 bg-white/90 p-1 flex flex-col items-center justify-center gap-1 z-10" onClick={(e) => e.stopPropagation()} onMouseDown={(e) => e.stopPropagation()}>
                    <input
                      type="text"
                      value={tempLetter}
                      onChange={(e) => setTempLetter(e.target.value.toUpperCase().replace(/[^A-Z]/g, '').slice(0,1))}
                      onKeyDown={(e) => { if (e.key === 'Enter') commitEdit(); if (e.key === 'Escape') setEditingCell(null); }}
                      className="w-10 h-7 text-center text-base font-bold border border-gray-400 rounded"
                      autoFocus
                    />
                    <label className="flex items-center gap-1 text-[10px] text-gray-700">
                      <input type="checkbox" checked={tempBlank} onChange={(e) => setTempBlank(e.target.checked)} /> Blank
                    </label>
                    <div className="flex gap-1">
                      <button className="text-xs bg-green-600 text-white px-2 py-0.5 rounded" onClick={(e) => { e.stopPropagation(); commitEdit(); }}>Save</button>
                      <button className="text-xs bg-gray-400 text-white px-2 py-0.5 rounded" onClick={(e) => { e.stopPropagation(); setEditingCell(null); }}>Cancel</button>
                    </div>
                  </div>
                )}
              </div>
            );
          }))}
        </div>
      </div>
    </div>
  );
};

export default BoardEditor;


