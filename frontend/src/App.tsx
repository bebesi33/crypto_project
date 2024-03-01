import "./App.css";
import MainNavbar from "./components/MainNavbar";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import ExplorerPage from './components/ExplorerPage';
import RiskCalcPage from './components/RiskCalcPage';
import Contacts from './components/documentation/Contacts';
import Tutorial from './components/documentation/Tutorial';
import FactorModelInfo from './components/documentation/FactorModelInfo';
import RiskCalculationInfo from './components/documentation/RiskCalculationInfo';


function App() {
  return (
    <>
    <Router>
      <div>
        <MainNavbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/explorer" element={<ExplorerPage />} />
          <Route path="/risk_calc" element={<RiskCalcPage />} />
          <Route path="/contacts" element={<Contacts />} />
          <Route path="/tutorial" element={<Tutorial />} />
          <Route path="/factor_model_info" element={<FactorModelInfo />} />
          <Route path="/risk_calculation_info" element={<RiskCalculationInfo />} />
        </Routes>
      </div>
    </Router>
    </>
    
  );
}

export default App;
