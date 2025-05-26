import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './App.css';

// Components
import Sidebar from './components/Sidebar';
import PrivateRoute from './components/auth/PrivateRoute'; // Import the PrivateRoute component

// Pages
import Home from './pages/Home'; 
import History from './pages/History';
import Saved from './pages/Saved';
import Settings from './pages/Settings';
import About from './pages/About';
import Login from './components/auth/Login';
import Register from './components/auth/Register';

const App = () => {
  return (
    <div className="app-container">
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* Protected routes */}
        <Route path="/" element={
          <PrivateRoute>
            <MainLayout />
          </PrivateRoute>
        }>
          <Route index element={<Home />} />
          <Route path="/history" element={<History />} />
          <Route path="/saved" element={<Saved />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/about" element={<About />} />
          <Route path="/chat" element={<Home />} />
        </Route>
        
        {/* Redirect to login for any unknown routes */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </div>
  );
};

// MainLayout component that includes sidebar and content
const MainLayout = () => {
  return (
    <>
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
        <div id="page-container">
          <Routes>
            <Route path="/" element={<Home />} /> {/* Use ChatPage for the home route */}
            <Route path="/history" element={<History />} />
            <Route path="/saved" element={<Saved />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </div>
      </div>
    </>
  );
};

export default App;