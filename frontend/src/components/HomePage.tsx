import Card from "react-bootstrap/Card";
import { Link } from "react-router-dom";
import "./HomePage.css";
import risk_calc_image from "./assets/images/risk_calc_image.jpg";
import explorer_image from "./assets/images/explorer_image.jpg";

function HomePage() {
  return (
    <div className="parent-container">
      <link href="/HomePage.css"></link>
      <div className="text-nowrap">
        <h4>Welcome to László's Cryptocurrency Risk Calculation Tool!</h4>
        <p style={{ textAlign: "left" }}>
          This project serves as a fundamental component of my Bachelor of
          Science thesis in Computer Science. <br />
          As a culmination of my academic journey, this tool represents my
          dedication to exploring the intricacies of risk assessment and
          financial modeling within the realm of computer science.
        </p>
        <h5 style={{ textAlign: "left" }}>Key Features:</h5>
        <ul style={{ textAlign: "left" }} id="key-features">
          <li>
            <strong>Accessibility:</strong> All the data utilized within this
            tool is sourced from publicly available information. <br />{" "}
            Transparency and accountability are central tenets of this project.
          </li>
          <li>
            <strong>Individual Endeavor:</strong> I developed this tool
            independently, leveraging my skills and knowledge gained throughout
            my academic studies <br /> to create a robust and user-friendly
            platform for risk calculation.
          </li>
          <li>
            <strong>Versatility:</strong> The tool comprises two primary
            functions: a risk calculator and an explorer. <br />
            These features are designed to cater to diverse needs within the
            realm of risk assessment and financial analysis.
          </li>
          <li>
            <strong>Support and Feedback:</strong> Your input is invaluable to
            me. Should you encounter any errors or have suggestions for
            improvement, please do not hesitate to <br /> reach out to me via
            the "Credits & Contacts" page.
          </li>
        </ul>
        <p style={{ textAlign: "left" }}>
          Thank you for utilizing this tool. I hope it can deliver valuable
          results to you, when analysing cryptocurrency portfolios. <br />
          Feel free to explore, analyze, and innovate with confidence.
        </p>
        <p style={{ textAlign: "left" }}>Best regards,</p>
        <p style={{ textAlign: "left" }}>László Bebesi</p>
      </div>

      <div className="row">
        <div className="col-3 col-sm-3">
          <Card style={{ width: "18rem" }} id="card-img-risk-calc">
            <Card.Img
              variant="top"
              src={risk_calc_image}
              alt="risk-calc-image"
              className="img-fluid" // make image responsive to different sizes
            />
            <Card.Body className="card-body">
              <Card.Title>Risk Calculator</Card.Title>
              <Card.Text className="card-text">
                Conduct a comprehensive assessment of the risk inherent in your
                portfolio and compare its risk profile against a benchmark.
              </Card.Text>
              <Link to="/risk_calc" className="btn btn-primary">
                Go to Risk Calculator
              </Link>
            </Card.Body>
          </Card>
        </div>

        <div className="col-3 col-sm-3">
          <Card style={{ width: "18rem" }} id="card-img-explorer">
            <Card.Img
              variant="top"
              src={explorer_image}
              alt="risk-calc-image"
              className="img-fluid" // make image responsive to different sizes
            />
            <Card.Body className="card-body">
              <Card.Title>Explorer</Card.Title>
              <Card.Text className="card-text">
                Explore model coverage, observe individual cryptocurrency price
                data, and assess risk.
              </Card.Text>
              <Link to="/explorer" className="btn btn-primary">
                Go to Explorer
              </Link>
            </Card.Body>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
