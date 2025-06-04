import React, { useState, useRef, useEffect } from 'react';
import { Container, Form, InputGroup, Button, Card, Stack, Alert } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';
import { useLocation, useNavigate } from 'react-router-dom';
import { authHeaders } from '../api/history';

const ChatInterface = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const chatContainerRef = useRef(null);
  const location = useLocation();
  const navigate = useNavigate();
  const [currentChatId, setCurrentChatId] = useState(null);

  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      .keyword-highlight-high {
        background-color: #ff6b6b !important;
        color: white !important;
        padding: 2px 4px;
        border-radius: 3px;
        font-weight: bold;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
      }
      .keyword-highlight-medium {
        background-color: #ffa726 !important;
        color: white !important;
        padding: 2px 4px;
        border-radius: 3px;
        font-weight: bold;
      }
      .keyword-highlight {
        background-color: #42a5f5 !important;
        color: white !important;
        padding: 1px 3px;
        border-radius: 3px;
      }
      .chart-container img {
        max-width: 100% !important;
        height: auto !important;
        width: 400px !important;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      }
    `;
    document.head.appendChild(style);
    
    return () => {
      document.head.removeChild(style);
    };
  }, []);

  useEffect(() => {
    const loadHistory = async () => {
      const params = new URLSearchParams(location.search);
      const historyId = params.get('history');
      
      if (historyId) {
        try {
          const token = localStorage.getItem('accessToken');
          if (!token) {
            setErrorMessage('Vui lòng đăng nhập để xem lịch sử trò chuyện.');
            navigate('/login');
            return;
          }

          const response = await fetch(`/api/chats/${historyId}`, {
            headers: authHeaders()
          });
          
          if (!response.ok) {
            const errorData = await response.json();
            if (response.status === 401) {
              setErrorMessage('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.');
              localStorage.removeItem('accessToken');
              navigate('/login');
              return;
            }
            if (response.status === 404) {
              setErrorMessage('Không tìm thấy cuộc trò chuyện.');
              return;
            }
            throw new Error(errorData.error || 'Không thể tải lịch sử trò chuyện.');
          }
          
          const data = await response.json();
          setMessages(data.messages);
          setCurrentChatId(historyId);
        } catch (error) {
          console.error('Lỗi khi tải lịch sử:', error);
          setErrorMessage(error.message || 'Không thể tải lịch sử trò chuyện. Vui lòng thử lại.');
        }
      }
    };
    
    loadHistory();
  }, [location, navigate]);

  // Lưu hoặc cập nhật chat history
  const saveChatHistory = async (title, retries = 3) => {
    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        const endpoint = currentChatId ? '/api/chats/active' : '/api/chats/new';
        const method = currentChatId ? 'PUT' : 'POST';
        
        const response = await fetch(endpoint, {
          method,
          headers: authHeaders(),
          body: JSON.stringify({ 
            messages, 
            title: title || `Chat ${new Date().toLocaleString()}`
          })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
          throw new Error(data.error || 'Failed to save chat');
        }
        
        if (!currentChatId && data.chat_id) {
          setCurrentChatId(data.chat_id);
        }
        
        return data;
      } catch (error) {
        console.error(`Attempt ${attempt} failed:`, error);
        if (attempt === retries) {
          setErrorMessage('Không thể lưu lịch sử trò chuyện sau nhiều lần thử.');
          throw error;
        }
        await new Promise(resolve => setTimeout(resolve, 1000)); // Đợi 1 giây trước khi thử lại
      }
    }
  };

  // Lưu lịch sử khi messages thay đổi
  useEffect(() => {
    if (messages.length > 0) {
      const firstUserMessage = messages.find(m => m.isUser);
      saveChatHistory(firstUserMessage?.content.substring(0, 50) || 'New Chat');
    }
  }, [messages]);

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

      // Phân tích sản phẩm với 3 module chính
      if (data.summary && (data.demo_reviews || data.file_path)) {
        if (data.product_image) {
          botResponse += `<div style="text-align: center; margin-bottom: 15px;"><img src="${data.product_image}" style="max-width: 300px; max-height: 300px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" alt="Product Image"></div>`;
        }
        
        if (data.product_name) {
          botResponse += `<h5 style="color: #e74c3c; margin-bottom: 15px; text-align: center;">🛍️ ${data.product_name}</h5>`;
        }
        
        if (data.crawled_data_info) {
          const info = data.crawled_data_info;
          botResponse += `
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #007bff;">
              <h6 style="color: #007bff; margin-bottom: 10px;">📊 MODULE 1: THÔNG TIN DỮ LIỆU ĐÃ CRAWL</h6>
              <p><strong>Tổng số reviews:</strong> ${info.total_reviews}</p>
              <p><strong>Độ dài trung bình:</strong> ${info.average_length} ký tự</p>
              <p><strong>Chất lượng dữ liệu:</strong> <span style="color: ${info.data_quality.includes('Tốt') ? '#27ae60' : info.data_quality.includes('Khá') ? '#f39c12' : '#e74c3c'};">${info.data_quality}</span></p>
              ${info.file_info ? `<p><strong>File info:</strong> ${info.file_info}</p>` : ''}
            </div>
          `;
          
          if (info.sample_reviews && info.sample_reviews.length > 0) {
            botResponse += `
              <div style="background: #e8f4fd; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                <h6 style="color: #0066cc; margin-bottom: 10px;">📝 Mẫu dữ liệu crawl (${info.sample_reviews.length} reviews đầu tiên)</h6>
                <ul style="margin: 0; padding-left: 20px;">
            `;
            info.sample_reviews.forEach(review => {
              botResponse += `<li style="margin-bottom: 8px; font-size: 14px;">${review.substring(0, 100)}${review.length > 100 ? '...' : ''}</li>`;
            });
            botResponse += '</ul></div>';
          }
        }
        
        botResponse += `<b>📝 Tóm tắt:</b> <br>${data.summary}<br><br>`;
        
        if (data.keywords && data.keywords.length > 0) {
          botResponse += '<b>🔍 Từ khóa quan trọng:</b> ';
          data.keywords.slice(0, 10).forEach((keyword, index) => {
            botResponse += `<span style="background: #3498db; color: white; padding: 2px 6px; border-radius: 12px; margin: 2px; font-size: 12px;">${keyword[0]} (${keyword[1]})</span> `;
          });
          botResponse += '<br><br>';
        }
        
        if (data.file_path) {
          botResponse += `<b>📁 File dữ liệu crawl:</b> <a href='${data.file_path}' download target='_blank' style="color: #3498db;">Tải file dữ liệu vừa crawl</a><br><br>`;
        }
        
        console.log('DEBUG: data.demo_reviews_with_highlights =', data.demo_reviews_with_highlights);
        console.log('DEBUG: data.overall_assessment =', data.overall_assessment);
        
        if (data.demo_reviews_with_highlights) {
          const demoData = data.demo_reviews_with_highlights;
          
          botResponse += `
            <div style="background: #f0f8ff; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #007bff;">
              <h6 style="color: #007bff; margin-bottom: 10px;">🎯 MODULE 2: PHÂN TÍCH TỪ KHÓA DEMO REVIEWS</h6>
          `;
          
          if (demoData.keywords_analysis) {
            if (demoData.keywords_analysis.positive_keywords) {
              botResponse += '<p><strong>Từ khóa tích cực:</strong> ';
              demoData.keywords_analysis.positive_keywords.slice(0, 5).forEach(kw => {
                botResponse += `<span style="background: #27ae60; color: white; padding: 2px 6px; border-radius: 12px; margin: 2px; font-size: 12px;">${kw[0]}</span> `;
              });
              botResponse += '</p>';
            }
            
            if (demoData.keywords_analysis.negative_keywords) {
              botResponse += '<p><strong>Từ khóa tiêu cực:</strong> ';
              demoData.keywords_analysis.negative_keywords.slice(0, 5).forEach(kw => {
                botResponse += `<span style="background: #e74c3c; color: white; padding: 2px 6px; border-radius: 12px; margin: 2px; font-size: 12px;">${kw[0]}</span> `;
              });
              botResponse += '</p>';
            }
          }
          
          botResponse += '</div>';
          
          if (demoData.positive_reviews && demoData.positive_reviews.length > 0) {
            botResponse += `
              <div style="background: #d5f4e6; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                <h6 style="color: #27ae60; margin-bottom: 10px;">😊 5 REVIEWS TÍCH CỰC (Với từ khóa được highlight)</h6>
                <ul style="margin: 0; padding-left: 20px;">
            `;
            demoData.positive_reviews.forEach((review, index) => {
              botResponse += `<li style="margin-bottom: 12px; line-height: 1.5;">${review.highlighted}</li>`;
            });
            botResponse += '</ul></div>';
          }
          
          if (demoData.negative_reviews && demoData.negative_reviews.length > 0) {
            botResponse += `
              <div style="background: #fadbd8; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                <h6 style="color: #e74c3c; margin-bottom: 10px;">😞 5 REVIEWS TIÊU CỰC (Với từ khóa được highlight)</h6>
                <ul style="margin: 0; padding-left: 20px;">
            `;
            demoData.negative_reviews.forEach((review, index) => {
              botResponse += `<li style="margin-bottom: 12px; line-height: 1.5;">${review.highlighted}</li>`;
            });
            botResponse += '</ul></div>';
          }
        }
        
        if (data.chart_url) {
          botResponse += `<br><div class="chart-container"><img src='${data.chart_url}' style='max-width:100%; border-radius:8px; margin: 10px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'></div>`;
        }
        
        if (data.overall_assessment) {
          const assessment = data.overall_assessment;
          
          let scoreColor = '#e74c3c';
          if (assessment.overall_score >= 8) scoreColor = '#27ae60';
          else if (assessment.overall_score >= 6) scoreColor = '#f39c12';
          else if (assessment.overall_score >= 4) scoreColor = '#f1c40f';
          
          botResponse += `
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 12px; margin: 20px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
              <h5 style="margin-bottom: 15px; text-align: center;">🏆 MODULE 3: ĐÁNH GIÁ TỔNG THỂ CUỐI CÙNG</h5>
              
              <div style="text-align: center; margin-bottom: 15px;">
                <div style="background: rgba(255,255,255,0.2); border-radius: 50px; padding: 10px 20px; display: inline-block;">
                  <span style="font-size: 24px; font-weight: bold; color: ${scoreColor};">${assessment.overall_score}/10</span>
                  <span style="margin-left: 10px; font-size: 16px;">${assessment.recommendation}</span>
                </div>
              </div>
              
              ${assessment.sentiment_distribution ? `
                <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 15px;">
                  <p style="margin: 5px 0;"><strong>📊 Phân bố cảm xúc:</strong></p>
                  <p style="margin: 0;">
                    😊 Tích cực: ${assessment.sentiment_distribution.positive} | 
                    😐 Trung tính: ${assessment.sentiment_distribution.neutral} | 
                    😞 Tiêu cực: ${assessment.sentiment_distribution.negative}
                  </p>
                </div>
              ` : ''}
              
              ${assessment.key_points && assessment.key_points.length > 0 ? `
                <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 15px;">
                  <p style="margin-bottom: 8px;"><strong>🔑 Điểm chính:</strong></p>
                  <ul style="margin: 0; padding-left: 20px;">
                    ${assessment.key_points.map(point => `<li style="margin-bottom: 5px;">${point}</li>`).join('')}
                  </ul>
                </div>
              ` : ''}
              
              ${assessment.detailed_analysis ? `
                <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 15px;">
                  <p style="margin-bottom: 8px;"><strong>📋 Phân tích chi tiết:</strong></p>
                  <p style="margin: 0; line-height: 1.5;">${assessment.detailed_analysis}</p>
                </div>
              ` : ''}
              
              ${assessment.buying_advice ? `
                <div style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px; border: 2px dashed rgba(255,255,255,0.3);">
                  <p style="margin-bottom: 5px;"><strong>💡 Lời khuyên mua hàng:</strong></p>
                  <p style="margin: 0; font-style: italic; line-height: 1.5;">${assessment.buying_advice}</p>
                </div>
              ` : ''}
            </div>
          `;
        }
        
        if (data.suggested_questions && data.suggested_questions.length > 0) {
          botResponse += '<br><b>💡 Câu hỏi gợi ý:</b><br>';
          data.suggested_questions.forEach((question, index) => {
            botResponse += `<button style="background: #f8f9fa; border: 1px solid #dee2e6; padding: nhà 8px 12px; margin: 4px; border-radius: 20px; cursor: pointer; font-size: 14px;" onclick="document.querySelector('input[type=text]').value='${question}'; document.querySelector('form').requestSubmit();">${question}</button> `;
          });
        }
      }
      else if (data.answer) {
        botResponse = `<b>💬 Trả lời:</b><br>${data.answer}`;
        
        if (data.suggested_questions && data.suggested_questions.length > 0) {
          botResponse += '<br><br><b>💡 Câu hỏi gợi ý:</b><br>';
          data.suggested_questions.forEach((question, index) => {
            botResponse += `<button style="background: #f8f9fa; border: 1px solid #dee2e6; padding: 8px 12px; margin: 4px; border-radius: 20px; cursor: pointer; font-size: 14px;" onclick="document.querySelector('input[type=text]').value='${question}'; document.querySelector('form').requestSubmit();">${question}</button> `;
          });
        }
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
    
    const userMessage = {
      content: message,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      isUser: true
    };
    
    setMessages(prev => [...prev, userMessage]);
    setMessage('');
    
    if (!currentChatId) {
      try {
        const response = await fetch('/api/chats/new', {
          method: 'POST',
          headers: authHeaders(),
          body: JSON.stringify({ initial_message: message })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Failed to create chat');
        setCurrentChatId(data.chat_id);
      } catch (error) {
        console.error('Error creating chat:', error);
        setErrorMessage('Không thể tạo cuộc trò chuyện mới.');
        return;
      }
    }
    
    const botResponse = await askShopee(message);
    setMessages(prev => [...prev, {
      ...botResponse,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }]);
  };

  useEffect(() => {
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
      {errorMessage && (
        <Alert variant="danger" onClose={() => setErrorMessage(null)} dismissible>
          {errorMessage}
        </Alert>
      )}

      <div className="welcome-message text-center py-4 d-flex flex-column justify-content-center" style={{ height: '15%' }}>
        <h1 className="display-6 mb-2">Phân tích & Hỏi đáp Shopee</h1>
      </div>

      <div 
        ref={chatContainerRef}
        className="flex-grow-1 overflow-auto p-3 bg-light"
        style={{ height: '70%' }}
      >
        {messages.map((msg, index) => (
          <Message
            key={index}
            content={msg.content}
            time={msg.time}
            isUser={msg.isUser}
          />
        ))}
        {isTyping && <TypingIndicator />}
      </div>

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

      <style>{`
        .dot {
          animation: typing 1.4s infinite ease-in-out;
        }
        
        @keyframes typing {
          0% { transform: translateY(0); opacity: 0.4; }
          50% { transform: translateY(-5px); opacity: 1; }
          100% { transform: translateY(0); opacity: 0.4; }
        }
        
        .keyword-highlight {
          background-color: #fff3cd;
          border: 1px solid #ffeaa7;
          border-radius: 3px;
          padding: 1px 4px;
          font-weight: 500;
          color: #856404;
        }
        
        .keyword-highlight-medium {
          background-color: #d1ecf1;
          border: 1px solid #74c0fc;
          border-radius: 3px;
          padding: 1px 4px;
          font-weight: 600;
          color: #0c5460;
        }
        
        .keyword-highlight-high {
          background-color: #d4edda;
          border: 1px solid #6bcf7f;
          border-radius: 3px;
          padding: 1px 4px;
          font-weight: 700;
          color: #155724;
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