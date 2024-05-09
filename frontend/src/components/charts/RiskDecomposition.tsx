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
import {
  CHART_BASE,
  CHART_BASE_BACKGROUND,
  CHART_LIGHT,
  CHART_LIGHT_BACKGROUND,
} from "../Colors";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface RiskDecompositionProps {
  primaryData: {
    [key: string]: {
      [subKey: string]: number;
    };
  };
  titleText: string;
} // end LineChartProps

const RiskDecompositionChart: React.FC<RiskDecompositionProps> = ({
  primaryData,
  titleText,
}) => {
  const options = {
    type: "bar",
    maintainAspectRatio: false,
    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true,
        title: {
            display: true,
            text: "Value in pct",
        },
      },
    },
    indexAxis: "x" as const,
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
  const first_element = Object.keys(primaryData)[0];
  const labels = Object.keys(primaryData[first_element]);

  const data = {
    labels,
    datasets: [
      {
        label: first_element,
        data: Object.values(primaryData[first_element]),
        borderColor: CHART_BASE,
        backgroundColor: CHART_BASE_BACKGROUND,
      },
    ],
  };

  Object.keys(primaryData).forEach((key) => {
    if (key != first_element) {
      data.datasets.push({
        label: key,
        data: Object.values(primaryData[key]),
        borderColor: CHART_LIGHT,
        backgroundColor: CHART_LIGHT_BACKGROUND,
      });
    }
  });

  return <Bar options={options} data={data} />;
};

export default RiskDecompositionChart;
