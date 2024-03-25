import React from "react";
import { Line } from "react-chartjs-2";
// https://react-chartjs-2.js.org/examples/line-chart
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
} from "chart.js";
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement);

interface LineChartProps {
  input_values: Map<string, number>;
  title: string;
  x_axis_title: string;
  y_axis_title: string;
} // end LineChartProps

const LineChart: React.FC<LineChartProps> = ({
  input_values,
  title,
  x_axis_title,
  y_axis_title,
}) => {
  console.log(typeof input_values);
  const chartData = {
    labels: Array.from(Object.keys(input_values)),
    datasets: [
      {
        label: title,
        data: Array.from(Object.values(input_values)),
        borderColor: "blue",
        fill: false,
      },
    ],
  }; // end chartData

  const chartOptions = {
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
