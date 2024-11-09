import "./components/assets/css/app.css";
import MainNavbar from "./components/MainNavbar";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import page_routes from "./page_routes";


function App() {
  return (
    <>
    <Router>
      <div>
        <MainNavbar />
        <Routes>
          {page_routes.map((route, index) => (
            <Route key={index} path={route.path} element={route.element} />
          ))}
        </Routes>
      </div>
    </Router>
    </>
  );
}

export default App;
