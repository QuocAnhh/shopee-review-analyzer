import React from 'react';
import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const TrialInfo = () => {
  return (
    <Container className="my-5">
      <Row className="justify-content-center">
        <Col md={8} lg={6}>
          <Card className="shadow-sm">
            <Card.Body className="p-4 text-center">
              <h2 className="mb-4">Bản dùng thử miễn phí</h2>
              <p className="text-muted mb-4">
                Trải nghiệm đầy đủ các tính năng phân tích đánh giá của chúng tôi trong một thời gian giới hạn.
              </p>
              <p className="text-muted mb-4">
                Với bản dùng thử, bạn có thể:
              </p>
              <ul className="list-unstyled text-start mx-auto mb-4" style={{ maxWidth: '300px' }}>
                <li>✅ Phân tích đánh giá sản phẩm</li>
                <li>✅ Xem báo cáo chi tiết</li>
                <li>✅ Sử dụng các module AI</li>
                <li>... và nhiều hơn nữa!</li>
              </ul>
              <Button as={Link} to="/register" variant="primary" size="lg" className="mt-3">
                Bắt đầu dùng thử ngay
              </Button>
              <p className="mt-3 text-muted">
                Đã có tài khoản? <Link to="/login">Đăng nhập</Link>
              </p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default TrialInfo; 