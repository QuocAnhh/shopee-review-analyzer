import React, {useState} from "react";
import {InputGroup, FormControl, Button, Badge, Fade} from 'react-bootstrap';
import { FaPaperclip, FaPaperPlane } from 'react-icons/fa';

const InputArea = ({ onSendMessage, suggestions = []}) => {
    const [message, setMessage] = useState('');
    const handleSend = () => {
        if(message.trim()) {
            onSendMessage(message);
            setMessage('');
        }
    };

    handleKeyPress = (e) => {
        if(e.key === 'Enter') {
            handleSend();
        }
    }

    const handleSuggestionClick = (suggestion) => {
        setMessage(suggestion);
    };

    return (
        <div className="input-area bg-white border-top p-3">
            <InputGroup>
                <Button variant="outline-secondary" id="attach-btn">
                    <FaPaperclip/>
                </Button>

                <FormControl
                    type="text"
                    className="message-input"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Nhập tin nhắn của bạn..."
                    autoComplete="off"
                />
                <Button
                    variant="primary"
                    className="send-btn"
                    onClick={handleSend}
                    disabled={!message.trim()}
                >
                    <FaPaperPlane />
                </Button>
            </InputGroup>

            {suggestions.length > 0 &&(
                <div className="input-suggestions mt-2 d-flex flex-wrap gap-2">
                    {suggestions.map((suggestion, index) => (
                        <Badge
                            key={index}
                            pill
                            bg="light"
                            text="dark"
                            className="suggestion-item cursor-pointer"
                            onClick={() => handleSuggestionClick(suggestion)}
                        >
                            {suggestion}
                        </Badge>
                    ))}
                </div>
            )}
        </div>
    );
};

// Default props
InputArea.defaultProps = {
    suggestion: [
        'Kiểm tra đơn hàng',
        'Tìm sản phẩm',
        'Hỗ trợ đổi trả'
    ]
}

export default InputArea;