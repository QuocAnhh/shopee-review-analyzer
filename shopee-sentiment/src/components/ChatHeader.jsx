import React from 'react';
import { Button, Container } from 'react-bootstrap';
import { FaArrowLeft } from 'react-icons/fa';

const ChatHeader = ({ onBackClick, title = "Shopee Assistant" }) => {
  return (
    <div className="chat-header p-3 border-bottom">
      <Container fluid className="d-flex align-items-center">
        {/* Back button (visible only on mobile) */}
        <Button
          variant="outline-secondary"
          size="sm"
          className="me-2 d-lg-none"
          onClick={onBackClick}
          aria-label="Back"
        >
          <FaArrowLeft />
        </Button>
        
        {/* Chat title */}
        <h3 className="mb-0 flex-grow-1">{title}</h3>
      </Container>
    </div>
  );
};

export default ChatHeader;