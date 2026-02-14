const OrganGauge = ({ title, value, max = 10 }) => {
  const getPercentage = () => Math.min((value / max) * 100, 100);

  const getColor = (val) => {
    if (val < 4) return "#22c55e"; // Safe
    if (val < 6) return "#f59e0b"; // Caution
    return "#ef4444"; // Danger
  };

  const color = getColor(value);

  return (
    <div className="card" style={{ flex: 1, padding: "20px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
        <h4 style={{ fontSize: "14px", color: "var(--text-muted)" }}>{title}</h4>
        <span style={{ fontWeight: 700, fontSize: "16px", color: color }}>{value} / {max}</span>
      </div>

      <div style={{
        height: "8px",
        background: "#e2e8f0",
        borderRadius: "4px",
        overflow: "hidden"
      }}>
        <div style={{
          width: `${getPercentage()}%`,
          height: "100%",
          background: color,
          transition: "width 0.5s ease-out"
        }} />
      </div>

      <div style={{ marginTop: "8px", display: "flex", justifyContent: "space-between", fontSize: "10px", color: "#94a3b8", fontWeight: 500 }}>
        <span>OPTIMAL</span>
        <span>STRESSED</span>
      </div>
    </div>
  );
};

export default OrganGauge;
