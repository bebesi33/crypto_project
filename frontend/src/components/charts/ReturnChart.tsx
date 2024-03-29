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
import { DEFAULT_BLUE, LIGHT_BLUE } from "../Colors";
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface LineChartProps {
  primary_data: Map<string, number>;
  primary_data_label: string;
  title_text: string;
  x_axis_title: string;
  y_axis_title: string;
  secondary_data: Map<string, number>;
  secondary_data_label: string;
} // end LineChartProps

const ReturnChart: React.FC<LineChartProps> = ({
  primary_data,
  primary_data_label,
  title_text,
  x_axis_title,
  y_axis_title,
  secondary_data,
  secondary_data_label
}) => {
  console.log(typeof primary_data);
  const chartData = {
    labels: Array.from(Object.keys(secondary_data)),
    datasets: [
      {
        label: primary_data_label,
        data: Array.from(Object.values(primary_data)),
        pointRadius: 2,
        lineThickness: 0,
        borderWidth: 0,
        borderColor: LIGHT_BLUE,
        fill: false,
      },
      {
        label: secondary_data_label,
        data: Array.from(Object.values(secondary_data)),
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

export default ReturnChart;
