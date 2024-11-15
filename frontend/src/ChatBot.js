import React, { useState } from 'react';
import './App.css';

const ChatBot = () => {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSend = async () => {
        if (!inputValue) return;

        setMessages(prevMessages => [
            ...prevMessages,
            { sender: 'user', text: inputValue }
        ]);

        setLoading(true);

        try {
            const response = await fetch('http://localhost:8000/search/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: inputValue }),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch response from the server');
            }

            const data = await response.json();
            
            const botMessage = data.response.length > 0
                ? data.response.map(post => `${post.title}: ${post.summary}`).join('\n\n')
                : "No relevant information found.";

            setMessages(prevMessages => [
                ...prevMessages,
                { sender: 'bot', text: botMessage }
            ]);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prevMessages => [
                ...prevMessages,
                { sender: 'bot', text: 'Error: Unable to fetch response. Please try again later.' }
            ]);
        }

        setLoading(false);
        setInputValue('');
    };

    return (
        <div className="chatbot-container">
            <div className="chat-heading">Chat Interface</div>
            <div className="chat-window">
                {/* Displaying user and bot messages */}
                {messages.map((msg, index) => (
                    <div key={index} className={msg.sender}>
                        {msg.text}
                    </div>
                ))}

                {/* Loading spinner */}
                {loading && <div className="loading">Bot is typing...</div>}
            </div>

            {/* Input field and send button */}
            <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Type your message..."
            />
            <button onClick={handleSend} disabled={loading || !inputValue}>Send</button>
        </div>
    );
};

export default ChatBot;