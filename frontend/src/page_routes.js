import HomePage from './components/HomePage';
import ExplorerPage from './components/ExplorerPage';
import RiskCalcPage from './components/RiskCalcPage';
import Contacts from './components/documentation/Contacts';
import Tutorial from './components/documentation/Tutorial';
import FactorModelInfo from './components/documentation/FactorModelInfo';
import RiskCalculationInfo from './components/documentation/RiskCalculationInfo';


const page_routes = [
  { path: '/', component: HomePage },
  { path: '/explorer', component: ExplorerPage },
  { path: '/risk_calc', component: RiskCalcPage },
  { path: '/contacts', component: Contacts },
  { path: '/tutorial', component: Tutorial },
  { path: '/factor_model_info', component: RiskCalculationInfo },
  { path: '/risk_calculation_info', component: FactorModelInfo },


  // Add more routes as needed
];

export default page_routes;