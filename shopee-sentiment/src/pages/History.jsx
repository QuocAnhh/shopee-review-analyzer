import React, { useState, useEffect } from 'react';
import { Container, InputGroup, Form, Card, Button, Spinner } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faTrash, faSyncAlt, faArrowRight } from '@fortawesome/free-solid-svg-icons';
import { useNavigate } from 'react-router-dom';

const HistoryPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [historyItems, setHistoryItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch('/api/history', {
          credentials: 'include'
        });
        const data = await response.json();
        setHistoryItems(data);
      } catch (error) {
        console.error('Error fetching history:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const handleReopen = (id) => {
     navigate(`/?history=${id}`);
  };

  const handleDelete = async (id) => {
    try {
      await fetch(`/api/history/${id}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      setHistoryItems(historyItems.filter(item => item.id !== id));
    } catch (error) {
      console.error('Error deleting history:', error);
    }
  };

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
  };

  const filteredItems = historyItems.filter(item =>
    item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (item.preview || '').toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="history-page h-100 overflow-auto bg-light">
      <Container className="py-4">
        <h2 className="mb-4 text-center">Lịch sử trò chuyện</h2>

        {/* Search Box */}
        <div className="search-box mb-4">
          <InputGroup>
            <InputGroup.Text>
              <FontAwesomeIcon icon={faSearch} />
            </InputGroup.Text>
            <Form.Control
              type="text"
              placeholder="Tìm kiếm trong lịch sử..."
              value={searchQuery}
              onChange={handleSearch}
            />
          </InputGroup>
        </div>

        {/* Loading Spinner */}
        {loading ? (
          <div className="text-center my-5">
            <Spinner animation="border" />
            <p className="mt-2">Đang tải lịch sử...</p>
          </div>
        ) : (
          <>
            {filteredItems.length === 0 ? (
              <p className="text-muted text-center">Không tìm thấy cuộc trò chuyện nào.</p>
            ) : (
              filteredItems.map((item) => (
                <Card key={item.id} className="mb-3 shadow-sm">
                  <Card.Body className="d-flex justify-content-between align-items-center">
                    <div>
                      <Card.Title>{item.title}</Card.Title>
                      <Card.Text className="text-muted small">
                        {item.preview || 'Không có nội dung xem trước'}
                      </Card.Text>
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
                        title="Xoá"
                      >
                        <FontAwesomeIcon icon={faTrash} />
                      </Button>
                    </div>
                  </Card.Body>
                </Card>
              ))
            )}
          </>
        )}
      </Container>
    </div>
  );
};

export default HistoryPage;
