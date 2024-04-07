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
    indexAxis: "y" as const,
    elements: {
      bar: {
        borderWidth: 2
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
        borderColor: "rgb(255, 99, 132)",
        backgroundColor: "rgba(255, 99, 132, 0.5)",
      },
    ],
  };

  // conditional logics only relevant if calculation needed in active space
  if (primaryData.hasOwnProperty("market")) {
    data.datasets.push({
      label: "benchmark",
      data: Object.values(primaryData["market"]["exposure"]),
      borderColor: "rgb(0, 128, 0)",
      backgroundColor: "rgba(0, 128, 0, 0.5)",
    });
  }

  if (primaryData.hasOwnProperty("active")) {
    data.datasets.push({
      label: "active",
      data: Object.values(primaryData["active"]["exposure"]),
      borderColor: "rgb(0, 0, 255)",
      backgroundColor: "rgba(0, 0, 255, 0.5)",
    });
  }

  return <Bar options={options} data={data} />;
};

export default ExposureChart;
