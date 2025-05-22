import React, { useState, useRef, useEffect } from 'react';
import { Container, Form, InputGroup, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';

const ChatInterface = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const chatContainerRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!message.trim()) return;
    
    // Add user message
    const userMessage = {
      content: message,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      isUser: true
    };
    
    setMessages(prev => [...prev, userMessage]);
    setMessage('');
    
    // Simulate bot typing
    setIsTyping(true);
    setTimeout(() => {
      const botMessage = {
        content: 'This is a sample response from the assistant.',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        isUser: false
      };
      setMessages(prev => [...prev, botMessage]);
      setIsTyping(false);
    }, 1500);
  };

  useEffect(() => {
    // Auto-scroll to bottom when messages change
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  return (
    <Container fluid className="d-flex flex-column h-100 p-0">
      {/* Welcome Message */}
      <div className="welcome-message text-center py-5">
        <h1 className="display-4 mb-4 chat-header-container">Shopee Assistant</h1>
      </div>

      {/* Chat Container */}
      <div 
        ref={chatContainerRef}
        className="chat-container flex-grow-1 overflow-auto p-3 bg-light"
      >
        {/* Messages */}
        {messages.map((msg, index) => (
          <div 
            key={index} 
            className={`message d-flex flex-column mb-3 ${msg.isUser ? 'align-items-end' : 'align-items-start'}`}
          >
            <div 
              className={`message-content p-3 rounded-3 ${msg.isUser ? 'bg-primary text-white' : 'bg-white'}`}
              style={{ maxWidth: '80%' }}
            >
              {msg.content}
            </div>
            <div className="message-time small text-muted">
              {msg.time}
            </div>
          </div>
        ))}
        
        {/* Typing Indicator */}
        {isTyping && (
          <div className="typing-indicator d-flex align-items-center p-2 bg-white rounded-3 shadow-sm mb-3">
            <span className="dot me-1" style={{ animationDelay: '0s' }}></span>
            <span className="dot me-1" style={{ animationDelay: '0.2s' }}></span>
            <span className="dot" style={{ animationDelay: '0.4s' }}></span>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="input-area-container bg-white border-top p-3">
        <Form onSubmit={handleSubmit} className="chat-input-form">
          <InputGroup>
            <Form.Control
              as="textarea"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Nhập tin nhắn của bạn..."
              rows={1}
              style={{ resize: 'none' }}
            />
            <Button 
              variant="primary" 
              type="submit"
              disabled={!message.trim()}
            >
              <FontAwesomeIcon icon={faPaperPlane} />
            </Button>
          </InputGroup>
        </Form>
        <div className="text-center text-muted small mt-2">
          Shopee Assistant có thể đưa ra thông tin không chính xác. Vui lòng kiểm tra lại thông tin quan trọng.
        </div>
      </div>

      {/* CSS for typing indicator */}
      <style>{`
        .dot {
          height: 10px;
          width: 10px;
          background-color: #bbb;
          border-radius: 50%;
          display: inline-block;
          animation: bounce 1.4s infinite ease-in-out both;
        }
        
        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }
        
        .chat-container {
          min-height: 0;
        }
      `}</style>
    </Container>
  );
};

export default ChatInterface;