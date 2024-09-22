import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import { Carousel } from "react-bootstrap";
import "./Tutorial.css";
import explorer_1 from "../assets/images/explorer_1.jpg";
import explorer_2 from "../assets/images/explorer_2.jpg";
import risk_calc_1 from "../assets/images/risk_calc_1.jpg";
import risk_calc_2 from "../assets/images/risk_calc_2.jpg";
//  https://stackoverflow.com/questions/73017616/bootstrap-carousel-control-not-working-in-dom-manipulation

const Tutorial: React.FC = () => {
  return (
    <Carousel data-bs-theme="dark">
      <Carousel.Item>
        <img className="d-block w-100" src={explorer_1} alt="Third slide" />
        <Carousel.Caption>
          <h3> Use the "Explorer" tool to check cryptocurrency coverage </h3>
          <p>
            <b>
              The relevant user input covers the name of the cryptocurrency (1)
              and half-life related parameters (2)
            </b>
          </p>
        </Carousel.Caption>
      </Carousel.Item>
      <Carousel.Item>
        <img className="d-block w-100" src={explorer_2} alt="Third slide" />
        <Carousel.Caption>
          <h3>
            {" "}
            The "Explorer" tool results show the price history and risk estimates of the
            selected cryptocurrency{" "}
          </h3>
          <p>
            {" "}
            <b>The debug messages may show problems with parameter settings </b>
          </p>
        </Carousel.Caption>
      </Carousel.Item>
      <Carousel.Item>
        <img className="d-block w-100" src={risk_calc_1} alt="Third slide" />
        <Carousel.Caption>
          <h3>
            Use "Risk Calculator" tool to assess your portfolio's risk profile
          </h3>
          <p>
            <b>
              Provide the calculation date (1), provide portfolio compositons in
              csv-s (2), specify risk calculation parameters (3)
            </b>
          </p>
        </Carousel.Caption>
      </Carousel.Item>
      <Carousel.Item>
        <img className="d-block w-100" src={risk_calc_2} alt="Third slide" />
        <Carousel.Caption>
          <h3>
            The "Risk Calculator" provides a detailed breakdown on the portfolio's risk profile
          </h3>
          <p>
            <b>
              The tool presents high level risk summary, and component level
              breakdowns
            </b>
          </p>
        </Carousel.Caption>
      </Carousel.Item>
    </Carousel>
  );
};

export default Tutorial;
