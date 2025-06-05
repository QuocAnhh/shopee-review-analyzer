import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './App.css';
import { Outlet } from 'react-router-dom';

// Components
import Sidebar from './components/Sidebar';
import PrivateRoute from './components/auth/PrivateRoute';

// Pages
import Home from './pages/Home'; 
import History from './pages/History';
import Saved from './pages/Saved';
import Settings from './pages/Settings';
import About from './pages/About';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Intro from './pages/Intro.tsx';
import TrialInfo from './pages/TrialInfo';

const App = () => {
  return (
    <div className="app-container">
      <Routes>
        {/* Public routes */}
        <Route path="/intro" element={<Intro />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/trial-info" element={<TrialInfo />} />
        
        {/* Protected routes */}
        <Route path="/" element={
          <PrivateRoute>
            <MainLayout />
          </PrivateRoute>
        }>
          <Route path="chat" element={<Home />} />
          <Route path="history" element={<History />} />
          <Route path="saved" element={<Saved />} />
          <Route path="settings" element={<Settings />} />
          <Route path="about" element={<About />} />
          <Route index element={<Navigate to="/chat" replace />} />
        </Route>
        
        <Route path="*" element={<Navigate to="/intro" replace />} />
      </Routes>
    </div>
  );
};

const MainLayout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  useEffect(() => {
    const toggleBtn = document.getElementById('toggleSidebar');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => setIsSidebarOpen(!isSidebarOpen));
    }
  }, [isSidebarOpen]);

  return (
    <>
      <button 
        className={`toggle-sidebar d-md-none ${isSidebarOpen ? 'd-none' : ''}`} 
        id="toggleSidebar"
      >
        <i className="bi bi-list"></i>
      </button>

      <div id="sidebar-container">
        <Sidebar onToggle={(isOpen) => setIsSidebarOpen(isOpen)} />
      </div>

      <div className="main-content">
        <div id="page-container">
          <Outlet />
        </div>
      </div>
    </>
  );
};

export default App;