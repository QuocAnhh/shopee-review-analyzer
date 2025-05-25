import React from "react";
import { useState } from "react";
import {Card, Stack, Badge} from 'react-bootstrap';

const ChatContainer = () => {
     const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

    const Message = ({ content, time, isUser}) => (
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
                <div className="message-contenr">{content}</div>
            </Card>
            <small className="text-muted">{time}</small>
        </Stack>
    );

    // Template cho typing indicator
    const TypingIndicator = () => (
        <div className="d-flex align-item-center p-2 bg-white rounded-3 shadow-sm mb-3">
            {[...Array(3)].map((_, i) => (
                <span
                    key={i}
                    className="dot bg-secondary rounded-cicle mx-1"
                    style={{
                        width: '8px',
                        height: '8px',
                        animation: `typing 1.4s ìninite ${i * 0.2}s`
                    }}
                />
            ))}
        </div>
    );

    return (
        <div
            id="chatContainer"
            className="chat-container p-3 overflow-auto"
            style={{
                height: 'calc(100vh - 150px)',
                backgroundColor: 'f8f9fa'
            }}
        >
            {/* Hiển thị message */}
            {messages.map((msg, index) => (
                <Message
                    key={index}
                    content={msg.content}
                    time={msg.time}
                    isUser={msg.isUser}
                />
            ))}

            {/* Hiển thị typing indicator khi cần */}
            {isTyping && <TypingIndicator/>}

            {/* Thêm CSS animatiom cjo typing indicator */}
            // Thêm media query cho mobile
        <style>{`
            @media (max-width: 768px) {
                .welcome-message {
                height: 15% !important;
                padding: 1rem !important;
                }
                .welcome-message h1 {
                font-size: 1.8rem !important;
                }
                .chat-message {
                max-width: 90% !important;
                }
            }
        `}</style>
        </div>
    )
}

export default ChatContainer;