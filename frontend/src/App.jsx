import React, { useState } from 'react';
import axios from 'axios';
import ChatWindow from './components/ChatWindow';
import InputArea from './components/InputArea';
import FileUpload from './components/FileUpload';

function App() {
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);

  const handleSendQuestion = async (questionText) => {
    if (!questionText) return;
    setError(null);

    setMessages((prev) => [
      ...prev,
      { role: 'user', text: questionText },
      { role: 'loading', text: '...' }
    ]);

    try {
      const res = await axios.post('/ask', { prompt: questionText });

      setMessages((prev) =>
        prev.map((msg) =>
          msg.role === 'loading'
            ? { role: 'ai', text: res.data.answer }
            : msg
        )
      );
    } catch (err) {
      setMessages((prev) => prev.filter((msg) => msg.role !== 'loading'));
      setError('Failed to get a response. Please try again.');
    }
  };

  const handleUploadFile = async (file) => {
    if (!file) return;
    setError(null);

    setMessages((prev) => [
      ...prev,
      { role: 'user', text: `Uploaded file: ${file.name}` },
      { role: 'loading', text: 'Uploading...' }
    ]);

    try {
      const formData = new FormData();
      formData.append('files', file);
      await axios.post('/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setMessages((prev) =>
        prev.map((msg) =>
          msg.role === 'loading'
            ? { role: 'system', text: 'File uploaded successfully.' }
            : msg
        )
      );
    } catch (err) {
      setMessages((prev) => prev.filter((msg) => msg.role !== 'loading'));
      setError('File upload failed. Please try again.');
    }
  };

  return (
    <div className="flex flex-col h-screen">
      <ChatWindow messages={messages} />
      {error && <div className="text-red-500 text-center p-2">{error}</div>}
      <InputArea onSend={handleSendQuestion} />
      <FileUpload onUpload={handleUploadFile} />
    </div>
  );
}

export default App;
