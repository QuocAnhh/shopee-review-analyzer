import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import styles from './Auth.module.scss';

const Login = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentCard, setCurrentCard] = useState(0);
  const navigate = useNavigate();
  const location = useLocation();

  const cards = [
    {
      title: 'Khám phá tính năng',
      content: 'Phân tích, đánh giá sản phẩm Shopee',
      color: '#ff9ff3',
      image: '/assets/img-1.jpg',
    },
    {
      title: 'Chính sách của Shopee',
      content: 'Hiểu biết hơn về chính sách của Shopee',
      color: '#feca57',
      image: '/assets/img-2.jpg',
    },
    {
      title: 'Hỗ trợ 24/7',
      content: 'Chatbot AI luôn sẵn sàng giúp đỡ bạn mọi lúc',
      color: '#5f27cd',
      image: '/assets/img-3.jpg',
    },
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentCard((prev) => (prev + 1) % cards.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  setError('');
  setLoading(true);

  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
      credentials: 'include',
    });

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Login failed');
    }

    localStorage.setItem('accessToken', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    localStorage.setItem('isAuthenticated', true);
    
    const from = location.state?.from?.pathname || '/';
    navigate(from, { replace: true });
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};

  return (
    <div className={styles.container}>
      <div className={styles.carouselContainer}>
        {cards.map((card, index) => (
          <div
            key={index}
            className={`${styles.card} ${index === currentCard ? styles.active : ''}`}
            style={{ backgroundColor: card.color }}
          >
            <img src={card.image} alt={card.title} className={styles.image} />
            <h3>{card.title}</h3>
            <p>{card.content}</p>
          </div>
        ))}
        <div className={styles.dots}>
          {cards.map((_, index) => (
            <span
              key={index}
              className={`${styles.dot} ${index === currentCard ? styles.activeDot : ''}`}
              onClick={() => setCurrentCard(index)}
            />
          ))}
        </div>
      </div>

      <div className={styles.authContainer}>
        <div className={styles.box}>
          <h2>Đăng nhập</h2>
          {error && <div className={styles.error}>{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className={styles.formGroup}>
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                autoComplete="username"
              />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="password">Mật khẩu</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                autoComplete="current-password"
              />
            </div>
            <button type="submit" className={styles.button} disabled={loading}>
              {loading ? 'Đang đăng nhập...' : 'Đăng nhập'}
            </button>
          </form>
          <p className={styles.switch}>
            Chưa có tài khoản?{' '}
            <span onClick={() => navigate('/register')} className={styles.link}>
              Đăng ký ngay
            </span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
