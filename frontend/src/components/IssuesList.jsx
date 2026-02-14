function IssueCard({ issue }) {
  const color =
    issue.severity === "high" ? "#f44336" :
    issue.severity === "medium" ? "#ff9800" :
    "#4caf50";

  return (
    <div style={{
      background: "#f9f9f9",
      padding: "15px",
      borderLeft: `5px solid ${color}`,
      marginBottom: "10px"
    }}>
      {issue.text}
    </div>
  );
}

export default IssueCard;
