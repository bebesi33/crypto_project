import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import page_routes from 'page_routes';
import { Link } from 'react-router-dom';


function MainNavbar() {
  return (
    <Navbar expand="lg" className="bg-body-tertiary" bg="ligth" data-bs-theme="light" fixed="top">
      <Container>
        <Navbar.Brand href="#home" as={Link} to="/">Crypto Risk Calculator</Navbar.Brand>
        <Navbar.Toggle aria-controls="main-navbar-nav" />
        <Navbar.Collapse id="main-navbar">
          <Nav className="me-auto">
          <Nav.Link href="#home" as={Link} to="/">Home</Nav.Link>
            <Nav.Link href="#risk">Risk Calculation</Nav.Link>
            <Nav.Link href="#explorer" as={Link} to="/explorer">Explorer</Nav.Link>
            <NavDropdown title="Documentation" id="documentation-nav-dropdown">
              <NavDropdown.Item href="#quick-tutorial">Quick Tutorial</NavDropdown.Item>
              <NavDropdown.Item href="#factor-model">
                Factor Model
              </NavDropdown.Item>
              <NavDropdown.Item href="#risk-calculation">Risk Calculation</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#credits">
                Credits & Contacts
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default MainNavbar;