import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import { Link } from "react-router-dom";
import { NAVBAR_BACKGROUND } from "./Colors";

function MainNavbar() {
  return (
    <Navbar
      expand="lg"
      style={{ backgroundColor: NAVBAR_BACKGROUND }}
      data-bs-theme="light"
      fixed="top"
    >
      <Container>
        <Navbar.Brand href="#home" as={Link} to="/">
          Crypto Risk Calculator
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="main-navbar-nav" />
        <Navbar.Collapse id="main-navbar">
          <Nav className="me-auto">
            <Nav.Link href="#home" as={Link} to="/">
              Home
            </Nav.Link>
            <Nav.Link href="#risk_calc" as={Link} to="/risk_calc">
              Risk Calculator
            </Nav.Link>
            <Nav.Link href="#explorer" as={Link} to="/explorer">
              Explorer
            </Nav.Link>
            <NavDropdown title="Documentation" id="documentation-nav-dropdown">
              <NavDropdown.Item href="#quick-tutorial" as={Link} to="/tutorial">
                Quick Tutorial
              </NavDropdown.Item>
              <NavDropdown.Item
                href="#factor-model"
                as={Link}
                to="/factor_model_info"
              >
                Factor Model
              </NavDropdown.Item>
              <NavDropdown.Item
                href="#risk-calculation"
                as={Link}
                to="/risk_calculation_info"
              >
                Risk Calculation
              </NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#contacts" as={Link} to="contacts">
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
