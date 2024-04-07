interface TableProps {
  primaryData: Map<string, number>;
  metricColumn: string;
  valueColumn: string;
  tableTitle: string;
} // end TableProps

const SimpleTable: React.FC<TableProps> = ({
  primaryData,
  tableTitle,
  metricColumn,
  valueColumn,
}) => {
  console.log("This is fine!");
  return (
    <div>
      <h3>{tableTitle}</h3>
      <table className="table table-striped">
        <thead className="thead-dark">
          <tr>
            <th>{metricColumn}</th>
            <th>{valueColumn}</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(primaryData).map(([key, value]) => (
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
