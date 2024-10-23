import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { useAuth } from '../../Login/Components/AuthContext';
import Translate from '../../Translate';
export default function TopNav() {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Failed to log out', error);
    }
  };

  const handleVideoChatClick = () => {
    navigate('/landing/video-chat');
  };

  return (
    <div>
      <Navbar expand="lg" className="bg-body-tertiary" data-bs-theme="dark" sticky="top">
        <Container style={{ marginLeft: '1rem' }}>
          <Navbar.Brand href="/">Home</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link href="interview">Take An Interview</Nav.Link>
              <Nav.Link href="questionnaire">Seek Help</Nav.Link>
              <Button
                variant="outline-light"
                onClick={handleVideoChatClick}
                style={{
                  marginLeft: '20px',
                  padding: '8px 15px',
                  fontSize: '14px',
                  borderRadius: '20px',
                  borderColor: '#fff',
                  color: '#fff'
                }}
              >
                Start Video Chat
              </Button>
            </Nav>
          </Navbar.Collapse>
        </Container>

        {currentUser ? (
          <Button variant="primary" style={{ marginRight: '1rem', padding: '8px 15px', borderRadius: '20px' }} onClick={handleLogout}>
            Logout
          </Button>
        ) : (
          <Button variant="primary" style={{ marginRight: '1rem', padding: '8px 15px', borderRadius: '20px' }}>
            <a href="/login" style={{ color: 'white', textDecoration: 'none' }}>Log In</a>
          </Button>
        )}
        <Translate />
      </Navbar>
    </div>
  );
}
