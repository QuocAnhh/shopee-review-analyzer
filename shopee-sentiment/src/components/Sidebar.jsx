import React, { useState, useEffect } from "react";
import { Nav, Image, Button } from 'react-bootstrap';
import { useNavigate, useLocation } from 'react-router-dom';
import {
    FaComment,
    FaHistory,
    FaStar,
    FaCog,
    FaInfoCircle,
    FaSignOutAlt,
    FaBars,
} from 'react-icons/fa';

const Sidebar = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
    const [isOpen, setIsOpen] = useState(!isMobile);
    const userData = JSON.parse(localStorage.getItem('user'));
    const userName = userData?.name;

    // Handle window resize
    useEffect(() => {
        const handleResize = () => {
            const mobile = window.innerWidth < 768;
            setIsMobile(mobile);
            setIsOpen(!mobile);
        };

        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    // Handle mobile toggle
    useEffect(() => {
        const toggleBtn = document.getElementById('toggleSidebar');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => setIsOpen(!isOpen));
        }
    }, [isOpen]);

    const handleNavigation = (path) => {
        navigate(path);
        if (isMobile) {
            setIsOpen(false);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('isAuthenticated');
        localStorage.removeItem('accessToken');
        localStorage.removeItem('user');
        window.location.href = '/login';
        };

    const menuItems = [
        { path: '/', icon: <FaComment />, label: 'New Chat' },
        { path: '/history', icon: <FaHistory />, label: 'History' },
        { path: '/saved', icon: <FaStar />, label: 'Saved' },
        { path: '/settings', icon: <FaCog />, label: 'Settings' },
        { path: '/about', icon: <FaInfoCircle />, label: 'About' },
    ];

    return (
        <div
            className={`sidebar bg-white border-end shadow-sm position-fixed h-100 d-flex flex-column ${
                isMobile ? (isOpen ? 'show' : 'hide') : ''
            }`}
            style={{ width: '250px', zIndex: 1000 }}
        >
            {/* Header */}
            <div className="sidebar-header p-3 border-bottom d-flex align-items-center">
                <Image
                    src="./assets/shopee-logo.jpg"
                    alt="Shopee Logo"
                    width={30}
                    height={30}
                    className="me-2"
                    rounded
                />
                <h5 className="mb-0 text-primary">Shopee Chatbot</h5>
            </div>

            {/* Menu */}
            <Nav
                variant="pills"
                className="flex-column p-3 flex-grow-1 overflow-auto"
            >
                {menuItems.map((item) => (
                    <Nav.Item key={item.path}>
                        <Nav.Link
                            onClick={() => handleNavigation(item.path)}
                            active={location.pathname === item.path}
                            className={`d-flex align-items-center py-2 px-3 rounded-end ${
                                location.pathname === item.path 
                                    ? 'bg-primary-light text-primary' 
                                    : 'text-muted'
                            }`}
                            style={{
                                '--primary-light': 'rgba(238, 77, 45, 0.1)',
                                '--primary-color': '#ee4d2d'
                            }}
                        >
                            <span 
                                className={`${
                                    location.pathname === item.path 
                                        ? 'text-primary' 
                                        : 'text-muted'
                                }`}
                            >
                                {item.icon}
                            </span>
                            <span className="ms-2">{item.label}</span>
                        </Nav.Link>
                    </Nav.Item>
                ))}
            </Nav>

            {/* Footer */}
            <div className="p-3 border-top">
                <div className="d-flex align-items-center">
                    <Image
                        src="./assets/user-avatar.jpg"
                        alt="User"
                        width={40}
                        roundedCircle
                        className="me-3"
                    />
                    <div className="flex-grow-1">
                        <h6 className="mb-0">{userName}</h6>
                        <small className="text-muted">Free Plan</small>
                    </div>
                    <Button 
                        variant="link" 
                        size="sm"
                        className="d-flex align-items-center py-2 px-3 rounded-end"
                        onClick={handleLogout}
                    >
                        <FaSignOutAlt />
                    </Button>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;