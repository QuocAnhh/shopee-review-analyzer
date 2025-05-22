import React from "react";
import { Container, Button, Form, Badge } from "react-bootstrap";
import { FaUserCog, FaPalette, FaBell, FaExclamationTriangle, FaTrashAlt } from "react-icons/fa";

const SettingsPage = () => {
  return (
    <div className="settings-page h-100 overflow-auto">
      <Container fluid>
        <div className="settings-content">
          {/* Section: Tài khoản */}
          <div className="settings-section border-bottom p-4">
            <h5 className="d-flex align-items-center mb-4">
              <FaUserCog className="me-2" /> Tài khoản
            </h5>

            <div className="d-flex justify-content-between align-items-center py-2">
              <div className="fw-medium">Thông tin cá nhân</div>
              <Button variant="outline-primary" size="sm">Chỉnh sửa</Button>
            </div>

            <div className="d-flex justify-content-between align-items-center py-2">
              <div className="fw-medium">Gói dịch vụ</div>
              <div>
                <Badge bg="primary">Free</Badge>
                <Button variant="outline-secondary" size="sm" className="ms-2">Nâng cấp</Button>
              </div>
            </div>
          </div>

          {/* Section: Giao diện */}
          <div className="settings-section border-bottom p-4">
            <h5 className="d-flex align-items-center mb-4">
              <FaPalette className="me-2" /> Giao diện
            </h5>

            <div className="d-flex justify-content-between align-items-center py-2">
              <div className="fw-medium">Chủ đề</div>
              <div className="d-flex gap-3">
                <div className="theme-option active" data-theme="light">
                  <div className="theme-preview light border rounded"></div>
                  <span>Sáng</span>
                </div>
                <div className="theme-option" data-theme="dark">
                  <div className="theme-preview dark border rounded"></div>
                  <span>Tối</span>
                </div>
              </div>
            </div>

            <div className="d-flex justify-content-between align-items-center py-2">
              <div className="fw-medium">Ngôn ngữ</div>
              <Form.Select size="sm" defaultValue="Tiếng Việt">
                <option>Tiếng Việt</option>
                <option>English</option>
                <option>中文</option>
              </Form.Select>
            </div>
          </div>

          {/* Section: Thông báo */}
          <div className="settings-section p-4 border-bottom">
            <h5 className="d-flex align-items-center mb-3">
              <FaBell className="me-2" /> Thông báo
            </h5>

            <div className="d-flex justify-content-between align-items-center py-2">
              <div>Thông báo tin nhắn mới</div>
              <Form.Check type="switch" id="notifMessages" defaultChecked />
            </div>

            <div className="d-flex justify-content-between align-items-center py-2">
              <div>Thông báo khuyến mãi</div>
              <Form.Check type="switch" id="notifPromotions" defaultChecked />
            </div>
          </div>

          {/* Section: Danger Zone */}
          <div className="settings-section danger-zone p-4">
            <h5 className="d-flex align-items-center mb-3">
              <FaExclamationTriangle className="me-2" /> Khu vực nguy hiểm
            </h5>
            <div className="d-flex justify-content-between align-items-center py-2">
              <div>Xóa tất cả dữ liệu</div>
              <Button variant="outline-danger" size="sm" id="resetAllData">
                <FaTrashAlt className="me-1" /> Xóa tất cả
              </Button>
            </div>
          </div>
        </div>
      </Container>
    </div>
  );
};

export default SettingsPage;
