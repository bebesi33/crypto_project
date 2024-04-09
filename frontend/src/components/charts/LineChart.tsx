import React from "react";
import { Line } from "react-chartjs-2";
// https://react-chartjs-2.js.org/examples/line-chart
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { CHART_BASE } from "../Colors";
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface LineChartProps {
  primaryData: Map<string, number>;
  titleText: string;
  primaryDataLabel: string;
  xAxisTitle: string;
  yAxisTitle: string;
} // end LineChartProps

const LineChart: React.FC<LineChartProps> = ({
  primaryData,
  titleText,
  primaryDataLabel,
  xAxisTitle,
  yAxisTitle,
}) => {
  const chartData = {
    labels: Array.from(Object.keys(primaryData)),
    datasets: [
      {
        label: primaryDataLabel,
        data: Array.from(Object.values(primaryData)),
        pointRadius: 0,
        borderColor: CHART_BASE,
        fill: false,
      },
    ],
  }; // end chartData

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: titleText,
        font: {
          size: 18,
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: xAxisTitle,
        },
      },
      y: {
        title: {
          display: true,
          text: yAxisTitle,
        },
      },
    },
  }; // end chartOptions

  return (
    <div>
      <Line data={chartData} options={chartOptions} />
    </div>
  ); // end return
};

export default LineChart;
