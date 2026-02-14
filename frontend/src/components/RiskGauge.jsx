import Plot from "react-plotly.js";

const RiskGauge = ({ score, riskLevel }) => {

  const getLevelConfig = (level) => {
    switch (level) {
      case "SAFE":
        return { text: "SAFE", color: "#22c55e" };
      case "CAUTION":
        return { text: "CAUTION", color: "#f59e0b" };
      case "HIGH RISK":
      default:
        return { text: "HIGH RISK", color: "#ef4444" };
    }
  };

  const level = getLevelConfig(riskLevel);

  return (
    <div
      className="card"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "20px"
      }}
    >
      <h3
        style={{
          marginBottom: "10px",
          color: "var(--text-muted)",
          fontSize: "14px",
          fontWeight: 600,
          textTransform: "uppercase",
          letterSpacing: "1px"
        }}
      >
        Overall Safety Score
      </h3>

      <Plot
        data={[
          {
            type: "indicator",
            mode: "gauge+number",
            value: score,
            number: {
              font: {
                size: 48,
                color: level.color,
                family: "Inter"
              },
              suffix: "/100"
            },
            gauge: {
              axis: {
                range: [0, 100],
                tickwidth: 1,
                tickcolor: "#e5e7eb"
              },
              bar: { color: level.color },
              bgcolor: "white",
              borderwidth: 2,
              bordercolor: "#e5e7eb",
              steps: [
                { range: [0, 25], color: "#dcfce7" },
                { range: [25, 60], color: "#fef3c7" },
                { range: [60, 100], color: "#fee2e2" }
              ],
              threshold: {
                line: { color: "black", width: 4 },
                thickness: 0.75,
                value: score
              }
            }
          }
        ]}
        layout={{
          width: 350,
          height: 250,
          margin: { t: 30, b: 30, l: 30, r: 30 },
          paper_bgcolor: "transparent",
          font: { family: "Inter" }
        }}
        config={{ displayModeBar: false }}
      />

      <div
        style={{
          marginTop: "-20px",
          background: level.color,
          color: "white",
          padding: "6px 20px",
          borderRadius: "999px",
          fontWeight: 700,
          fontSize: "18px"
        }}
      >
        {level.text}
      </div>
    </div>
  );
};

export default RiskGauge;
