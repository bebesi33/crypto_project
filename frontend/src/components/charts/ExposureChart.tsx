import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import { CHART_BASE, CHART_BASE_BACKGROUND, CHART_LIGHT, CHART_LIGHT_BACKGROUND, CHART_DARK, CHART_DARK_BACKGROUND } from "../Colors";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface ExposureChartProps {
  primaryData: {
    [key: string]: {
      [subKey: string]: {
        [subSubKey: string]: number;
      };
    };
  };
  titleText: string;
} // end LineChartProps

const ExposureChart: React.FC<ExposureChartProps> = ({
  primaryData,
  titleText,
}) => {
  const options = {
    maintainAspectRatio: false,
    indexAxis: "y" as const,
    elements: {
      bar: {
        borderWidth: 2,
      },
    },
    responsive: true,
    plugins: {
      legend: {
        position: "bottom" as const,
      },
      title: {
        display: true,
        text: titleText,
        font: {
          size: 18,
        },
      },
    },
  };

  const labels = Object.keys(primaryData["portfolio"]["exposure"]);

  const data = {
    labels,
    datasets: [
      {
        label: "portfolio",
        data: Object.values(primaryData["portfolio"]["exposure"]),
        borderColor: CHART_BASE,
        backgroundColor: CHART_BASE_BACKGROUND,
      },
    ],
  };

  // conditional logics only relevant if calculation needed in active space
  if (primaryData.hasOwnProperty("market")) {
    data.datasets.push({
      label: "benchmark",
      data: Object.values(primaryData["market"]["exposure"]),
      borderColor: CHART_LIGHT,
      backgroundColor: CHART_LIGHT_BACKGROUND,
    });
  }

  if (primaryData.hasOwnProperty("active")) {
    data.datasets.push({
      label: "active",
      data: Object.values(primaryData["active"]["exposure"]),
      borderColor: CHART_DARK,
      backgroundColor: CHART_DARK_BACKGROUND,
    });
  }

  return <Bar options={options} data={data} />;
};

export default ExposureChart;
