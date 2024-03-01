import HomePage from './components/HomePage';
import ExplorerPage from './components/ExplorerPage';
import RiskCalcPage from './components/RiskCalcPage';
import Contacts from './components/documentation/Contacts';
import Tutorial from './components/documentation/Tutorial';
import FactorModelInfo from './components/documentation/FactorModelInfo';
import RiskCalculationInfo from './components/documentation/RiskCalculationInfo';


const page_routes = [
  { path: '/', element: <HomePage /> },
  { path: '/explorer', element: <ExplorerPage /> },
  { path: '/risk_calc', element: <RiskCalcPage /> },
  { path: '/contacts', element: <Contacts /> },
  { path: '/tutorial', element: <Tutorial /> },
  { path: '/factor_model_info', element: <RiskCalculationInfo /> },
  { path: '/risk_calculation_info', element: <FactorModelInfo /> },


  // Add more routes as needed
];

export default page_routes;