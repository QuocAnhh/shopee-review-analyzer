import React, { useState } from 'react';
import { Container, InputGroup, Form, Card, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faTrash, faSyncAlt } from '@fortawesome/free-solid-svg-icons';

const HistoryPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  
  // Sample history data
  const [historyItems, setHistoryItems] = useState([
    {
      id: 1,
      title: "Hỏi về đơn hàng #12345",
      preview: "Tôi muốn kiểm tra tình trạng đơn hàng của mình...",
      time: "2 giờ trước"
    },
    {
      id: 2,
      title: "Tìm sản phẩm điện thoại",
      preview: "Bạn có thể giới thiệu điện thoại tầm 5 triệu...",
      time: "Hôm qua"
    },
    {
      id: 3,
      title: "Hỏi về chính sách đổi trả",
      preview: "Tôi muốn biết chính sách đổi trả sản phẩm...",
      time: "3 ngày trước"
    },
    {
      id: 4,
      title: "Khuyến mãi tháng 10",
      preview: "Có chương trình khuyến mãi nào trong tháng 10...",
      time: "1 tuần trước"
    }
  ]);

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
    // In a real app, you would filter the history items here
  };

  const handleReopen = (id) => {
    console.log(`Reopening conversation ${id}`);
    // Implement reopen logic
  };

  const handleDelete = (id) => {
    setHistoryItems(historyItems.filter(item => item.id !== id));
  };

  // Filter history items based on search query
  const filteredItems = historyItems.filter(item =>
    item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.preview.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="history-page h-100 overflow-auto">
      <Container className="py-4">
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
        
        {/* History List */}
        <div className="history-list">
          {filteredItems.length > 0 ? (
            filteredItems.map(item => (
              <Card key={item.id} className="mb-3 shadow-sm">
                <Card.Body>
                  <div className="d-flex justify-content-between align-items-center">
                    <h5 className="card-title mb-1">{item.title}</h5>
                    <small className="text-muted">{item.time}</small>
                  </div>
                  <p className="card-text text-muted mb-2">{item.preview}</p>
                  <div className="d-flex">
                    <Button 
                      variant="outline-primary" 
                      size="sm" 
                      className="me-2"
                      onClick={() => handleReopen(item.id)}
                    >
                      <FontAwesomeIcon icon={faSyncAlt} className="me-1" />
                      Mở lại
                    </Button>
                    <Button 
                      variant="outline-danger" 
                      size="sm"
                      onClick={() => handleDelete(item.id)}
                    >
                      <FontAwesomeIcon icon={faTrash} className="me-1" />
                      Xóa
                    </Button>
                  </div>
                </Card.Body>
              </Card>
            ))
          ) : (
            <div className="text-center py-5 text-muted">
              Không tìm thấy kết quả phù hợp
            </div>
          )}
        </div>
      </Container>
    </div>
  );
};

export default HistoryPage;