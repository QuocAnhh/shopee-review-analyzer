import React from 'react';
import { motion } from 'framer-motion';
import { FaChartLine, FaComments, FaRobot, FaSearch, FaArrowRight } from 'react-icons/fa';
import { Link } from 'react-router-dom';

const Intro: React.FC = () => {
  const features = [
    {
      icon: <FaComments />,
      title: 'Phân tích đánh giá',
      description: 'Tự động phân tích và tổng hợp đánh giá từ người dùng Shopee'
    },
    {
      icon: <FaChartLine />,
      title: 'Thống kê chi tiết',
      description: 'Hiển thị biểu đồ và số liệu thống kê trực quan'
    },
    {
      icon: <FaRobot />,
      title: 'AI-Powered',
      description: 'Sử dụng công nghệ AI để phân tích cảm xúc và nội dung đánh giá'
    },
    {
      icon: <FaSearch />,
      title: 'Tìm kiếm thông minh',
      description: 'Tìm kiếm và lọc đánh giá theo nhiều tiêu chí khác nhau'
    }
  ];

  return (
    <div className="container-fluid p-0">
      {/* Hero Section */}
      <section className="py-5 py-md-6 bg-light">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center my-auto"
        >
          <motion.h1 
            className="display-4 font-weight-bold text-dark mb-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            <span className="gradient-text">Shopee Review Analyzer</span>
          </motion.h1>
          <motion.p 
            className="lead text-secondary mb-5"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            Công cụ phân tích đánh giá thông minh giúp bạn hiểu rõ hơn về sản phẩm
            và trải nghiệm người dùng trên Shopee thông qua trí tuệ nhân tạo
          </motion.p>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
          >
            <Link to="/trial-info">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn btn-primary btn-lg px-5 py-3 rounded-pill shadow"
              >
                <span>Bắt đầu ngay</span>
                <span className="ms-2"><FaArrowRight /></span>
              </motion.button>
            </Link>
          </motion.div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="py-5">
        <div className="container">
          <motion.h2 
            className="h3 font-weight-bold text-center text-dark mb-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            <span className="highlight-text">Tính năng nổi bật</span>
          </motion.h2>
          <motion.p 
            className="text-center text-secondary mx-auto mb-5" style={{ maxWidth: '32rem' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            Khám phá những tính năng mạnh mẽ giúp bạn hiểu rõ hơn về đánh giá sản phẩm
          </motion.p>
          <div className="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4">
            {features.map((feature, index) => (
              <div className="col" key={index}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  whileHover={{ y: -5 }}
                  className="card h-100 shadow-sm border-light"
                >
                  <div className="card-body d-flex flex-column align-items-center text-center">
                    <div className="feature-icon-circle bg-primary-light text-primary rounded-circle mb-4">
                      {feature.icon}
                    </div>
                    <h3 className="h5 font-weight-semibold text-dark mb-3">
                      {feature.title}
                    </h3>
                    <p className="card-text text-secondary">{feature.description}</p>
                  </div>
                </motion.div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works Section */}
      <section className="py-5 bg-light">
        <div className="container">
          <motion.h2 
            className="h3 font-weight-bold text-center text-dark mb-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            <span className="highlight-text">Cách thức hoạt động</span>
          </motion.h2>
          <motion.p 
            className="text-center text-secondary mx-auto mb-5" style={{ maxWidth: '32rem' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            Chỉ với 3 bước đơn giản để có được báo cáo phân tích chi tiết
          </motion.p>
          <div className="row row-cols-1 row-cols-md-3 g-4">
            <div className="col">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5 }}
                className="position-relative text-center"
              >
                <div className="step-number position-absolute top-0 start-50 translate-middle bg-primary text-white rounded-circle d-flex align-items-center justify-content-center font-weight-bold shadow">
                  1
                </div>
                <div className="card h-100 pt-5 px-3 pb-3 shadow-sm border-light">
                  <div className="card-body">
                    <h3 className="h5 font-weight-semibold mb-3 text-center">Nhập URL sản phẩm</h3>
                    <p className="card-text text-secondary text-center">
                      Dán URL sản phẩm Shopee cần phân tích vào hệ thống
                    </p>
                  </div>
                </div>
              </motion.div>
            </div>
            <div className="col">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="position-relative text-center"
              >
                <div className="step-number position-absolute top-0 start-50 translate-middle bg-primary text-white rounded-circle d-flex align-items-center justify-content-center font-weight-bold shadow">
                  2
                </div>
                <div className="card h-100 pt-5 px-3 pb-3 shadow-sm border-light">
                  <div className="card-body">
                    <h3 className="h5 font-weight-semibold mb-3 text-center">Thu thập dữ liệu</h3>
                    <p className="card-text text-secondary text-center">
                      Hệ thống tự động thu thập và xử lý tất cả các đánh giá
                    </p>
                  </div>
                </div>
              </motion.div>
            </div>
            <div className="col">
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.4 }}
                className="position-relative text-center"
              >
                <div className="step-number position-absolute top-0 start-50 translate-middle bg-primary text-white rounded-circle d-flex align-items-center justify-content-center font-weight-bold shadow">
                  3
                </div>
                <div className="card h-100 pt-5 px-3 pb-3 shadow-sm border-light">
                  <div className="card-body">
                    <h3 className="h5 font-weight-semibold mb-3 text-center">Xem kết quả</h3>
                    <p className="card-text text-secondary text-center">
                      Nhận báo cáo phân tích chi tiết với biểu đồ trực quan
                    </p>
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-5 bg-primary text-white">
        <div className="container text-center">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="h3 font-weight-bold mb-3">Sẵn sàng trải nghiệm?</h2>
            <p className="lead mb-4 mx-auto" style={{ maxWidth: '32rem' }}>
              Bắt đầu phân tích đánh giá sản phẩm ngay hôm nay để có những insights giá trị
            </p>
            <Link to="/trial-info">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn btn-light btn-lg font-weight-semibold rounded-pill shadow"
              >
                Dùng thử miễn phí
              </motion.button>
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default Intro;