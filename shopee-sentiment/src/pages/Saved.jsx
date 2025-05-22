import React, { useState } from 'react';
import { Container, Dropdown, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSort, faStar, faEye } from '@fortawesome/free-solid-svg-icons';

const SavedPage = () => {
  const [sortBy, setSortBy] = useState('newest');
  const [savedItems, setSavedItems] = useState([]); // Empty array for no saved items state

  // Sample data - uncomment to test with saved items
  // const [savedItems, setSavedItems] = useState([
  //   {
  //     id: 1,
  //     title: "Hướng dẫn đổi trả hàng",
  //     content: "Để đổi trả hàng, bạn cần giữ nguyên trạng thái sản phẩm và liên hệ trong vòng 7 ngày...",
  //     date: "2 giờ trước",
  //     isSaved: true
  //   },
  //   {
  //     id: 2,
  //     title: "Thông tin khuyến mãi tháng 12",
  //     content: "Tháng 12 này có chương trình giảm giá 50% cho tất cả sản phẩm điện tử...",
  //     date: "Hôm qua",
  //     isSaved: true
  //   }
  // ]);

  const handleSort = (sortType) => {
    setSortBy(sortType);
    // Implement sorting logic here
    console.log(`Sorting by: ${sortType}`);
  };

  const handleView = (id) => {
    console.log(`Viewing saved item ${id}`);
    // Implement view logic
  };

  const handleUnsave = (id) => {
    setSavedItems(savedItems.filter(item => item.id !== id));
    console.log(`Unsaved item ${id}`);
  };

  return (
    <div className="saved-page">
      <Container fluid>
        {/* Header with sort dropdown */}
        <div className="saved-header py-3">
          <div className="saved-actions">
            <Dropdown>
              <Dropdown.Toggle variant="outline-secondary" size="sm" id="dropdown-sort">
                <FontAwesomeIcon icon={faSort} className="me-1" /> Sắp xếp
              </Dropdown.Toggle>
              <Dropdown.Menu>
                <Dropdown.Item 
                  active={sortBy === 'newest'}
                  onClick={() => handleSort('newest')}
                >
                  Mới nhất
                </Dropdown.Item>
                <Dropdown.Item 
                  active={sortBy === 'oldest'}
                  onClick={() => handleSort('oldest')}
                >
                  Cũ nhất
                </Dropdown.Item>
                <Dropdown.Item 
                  active={sortBy === 'alphabet'}
                  onClick={() => handleSort('alphabet')}
                >
                  Theo tên
                </Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          </div>
        </div>
        
        {/* Saved items list */}
        {savedItems.length > 0 ? (
          <div className="saved-list">
            {savedItems.map(item => (
              <div key={item.id} className="saved-item mb-3 p-3 border rounded">
                <div className="saved-item-header d-flex justify-content-between mb-2">
                  <div className="saved-title fw-bold">{item.title}</div>
                  <div className="saved-date text-muted small">{item.date}</div>
                </div>
                <div className="saved-content text-muted mb-3">{item.content}</div>
                <div className="saved-item-actions d-flex justify-content-between">
                  <Button 
                    variant="outline-primary" 
                    size="sm"
                    onClick={() => handleView(item.id)}
                  >
                    <FontAwesomeIcon icon={faEye} className="me-1" /> Xem
                  </Button>
                  <Button 
                    variant="outline-secondary" 
                    size="sm"
                    onClick={() => handleUnsave(item.id)}
                  >
                    <FontAwesomeIcon icon={faStar} />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          /* Empty state */
          <div className="no-saved text-center py-5">
            <FontAwesomeIcon icon={faStar} className="fa-3x mb-3 text-muted" />
            <h5>Không có tin nhắn nào được lưu</h5>
            <p className="text-muted">
              Bạn có thể lưu tin nhắn quan trọng bằng cách nhấn vào biểu tượng {' '}
              <FontAwesomeIcon icon={faStar} />
            </p>
          </div>
        )}
      </Container>
    </div>
  );
};

export default SavedPage;