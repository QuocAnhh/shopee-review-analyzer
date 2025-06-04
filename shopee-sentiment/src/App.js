import React from 'react';
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

const App = () => {
  return (
    <div className="app-container">
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        <Route path="/" element={
          <PrivateRoute>
            <MainLayout />
          </PrivateRoute>
        }>
          <Route index element={<Home />} />
          <Route path="history" element={<History />} />
          <Route path="saved" element={<Saved />} />
          <Route path="settings" element={<Settings />} />
          <Route path="about" element={<About />} />
          <Route path="chat" element={<Home />} />
        </Route>
        
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </div>
  );
};

const MainLayout = () => {
  return (
    <>
      <button className="toggle-sidebar d-md-none" id="toggleSidebar">
        <i className="fas fa-bars"></i>
      </button>

      <div id="sidebar-container">
        <Sidebar />
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