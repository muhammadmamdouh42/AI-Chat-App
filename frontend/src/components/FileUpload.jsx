import React, { useState, useRef } from 'react';

function FileUpload({ onUpload }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0] || null);
  };

  const handleUploadClick = () => {
    if (selectedFile) {
      onUpload(selectedFile);
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <div className="p-4 bg-gray-100 flex flex-col sm:flex-row items-center gap-2">
      <input 
        type="file" 
        ref={fileInputRef}
        onChange={handleFileChange}
        className="flex-1 file:mr-2"
      />
      <button 
        className="bg-green-600 text-white px-4 py-2 rounded"
        onClick={handleUploadClick}
      >
        Upload
      </button>
    </div>
  );
}

export default FileUpload;
