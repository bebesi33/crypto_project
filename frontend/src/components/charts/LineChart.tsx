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
  Legend
} from "chart.js";
import { DEFAULT_BLUE } from "../Colors";
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface LineChartProps {
  primary_data: Map<string, number>;
  title_text: string;
  primary_data_label: string;
  x_axis_title: string;
  y_axis_title: string;
} // end LineChartProps

const LineChart: React.FC<LineChartProps> = ({
  primary_data,
  title_text,
  primary_data_label,
  x_axis_title,
  y_axis_title,
}) => {
  console.log(typeof primary_data);
  const chartData = {
    labels: Array.from(Object.keys(primary_data)),
    datasets: [
      {
        label: primary_data_label,
        data: Array.from(Object.values(primary_data)),
        pointRadius: 0,
        borderColor: DEFAULT_BLUE,
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
        text: title_text,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: x_axis_title,
        },
      },
      y: {
        title: {
          display: true,
          text: y_axis_title,
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