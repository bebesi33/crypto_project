interface TableProps {
  primaryData: Map<string, number>;
  metricColumn: string;
  valueColumn: string;
  tableTitle: string;
  headerLevel?: keyof JSX.IntrinsicElements;
} // end TableProps

const SimpleTable: React.FC<TableProps> = ({
  primaryData,
  tableTitle,
  metricColumn,
  valueColumn,
  headerLevel = 'h3'
}) => {
  const HeaderTag = headerLevel;
  return (
    <div>
      <HeaderTag>{tableTitle}</HeaderTag>
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
