import React from 'react';
import { Container, Card, Row, Col } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faInfoCircle, 
  faStar, 
  faEnvelope, 
  faPhoneAlt, 
  faMapMarkerAlt,
  faSearch,
  faBoxOpen,
  faPercentage,
  faHeadset,
  faCode
} from '@fortawesome/free-solid-svg-icons';
import { 
  faFacebookF, 
  faTwitter, 
  faLinkedinIn, 
  faGithub,
  faPython,
  faReact,
  faNodeJs,
  faBootstrap
} from '@fortawesome/free-brands-svg-icons';

const AboutPage = () => {
  // App information data
  const appInfo = {
    version: "1.0.0",
    lastUpdated: "30/4/2025",
    developer: "Quốc Anh Team"
  };

  // Features data
  const features = [
    {
      icon: faSearch,
      title: "Phân tích sản phẩm",
      description: "Phân tích đánh giá người dùng thông qua bình luận"
    },
    {
      icon: faBoxOpen,
      title: "Theo dõi đơn hàng",
      description: "Kiểm tra tình trạng đơn hàng nhanh chóng và chính xác"
    },
    {
      icon: faPercentage,
      title: "Khuyến mãi",
      description: "Thông báo chương trình khuyến mãi và voucher mới nhất"
    },
    {
      icon: faHeadset,
      title: "Hỗ trợ 24/7",
      description: "Giải đáp mọi thắc mắc về sản phẩm và dịch vụ"
    }
  ];

  // Technologies data
  const technologies = [
    {
      name: "Python",
      icon: faPython,
      description: "Xử lý backend và phân tích dữ liệu",
      color: "#3776AB"
    },
    {
      name: "Selenium",
      icon: "SiSelenium",
      description: "Tự động hóa thu thập dữ liệu",
      color: "#43B02A"
    },
    {
      name: "React",
      icon: faReact,
      description: "Xây dựng giao diện người dùng",
      color: "#61DAFB"
    },
    {
      name: "Node.js",
      icon: faNodeJs,
      description: "Xử lý phía server và API",
      color: "#339933"
    },
    {
      name: "Bootstrap 5",
      icon: faBootstrap,
      description: "Thiết kế giao diện responsive",
      color: "#7952B3"
    },
    {
      name: "NLP",
      icon: "SiNlp",
      description: "Xử lý ngôn ngữ tự nhiên cho chatbot",
      color: "#FF6F61"
    },
    {
      name: "MongoDB",
      icon: "DiMongodb",
      description: "Lưu trữ dữ liệu NoSQL",
      color: "#47A248"
    }
  ];

  // Contact information
  const contactInfo = [
    {
      icon: faEnvelope,
      text: "support@shopee-chatbot.com"
    },
    {
      icon: faPhoneAlt,
      text: "1900 1234"
    },
    {
      icon: faMapMarkerAlt,
      text: "TP. Hà Nội, Việt Nam"
    }
  ];

  // Social media links
  const socialLinks = [
    { icon: faFacebookF, url: "#" },
    { icon: faTwitter, url: "#" },
    { icon: faLinkedinIn, url: "#" },
    { icon: faGithub, url: "#" }
  ];

  // Function to render technology icon
  const renderTechIcon = (tech) => {
    if (tech.icon === "SiSelenium") {
      return <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/selenium/selenium-original.svg" width="24" alt="Selenium" />;
    } else if (tech.icon === "SiNlp") {
      return <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg" width="24" alt="NLP" />;
    } else if (tech.icon === "DiMongodb") {
      return <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg" width="24" alt="MongoDB" />;
    } else {
      return <FontAwesomeIcon icon={tech.icon} />;
    }
  };

  return (
    <div className="about-page h-100 overflow-auto">
      <Container fluid>
        {/* Header Section */}
        <div className="about-header text-center py-5 border-bottom">
          <img 
            src="./assets/shopee-logo.jpg" 
            alt="Shopee Logo" 
            className="mb-4" 
            width="100"
          />
          <h2>Shopee Chatbot</h2>
          <p className="lead text-muted">Trợ lý ảo thông minh hỗ trợ người dùng Shopee</p>
        </div>
        
        {/* Content Sections */}
        <div className="about-content">
          {/* App Info Section */}
          <div className="about-section border-bottom p-4">
            <h4 className="d-flex align-items-center mb-4">
              <FontAwesomeIcon icon={faInfoCircle} className="me-2" />
              Thông tin ứng dụng
            </h4>
            <div className="row g-3">
              <div className="col-md-4">
                <div className="d-flex justify-content-between py-2 border-bottom">
                  <span className="fw-medium">Phiên bản:</span>
                  <span className="text-muted">{appInfo.version}</span>
                </div>
              </div>
              <div className="col-md-4">
                <div className="d-flex justify-content-between py-2 border-bottom">
                  <span className="fw-medium">Cập nhật:</span>
                  <span className="text-muted">{appInfo.lastUpdated}</span>
                </div>
              </div>
              <div className="col-md-4">
                <div className="d-flex justify-content-between py-2 border-bottom">
                  <span className="fw-medium">Nhà phát triển:</span>
                  <span className="text-muted">{appInfo.developer}</span>
                </div>
              </div>
            </div>
          </div>
          
          {/* Features Section */}
          <div className="about-section border-bottom p-4">
            <h4 className="d-flex align-items-center mb-4">
              <FontAwesomeIcon icon={faStar} className="me-2" />
              Tính năng nổi bật
            </h4>
            <div className="row g-4">
              {features.map((feature, index) => (
                <div key={index} className="col-md-6 col-lg-3">
                  <Card className="h-100 shadow-sm">
                    <Card.Body className="text-center">
                      <div 
                        className="feature-icon bg-primary bg-opacity-10 text-primary rounded-circle d-inline-flex align-items-center justify-content-center mb-3" 
                        style={{ width: '50px', height: '50px' }}
                      >
                        <FontAwesomeIcon icon={feature.icon} />
                      </div>
                      <h5 className="card-title">{feature.title}</h5>
                      <p className="card-text text-muted">{feature.description}</p>
                    </Card.Body>
                  </Card>
                </div>
              ))}
            </div>
          </div>
          
          {/* Technologies Section */}
          <div className="about-section border-bottom p-4">
            <h4 className="d-flex align-items-center mb-4">
              <FontAwesomeIcon icon={faCode} className="me-2" />
              Công nghệ sử dụng
            </h4>
            <div className="row g-4">
              {technologies.map((tech, index) => (
                <Col key={index} xs={6} md={4} lg={3}>
                  <Card className="h-100 shadow-sm">
                    <Card.Body className="text-center">
                      <div 
                        className="tech-icon mb-3 mx-auto d-flex align-items-center justify-content-center rounded-circle"
                        style={{ 
                          width: '60px', 
                          height: '60px', 
                          backgroundColor: `${tech.color}20`,
                          color: tech.color,
                          fontSize: '24px'
                        }}
                      >
                        {renderTechIcon(tech)}
                      </div>
                      <h5 className="card-title">{tech.name}</h5>
                      <p className="card-text text-muted small">{tech.description}</p>
                    </Card.Body>
                  </Card>
                </Col>
              ))}
            </div>
          </div>
          
          {/* Contact Section */}
          <div className="about-section p-4">
            <h4 className="d-flex align-items-center mb-4">
              <FontAwesomeIcon icon={faEnvelope} className="me-2" />
              Liên hệ
            </h4>
            <div className="contact-info">
              {contactInfo.map((contact, index) => (
                <div key={index} className="d-flex align-items-center mb-3">
                  <FontAwesomeIcon icon={contact.icon} className="me-3 text-primary" />
                  <span>{contact.text}</span>
                </div>
              ))}
            </div>
            
            <div className="social-links d-flex gap-3 mt-4">
              {socialLinks.map((social, index) => (
                <a 
                  key={index} 
                  href={social.url} 
                  className="btn btn-outline-primary rounded-circle"
                >
                  <FontAwesomeIcon icon={social.icon} />
                </a>
              ))}
            </div>
          </div>
        </div>
      </Container>
    </div>
  );
};

export default AboutPage;