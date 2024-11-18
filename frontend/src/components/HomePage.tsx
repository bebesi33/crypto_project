import Card from "react-bootstrap/Card";
import { Link } from "react-router-dom";
import "./assets/css/home_page.css";
import risk_calc_image from "./assets/images/risk_calc_image.jpg";
import explorer_image from "./assets/images/explorer_image.jpg";

function HomePage() {
  return (
    <div className="parent-container">
      <link href="/HomePage.css"></link>
      <div className="text-nowrap">
        <h4>Welcome to László's Cryptocurrency Risk Calculation Tool!</h4>
        <p style={{ textAlign: "left" }}>
          This project serves as the basis of my BSc thesis in Computer Science.{" "}
          <br />
          In this project, I leverage my existing quailifications (Financial
          Mathematics) along with the knowledge I gained as part of the ELTE
          Computer Science BSc program.
        </p>
        <h5 style={{ textAlign: "left" }}>Key Features:</h5>
        <ul style={{ textAlign: "left" }} id="key-features">
          <li>
            <strong>Accessibility:</strong> The Risk Calculation Tool relies on
            publicly available data, which users can access this without any
            restrictions.
          </li>
          <li>
            <strong>Individual Endeavor:</strong> I developed the model on my
            own, while receiving feedback from my consultant/teacher Zoltán
            Illés Phd.
          </li>
          <li>
            <strong>Versatility:</strong> The tool allows for multiple risk
            calculation settings, which accomodates the needs of a diverse user
            base.
          </li>
          <li>
            <strong>Support and Feedback:</strong> The documentation for the
            tool is available within the application. You can reach out to me
            (the author) through multiple channels.
          </li>
        </ul>
        <p style={{ textAlign: "left" }}>
          Thank you for utilizing this tool. I hope it can deliver valuable
          results to you, when analysing cryptocurrency portfolios. <br />
          Feel free to explore, analyze with confidence. If you find any caveats
          or if You have any feedback, please use the contacts in the contacts
          page. <br />
          All errors, caveats in this project are mine.
        </p>
        <p style={{ textAlign: "left" }}>Best regards, <br/> László Bebesi</p>
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
