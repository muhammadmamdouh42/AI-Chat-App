import React, { useState } from 'react';

function InputArea({ onSend }) {
  const [text, setText] = useState('');

  const handleSendClick = () => {
    if (text.trim() !== '') {
      onSend(text.trim());
      setText('');
    }
  };

  return (
    <div className="p-4 bg-gray-100 flex flex-col sm:flex-row gap-2">
      <input
        type="text"
        className="flex-1 p-2 border border-gray-300 rounded"
        placeholder="Type your question..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => { if (e.key === 'Enter') handleSendClick(); }}
      />
      <button 
        className="bg-blue-600 text-white px-4 py-2 rounded"
        onClick={handleSendClick}
      >
        Send
      </button>
    </div>
  );
}

export default InputArea;
