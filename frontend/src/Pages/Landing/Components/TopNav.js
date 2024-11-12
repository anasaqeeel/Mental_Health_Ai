import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { useAuth } from '../../Login/Components/AuthContext';
import Translate from '../../Translate';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSignOutAlt } from '@fortawesome/free-solid-svg-icons';
import '../Styles/navbarStyle.css';

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

  const handleVisualizeClick = () => {
    navigate('/landing/visualize');
  };
  // const handleHomeClick = () => {
  //   navigate('/');
  // };

  return (
    <>
      <Navbar expand="lg" className="custom-navbar" sticky="top">
        <Container fluid>
          <Navbar.Brand href="/">Therapy Is Healing</Navbar.Brand>

          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav" >
            <Nav className="mx-auto">
              {/* <Nav.Link href="/landing">Take An Interview</Nav.Link>
              <Nav.Link href="/landing">Seek Help</Nav.Link> */}
              <Nav.Link onClick={handleVideoChatClick}>Start Video Chat</Nav.Link>
              <Nav.Link onClick={handleVisualizeClick}>Visualize</Nav.Link> {/* New Button */}
              {currentUser && (
                <span className="navbar-email text-white">Signed in as: {currentUser.email}</span>
              )}
            </Nav>
            <Nav>
              {currentUser ? (
                <Button
                  variant="outline-light"
                  className="logout-button"
                  onClick={handleLogout}
                  aria-label="Logout"
                >
                  <FontAwesomeIcon icon={faSignOutAlt} />
                </Button>
              ) : (
                <Button
                  variant="outline-light"
                  className="logout-button"
                  href="/login"
                >
                  Log In
                </Button>
              )}
              <Translate />
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  );
}
