interface TableProps {
  primary_data: Map<string, number>;
  metric_column: string;
  value_column: string;
  table_title: string;
} // end TableProps

const SimpleTable: React.FC<TableProps> = ({
  primary_data,
  table_title,
  metric_column,
  value_column,
}) => {
  console.log("This is fine!");
  return (
    <div style={{ margin: "50px" }}>
      <h1>{table_title}</h1>
      <table>
        <thead>
          <tr>
            <th>{metric_column}</th>
            <th>{value_column}</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(primary_data).map(([key, value]) => (
            <tr key={key}>
              <td>{key}</td>
              <td>{value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  ); // end return
};

export default SimpleTable;
