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
  CHART_BASE_BACKGROUND,
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
        borderColor: CHART_BASE_BACKGROUND,
        backgroundColor: CHART_BASE_BACKGROUND,
      },
    ],
  };
  // here the number of data elements is variable
  // we need to iterate the colors
  var green = 225;
  var blue = 242;
  var red = 217
  var updatedColor = `rgb(${red},${green},${blue})`;
  Object.keys(primaryData).forEach((key) => {
    if (key != first_element) {
      data.datasets.push({
        label: key,
        data: Object.values(primaryData[key]),
        borderColor: updatedColor,
        backgroundColor: updatedColor,
      });
      green = Math.max(40, (green + 20) % 256);
      blue = Math.max(40, (blue + 5) % 256);
      red = Math.max(40, (red - 10) % 256);
      updatedColor = `rgb(${red},${green},${blue})`;
    }
  });

  return <Bar options={options} data={data} />;
};

export default RiskDecompositionChart;
