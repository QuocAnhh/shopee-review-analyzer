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
    <Container fluid className="d-flex flex-column vh-100 p-0">
      {/* Welcome Message */}
      <div className="welcome-message text-center py-4 d-flex flex-column justify-content-center" style={{ height: '20%' }}>
        <h1 className="display-4 mb-4">Shopee Assistant</h1>
        <p className="text-muted">How can I help you today?</p>
      </div>

      {/* Chat Container */}
      <div 
        ref={chatContainerRef}
        className="flex-grow-1 overflow-auto p-3 bg-light"
        style={{ height: '65%' }}
      >
        {/* Messages */}
        {messages.map((msg, index) => (
          <div 
            key={index} 
            className={`d-flex flex-column mb-3 ${msg.isUser ? 'align-items-end' : 'align-items-start'}`}
          >
            <div 
              className={`p-3 rounded-3 ${msg.isUser ? 'bg-primary text-white' : 'bg-white shadow-sm'}`}
              style={{ 
                maxWidth: '80%',
                borderRadius: msg.isUser ? '18px 18px 0 18px' : '18px 18px 18px 0'
              }}
            >
              {msg.content}
            </div>
            <small className={`text-muted mt-1 ${msg.isUser ? 'text-end' : 'text-start'}`}>
              {msg.time}
            </small>
          </div>
        ))}
        
        {/* Typing Indicator */}
        {isTyping && (
          <div className="typing-indicator d-flex align-items-center p-3 bg-white rounded-3 shadow-sm mb-3" style={{ width: 'fit-content' }}>
            <span className="dot" style={{ animationDelay: '0s' }}></span>
            <span className="dot mx-1" style={{ animationDelay: '0.2s' }}></span>
            <span className="dot" style={{ animationDelay: '0.4s' }}></span>
          </div>
        )}
      </div>

      {/* Input Area */}
    <div className="input-area bg-white border-top p-3" style={{ minHeight: '80px' }}>
      <Form onSubmit={handleSubmit}>
        <InputGroup style={{ height: '50px' }}> 
          <Form.Control
            as="textarea"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Nhập tin nhắn của bạn..."
            style={{ 
              resize: 'none',
              height: '50px',
              minHeight: '50px', 
              lineHeight: '1.2' 
            }}
          />
          <Button 
            variant="primary" 
            type="submit"
            disabled={!message.trim()}
            style={{
              height: '50px',
              width: '40px', 
              padding: '0' 
            }}
          >
            <FontAwesomeIcon icon={faPaperPlane} size="sm" /> 
          </Button>
        </InputGroup>
      </Form>
      <div className="text-center text-muted small mt-2">
        Shopee Assistant có thể đưa ra thông tin không chính xác. Vui lòng kiểm tra lại thông tin quan trọng.
      </div>
    </div>

      {/* CSS Styles */}
      <style>{`
        .dot {
          height: 8px;
          width: 8px;
          background-color: #6c757d;
          border-radius: 50%;
          display: inline-block;
          animation: bounce 1.4s infinite ease-in-out both;
        }
        
        @keyframes bounce {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }
        
        @media (max-width: 768px) {
          .welcome-message {
            height: 15% !important;
            padding: 1rem !important;
          }
          .welcome-message h1 {
            font-size: 1.8rem !important;
            margin-bottom: 0.5rem !important;
          }
          .welcome-message p {
            display: none;
          }
          .message-content {
            max-width: 90% !important;
          }
        }
      `}</style>
    </Container>
  );
};

export default ChatInterface;