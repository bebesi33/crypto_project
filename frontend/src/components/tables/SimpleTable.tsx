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

  const renderHeader = () => {
    return (
      <tr>
        <th>{metric_column}</th>
        <th>{value_column}</th>
      </tr>
    );
  }; // end renderHeader

  const renderRows = () => {
    // Convert the Map to an array of entries
    const dataEntries = Array.from(primary_data.entries());
    console.log(dataEntries)
    return (<div/>)
    // return dataEntries.map(([name, value]) => (
    //   <tr key={name}>
    //     <td>{name}</td>
    //     <td>{value}</td>
    //   </tr>
    // ));
  }; // end renderRows
  console.log("This is fine!")
  return (
    <div style={{ margin: "50px" }}>
      <h1>{table_title}</h1>
      <table>
        <thead>{renderHeader()}</thead>
        <tbody>{renderRows()}</tbody>
      </table>
    </div>
  ); // end return
};

export default SimpleTable;
