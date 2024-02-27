import "./App.css";
import MainNavbar from "./components/MainNavbar";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import ExplorerPage from './components/ExplorerPage';


function App() {
  return (
    <>
    <Router>
      <div>
        <MainNavbar />
        <Routes>
          <Route index element={<HomePage />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/explorer" element={<ExplorerPage />} />
        </Routes>
      </div>
    </Router>
    </>
    
  );
}

export default App;
