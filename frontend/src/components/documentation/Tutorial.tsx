import React, { useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import './Tutorial.css';
import explorer_1 from "../assets/images/explorer1.jpg";
import explorer_2 from "../assets/images/explorer2.jpg";
//  https://stackoverflow.com/questions/73017616/bootstrap-carousel-control-not-working-in-dom-manipulation

const Tutorial: React.FC = () => {
    useEffect(() => {
        // Ensure Bootstrap's carousel is initialized
        const carousel = document.querySelector('#tutorial');
        if (carousel) {
            // new window.bootstrap.Carousel(carousel);
        }
    }, []);

    return (
        <>
        <div><h4>Quick Tutorial</h4></div>
        <div id="tutorial" className="carousel slide" data-ride="carousel">
        <ol className="carousel-indicators">
            <li data-target="#tutorial" data-slide-to="0" className="active"></li>
            <li data-target="#tutorial" data-slide-to="1"></li>
            <li data-target="#tutorial" data-slide-to="2"></li>
        </ol>
        <div className="carousel-inner">
            <div className="carousel-item active">
            <img className="d-block w-100" src={explorer_1} alt="First slide" />
            </div>
            <div className="carousel-item">
            <img className="d-block w-100" src={explorer_2} alt="Second slide" />
            </div>
            <div className="carousel-item">
            <img className="d-block w-100" src={explorer_1} alt="Third slide" />
            </div>
        </div>
        <a className="carousel-control-prev" href="#tutorial" role="button" data-slide="prev">
            <span className="carousel-control-prev-icon" aria-hidden="true"></span>
            <span className="sr-only">Previous</span>
        </a>
        <a className="carousel-control-next" href="#tutorial" role="button" data-slide="next">
            <span className="carousel-control-next-icon" aria-hidden="true"></span>
            <span className="sr-only">Next</span>
        </a>
        </div>
        </>
    );
}

export default Tutorial;