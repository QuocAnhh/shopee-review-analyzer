import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Auth.module.scss';

const Register = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [currentCard, setCurrentCard] = useState(0);
  const navigate = useNavigate();

  const cards = [
    {
      title: 'Trở thành người dùng Shopee AI',
      content: 'Tận dụng trí tuệ nhân tạo để phân tích sản phẩm',
      color: '#00d2d3',
      image: '/assets/img-1.jpg',
    },
    {
      title: 'Đảm bảo quyền riêng tư',
      content: 'Chúng tôi tôn trọng và bảo vệ dữ liệu của bạn',
      color: '#ff6b6b',
      image: '/assets/img-2.jpg',
    },
    {
      title: 'Cộng đồng phát triển',
      content: 'Tham gia cộng đồng và nhận hỗ trợ liên tục',
      color: '#48dbfb',
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
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  setError('');

  if (formData.password !== formData.confirmPassword) {
    setError('Mật khẩu không khớp');
    return;
  }

  try {
    const response = await fetch('/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
      credentials: 'include',
    });

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Registration failed');
    }

    localStorage.setItem('accessToken', data.access_token);
    navigate('/');
  } catch (err) {
    setError(err.message);
  }
};

  return (
    <div className={styles.container}>
      <div className={styles.authContainer}>
        <div className={styles.box}>
          <h2>Đăng ký</h2>
          {error && <div className={styles.error}>{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className={styles.formGroup}>
              <label htmlFor="name">Họ tên</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
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
              />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="confirmPassword">Xác nhận mật khẩu</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
              />
            </div>
            <button type="submit" className={styles.button}>Đăng ký</button>
          </form>
          <p className={styles.switch}>
            Đã có tài khoản?{' '}
            <span onClick={() => navigate('/login')} className={styles.link}>
              Đăng nhập ngay
            </span>
          </p>
        </div>
      </div>

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
    </div>
  );
};

export default Register;
