import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

const PrivateRoute = ({ children }) => {
  const location = useLocation();
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  const user = JSON.parse(localStorage.getItem('user')); // Lấy thông tin user

  // Kiểm tra nếu không xác thực
  if (!isAuthenticated) {
    // Kiểm tra nếu user đang trong giai đoạn trial và trial còn hạn
    const isTrial = user?.isTrial === true;
    const trialEndDate = user?.trialEndDate ? new Date(user.trialEndDate) : null;
    const isTrialActive = isTrial && trialEndDate && trialEndDate > new Date();

    if (isTrialActive) {
      // Nếu trial còn hạn, cho phép truy cập các route trong PrivateRoute
      return children;
    } else {
      // Nếu không xác thực và trial không còn hạn, chuyển hướng về trang intro
      return <Navigate to="/intro" state={{ from: location }} replace />;
    }
  }

  // Nếu đã xác thực, cho phép truy cập
  return children;
};

export default PrivateRoute;