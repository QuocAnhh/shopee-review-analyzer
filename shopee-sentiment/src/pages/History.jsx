import React, { useState, useEffect } from 'react';
import {
  Container,
  InputGroup,
  Form,
  Card,
  Button,
  Spinner,
  Alert,
} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faTrash, faArrowRight } from '@fortawesome/free-solid-svg-icons';
import { useNavigate } from 'react-router-dom';
import { fetchHistory, deleteChat, getChatById } from '../api/history';
import { authHeaders } from '../api/history';

const HistoryPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [historyItems, setHistoryItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null); // New state for error messages
  const navigate = useNavigate();

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await fetchHistory();
        setHistoryItems(data);
      } catch (error) {
        console.error('Lỗi khi tải lịch sử:', error);
        setErrorMessage('Không thể tải lịch sử trò chuyện. Vui lòng thử lại.');
        setHistoryItems([]);
      } finally {
        setLoading(false);
      }
    };

    loadHistory();
  }, []);

  const handleReopen = async (id) => {
    try {
      setLoading(true);
      
      // Kích hoạt chat trước
      const activateResponse = await fetch(`/api/chats/${id}`, {
        method: 'PUT',
        headers: authHeaders(),
        body: JSON.stringify({ set_active: true })
      });
      
      if (!activateResponse.ok) {
        throw new Error('Không thể kích hoạt trò chuyện');
      }
      
      // Sau đó tải dữ liệu chat
      const chatData = await getChatById(id);
      
      // Chuyển hướng với state
      navigate(`/chat?history=${id}`, { 
        state: { messages: chatData.messages } 
      });
      
    } catch (error) {
      console.error('Lỗi khi mở lại trò chuyện:', error);
      setErrorMessage(error.message || 'Không thể mở lại cuộc trò chuyện');
      setHistoryItems(prev => prev.filter(item => item.id !== id));
    } finally {
      setLoading(false);
    }
  };
  
  const handleDelete = async (id) => {
    if (!window.confirm('Bạn chắc chắn muốn xóa?')) return;

    setDeletingId(id);
    try {
      await deleteChat(id);
      setHistoryItems((prev) => prev.filter((item) => item.id !== id));
    } catch (error) {
      console.error('Lỗi khi xóa:', error);
      setErrorMessage('Xóa cuộc trò chuyện thất bại. Vui lòng thử lại.');
    } finally {
      setDeletingId(null);
    }
  };

  const filteredItems = historyItems.filter((item) =>
    item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (item.preview || '').toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Container className="py-4">
      <h2 className="mb-4 text-center">Lịch sử trò chuyện</h2>

      {/* Error Message */}
      {errorMessage && (
        <Alert variant="danger" onClose={() => setErrorMessage(null)} dismissible>
          {errorMessage}
        </Alert>
      )}

      {/* Tìm kiếm */}
      <div className="mb-4">
        <InputGroup>
          <InputGroup.Text>
            <FontAwesomeIcon icon={faSearch} />
          </InputGroup.Text>
          <Form.Control
            type="text"
            placeholder="Tìm theo tiêu đề hoặc nội dung..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </InputGroup>
      </div>

      {/* Loading */}
      {loading ? (
        <div className="text-center my-5">
          <Spinner animation="border" variant="primary" />
          <p className="mt-2">Đang tải lịch sử...</p>
        </div>
      ) : filteredItems.length === 0 ? (
        <Card className="text-center py-4 bg-light">
          <Card.Body>
            {historyItems.length === 0 ? (
              <span>Bạn chưa có cuộc trò chuyện nào</span>
            ) : (
              <span>Không tìm thấy kết quả phù hợp</span>
            )}
          </Card.Body>
        </Card>
      ) : (
        filteredItems.map((item) => (
          <Card key={item.id} className="mb-3 shadow-sm">
            <Card.Body className="d-flex justify-content-between align-items-center">
              <div style={{ cursor: 'pointer' }} onClick={() => handleReopen(item.id)}>
                <Card.Title>{item.title || 'Không có tiêu đề'}</Card.Title>
                <Card.Text className="text-muted small">
                  {item.preview || 'Không có nội dung xem trước'}
                </Card.Text>
                <small className="text-muted">
                  {new Date(item.created_at).toLocaleString()}
                </small>
              </div>
              <div className="d-flex gap-2">
                <Button
                  variant="outline-primary"
                  size="sm"
                  onClick={() => handleReopen(item.id)}
                  title="Mở lại"
                >
                  <FontAwesomeIcon icon={faArrowRight} />
                </Button>
                <Button
                  variant="outline-danger"
                  size="sm"
                  onClick={() => handleDelete(item.id)}
                  title="Xóa"
                  disabled={deletingId === item.id}
                >
                  {deletingId === item.id ? (
                    <Spinner animation="border" size="sm" />
                  ) : (
                    <FontAwesomeIcon icon={faTrash} />
                  )}
                </Button>
              </div>
            </Card.Body>
          </Card>
        ))
      )}
    </Container>
  );
};

export default HistoryPage;