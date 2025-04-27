import React from 'react';

function ChatWindow({ messages }) {
  return (
    <div className="flex-1 p-4 overflow-y-auto bg-white">
      {messages.map((msg, index) => (
        <div 
          key={index}
          className={`mb-2 flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div className={`px-4 py-2 rounded-lg max-w-md break-words 
                           ${msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-900'}`}>
            {msg.text}
          </div>
        </div>
      ))}
    </div>
  );
}

export default ChatWindow;
