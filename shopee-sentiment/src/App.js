import React from 'react';
import { Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './App.css';

// Components
import Sidebar from './components/Sidebar';
// import ChatHeader from './components/ChatHeader';
// import ChatContainer from './components/ChatContainer';
// import InputArea from './components/InputArea';

// Pages
import Home from './pages/Home'; // We will keep Home, but simplify it
import History from './pages/History';
import Saved from './pages/Saved';
import Settings from './pages/Settings';
import About from './pages/About'; // Import the new ChatPage

const App = () => {
  return (
    <div className="app-container">
      {/* Toggle Sidebar Button - chỉ hiển thị trên thiết bị nhỏ */}
      <button className="toggle-sidebar d-md-none" id="toggleSidebar">
        <i className="fas fa-bars"></i>
      </button>

      {/* Sidebar */}
      <div id="sidebar-container">
        <Sidebar />
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* We no longer render ChatHeader, ChatContainer, InputArea directly here */}
        <div id="page-container">
          <Routes>
            <Route path="/" element={<Home />} /> {/* Use ChatPage for the home route */}
            <Route path="/history" element={<History />} />
            <Route path="/saved" element={<Saved />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </div>
        {/* InputArea is now inside ChatPage */}
      </div>
    </div>
  );
};

export default App;
