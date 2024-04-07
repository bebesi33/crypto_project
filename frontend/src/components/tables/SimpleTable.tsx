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
    <div>
      <h3>{table_title}</h3>
      <table className="table table-striped">
        <thead className="thead-dark">
          <tr>
            <th>{metric_column}</th>
            <th>{value_column}</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(primary_data).map(([key, value]) => (
            <tr key={key}>
              <td style={{ textAlign: "left" }}>{key}</td>
              <td style={{ textAlign: "right" }}>{value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  ); // end return
};

export default SimpleTable;
