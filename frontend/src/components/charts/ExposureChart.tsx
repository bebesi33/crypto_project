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
import { DEFAULT_BLUE, DEFAULT_BLUE_BACKGROUND, LIGHT_BLUE, LIGHT_BLUE_BACKGROUND, MEDIUM_BLUE, MEDIUM_BLUE_BACKGROUND } from "../Colors";

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
    // scales: {
    //   x: {
    //     type: "linear" as const,
    //     barPercentage: 0.9,
    //     barThickness: 15,
    //     maxBarThickness: 30
    //   },
    // },
  };

  const labels = Object.keys(primaryData["portfolio"]["exposure"]);

  const data = {
    labels,
    datasets: [
      {
        label: "portfolio",
        data: Object.values(primaryData["portfolio"]["exposure"]),
        borderColor: DEFAULT_BLUE,
        backgroundColor: DEFAULT_BLUE_BACKGROUND,
      },
    ],
  };

  // conditional logics only relevant if calculation needed in active space
  if (primaryData.hasOwnProperty("market")) {
    data.datasets.push({
      label: "benchmark",
      data: Object.values(primaryData["market"]["exposure"]),
      borderColor: LIGHT_BLUE,
      backgroundColor: LIGHT_BLUE_BACKGROUND,
    });
  }

  if (primaryData.hasOwnProperty("active")) {
    data.datasets.push({
      label: "active",
      data: Object.values(primaryData["active"]["exposure"]),
      borderColor: MEDIUM_BLUE,
      backgroundColor: MEDIUM_BLUE_BACKGROUND,
    });
  }

  return <Bar options={options} data={data} />;
};

export default ExposureChart;
