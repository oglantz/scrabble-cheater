import React, { useState, useRef } from 'react';

/**
 * PhotoUpload component
 * - Drag-and-drop or click-to-select image upload for the board photo.
 * - Calls onImageUpload(File) when a valid image is selected.
 */

/**
 * @param {{ onImageUpload: (file: File) => void }} props
 */
const PhotoUpload = ({ onImageUpload }) => {
  const [dragActive, setDragActive] = useState(false);
  const [uploadedImage, setUploadedImage] = useState(null);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    if (file && file.type.startsWith('image/')) {
      setUploadedImage(file);
      onImageUpload(file);
    } else {
      alert('Please upload a valid image file.');
    }
  };

  const onButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="w-full">
      <div
        className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors
          ${dragActive 
            ? 'border-scrabble-green bg-green-50' 
            : 'border-gray-300 hover:border-gray-400'
          }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept="image/*"
          onChange={handleChange}
        />
        
        {uploadedImage ? (
          <div className="space-y-4">
            <div className="flex justify-center">
              <img
                src={URL.createObjectURL(uploadedImage)}
                alt="Uploaded Scrabble board"
                className="max-h-64 max-w-full rounded-lg shadow-md"
              />
            </div>
            <p className="text-green-600 font-medium">
              ✓ Image uploaded: {uploadedImage.name}
            </p>
            <button
              onClick={onButtonClick}
              className="bg-scrabble-blue hover:bg-blue-600 text-white font-medium py-2 px-4 rounded transition-colors"
            >
              Choose Different Image
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="mx-auto w-16 h-16 text-gray-400">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <div>
              <p className="text-xl font-medium text-gray-700 mb-2">
                Upload a photo of your Scrabble board
              </p>
              <p className="text-gray-500 mb-4">
                Drag and drop your image here, or click to select
              </p>
              <button
                onClick={onButtonClick}
                className="bg-scrabble-blue hover:bg-blue-600 text-white font-medium py-2 px-6 rounded transition-colors"
              >
                Select Image
              </button>
            </div>
          </div>
        )}
      </div>
      
      <div className="mt-4 text-sm text-gray-600">
        <p>💡 <strong>Tips for best results:</strong></p>
        <ul className="list-disc list-inside mt-2 space-y-1">
          <li>Take the photo from directly above the board</li>
          <li>Ensure good lighting and all tiles are clearly visible</li>
          <li>Avoid shadows and glare on the board</li>
        </ul>
      </div>
    </div>
  );
};

export default PhotoUpload;
