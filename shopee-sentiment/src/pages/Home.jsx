import React, { useState, useRef, useEffect } from 'react';
import { Container, Form, InputGroup, Button, Card, Stack } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';

const ChatInterface = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const chatContainerRef = useRef(null);

  const askShopee = async (query) => {
    setIsTyping(true);
    
    try {
      const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const data = await res.json();

      if (data.error) {
        return {
          content: data.error,
          isUser: false
        };
      }

      let botResponse = "";
      // Phân tích sản phẩm
      if (data.summary && (data.demo_reviews || data.file_path)) {
        botResponse = `<b>Tóm tắt:</b> <br>${data.summary}<br><br>`;
        
        if (data.file_path) {
          botResponse += `<b>File dữ liệu crawl:</b> <a href='${data.file_path}' download target='_blank'>Tải file dữ liệu vừa crawl</a><br><br>`;
        }
        
        if (data.demo_reviews && data.demo_reviews.length > 0) {
          botResponse += '<b>Demo cảm xúc (5 bình luận ngẫu nhiên):</b><ul>';
          data.demo_reviews.forEach(function(s) {
            botResponse += `<li>${s.review ? s.review : ''} <b>[${s.sentiment}]</b></li>`;
          });
          botResponse += '</ul>';
        }
        
        if (data.product_review) {
          botResponse += `<br><b>Đánh giá tổng quan:</b><br>${data.product_review}`;
        }
        
        if (data.chart_url) {
          botResponse += `<br><img src='${data.chart_url}' style='max-width:100%; border-radius:8px; margin-top:10px;'>`;
        }
      } 
      // Trả lời câu hỏi Shopee
      else if (data.answer) {
        botResponse = `<b>Trả lời:</b><br>${data.answer}`;
      }
      
      return {
        content: botResponse,
        isUser: false
      };
    } catch (error) {
      return {
        content: "Đã xảy ra lỗi khi kết nối với server",
        isUser: false
      };
    } finally {
      setIsTyping(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;
    
    // Thêm tin nhắn người dùng
    const userMessage = {
      content: message,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      isUser: true
    };
    
    setMessages(prev => [...prev, userMessage]);
    setMessage('');
    
    // Gửi yêu cầu và nhận phản hồi
    const botResponse = await askShopee(message);
    setMessages(prev => [...prev, {
      ...botResponse,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }]);
  };

  useEffect(() => {
    // Tự động cuộn xuống dưới cùng
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const Message = ({ content, time, isUser }) => (
    <Stack
      direction="vertical"
      gap={1}
      className={`mb-3 align-items-${isUser ? 'end' : 'start'}`}
    >  
      <Card
        bg={isUser ? 'primary' : 'light'}
        text={isUser ? 'white' : 'dark'}
        className="rounded-3 p-2"
      >
        <div 
          className="message-content" 
          dangerouslySetInnerHTML={{ __html: content }}
          style={{ maxWidth: '100%', overflowWrap: 'break-word' }}
        />
      </Card>
      <small className="text-muted">{time}</small>
    </Stack>
  );

  const TypingIndicator = () => (
    <div className="d-flex align-items-center p-2 bg-white rounded-3 shadow-sm mb-3">
      {[...Array(3)].map((_, i) => (
        <span
          key={i}
          className="dot bg-secondary rounded-circle mx-1"
          style={{
            width: '8px',
            height: '8px',
            animation: `typing 1.4s infinite ${i * 0.2}s`
          }}
        />
      ))}
    </div>
  );

  return (
    <Container fluid className="d-flex flex-column vh-100 p-0">
      {/* Tiêu đề */}
      <div className="welcome-message text-center py-4 d-flex flex-column justify-content-center" style={{ height: '15%' }}>
        <h1 className="display-6 mb-2">Phân tích & Hỏi đáp Shopee</h1>
      </div>

      {/* Khu vực chat */}
      <div 
        ref={chatContainerRef}
        className="flex-grow-1 overflow-auto p-3 bg-light"
        style={{ height: '70%' }}
      >
        {/* Hiển thị tin nhắn */}
        {messages.map((msg, index) => (
          <Message
            key={index}
            content={msg.content}
            time={msg.time}
            isUser={msg.isUser}
          />
        ))}

        {/* Hiệu ứng đang nhập */}
        {isTyping && <TypingIndicator />}
      </div>

      {/* Ô nhập tin nhắn */}
      <div className="input-area bg-white border-top p-3" style={{ minHeight: '80px' }}>
        <Form onSubmit={handleSubmit}>
          <InputGroup style={{ height: '50px' }}> 
            <Form.Control
              as="textarea"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Nhập link sản phẩm Shopee hoặc câu hỏi về Shopee..."
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
                width: '50px', 
                padding: '0' 
              }}
            >
              <FontAwesomeIcon icon={faPaperPlane} />
            </Button>
          </InputGroup>
        </Form>
      </div>

      {/* CSS tùy chỉnh */}
      <style>{`
        .dot {
          animation: typing 1.4s infinite ease-in-out;
        }
        
        @keyframes typing {
          0% { transform: translateY(0); opacity: 0.4; }
          50% { transform: translateY(-5px); opacity: 1; }
          100% { transform: translateY(0); opacity: 0.4; }
        }
        
        @media (max-width: 768px) {
          .welcome-message {
            height: 10% !important;
            padding: 0.5rem !important;
          }
          .welcome-message h1 {
            font-size: 1.5rem !important;
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