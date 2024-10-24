import "../assets/css/contacts.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faLinkedin, faGithub } from "@fortawesome/free-brands-svg-icons";

function Contacts() {
  return (
    <div className="jumbotron jumbotron-fluid">
      <div className="container-disclaimer">
        <h5 className="display-6" style={{ textAlign: "left" }}>
          Contacts
        </h5>
        <p style={{ textAlign: "left" }}>
          <br />
          Dear User,
          <br />
          <br />
          Please note that software is subject to MIT Licence, the tool was
          developed for educational purposes <br />
          and not for any kind of commercial use.
          <br /> <br />
          <div className="container-disclaimer-text">
            MIT License Copyright (c) 2024 bebesi33 "THE SOFTWARE IS PROVIDED
            "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
            BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
            PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
            AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
            OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
            OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
            OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."
          </div>
          <br />
          <br />
          If you have any questions, please reach out to the developer using the links or the
          email below:
          <br />
          L&aacute;szl&oacute; Bebesi
          <br />
          email: bebesi33{"{at}"}gmail.com
        </p>
      </div>
      <div className="container-contact">
        <div className="social-buttons">
          <a
            href="https://www.linkedin.com/in/l%C3%A1szl%C3%B3-bebesi-frm-93267292"
            className="social-margin"
            target="_blank"
            rel="noopener noreferrer"
          >
            <div className="social-icon linkedin">
              <FontAwesomeIcon icon={faLinkedin} size="5x" />
            </div>
          </a>
          <a
            href="https://github.com/bebesi33/crypto_project"
            target="_blank"
            className="social-margin"
            rel="noopener noreferrer"
          >
            <div className="social-icon github">
              <FontAwesomeIcon icon={faGithub} size="5x" />
            </div>
          </a>
        </div>
      </div>
    </div>
  );
}

export default Contacts;
