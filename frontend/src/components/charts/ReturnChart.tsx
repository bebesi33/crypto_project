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
import { CHART_BASE, CHART_LIGHT } from "../Colors";
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
  primaryDataLabel: string;
  titleText: string;
  xAxisTitle: string;
  yAxisTitle: string;
  secondaryData: Map<string, number>;
  secondaryDataLabel: string;
} // end LineChartProps

const ReturnChart: React.FC<LineChartProps> = ({
  primaryData,
  primaryDataLabel,
  titleText,
  xAxisTitle,
  yAxisTitle,
  secondaryData,
  secondaryDataLabel,
}) => {
  console.log(typeof primaryData);
  const chartData = {
    labels: Array.from(Object.keys(secondaryData)),
    datasets: [
      {
        label: primaryDataLabel,
        data: Array.from(Object.values(primaryData)),
        pointRadius: 2,
        lineThickness: 0,
        borderWidth: 0,
        borderColor: CHART_LIGHT,
        fill: false,
      },
      {
        label: secondaryDataLabel,
        data: Array.from(Object.values(secondaryData)),
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

export default ReturnChart;
