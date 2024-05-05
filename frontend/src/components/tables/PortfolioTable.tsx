interface TableProps {
  primaryData: Map<string, Map<string, number>>;
  tableTitle: string;
} // end TableProps

const PortfolioTable: React.FC<TableProps> = ({ primaryData, tableTitle }) => {
  console.log(primaryData);
  return (
    <div>
      <h5>{tableTitle}</h5>
      <table className="table table-striped">
        <thead className="thead-dark">
          <th>Symbol</th>
          <th>portfolio</th>
          <th>benchmark</th>
          <th>active</th>
        </thead>
        <tbody>
          {Object.entries(primaryData).map(([key, value]) => (
            <tr key={key}>
              <td style={{ textAlign: "left" }}>{key}</td>
              <td style={{ textAlign: "right" }}>{value["portfolio"]}</td>
              <td style={{ textAlign: "right" }}>{value["benchmark"]}</td>
              <td style={{ textAlign: "right" }}>{value["active"]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  ); // end return
};

export default PortfolioTable;
