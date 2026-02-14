import { CheckCircle2 } from "lucide-react";

const GuidancePanel = ({ guidance }) => {
  if (!guidance || guidance.length === 0) return null;

  return (
    <div className="card" style={{ marginTop: "24px" }}>
      <h3 style={{ marginBottom: "16px", fontSize: "18px", display: "flex", alignItems: "center", gap: "8px", color: "var(--text-main)" }}>
        <CheckCircle2 size={20} color="var(--primary)" /> Recommended Next Steps
      </h3>
      <ul style={{ listStyle: "none", display: "flex", flexDirection: "column", gap: "10px" }}>
        {guidance.map((item, index) => (
          <li key={index} style={{
            display: "flex",
            gap: "12px",
            padding: "16px",
            background: "#fdfdfd",
            borderRadius: "var(--radius-sm)",
            fontSize: "15px",
            color: "#4a4a4a",
            fontWeight: 500,
            borderLeft: "4px solid var(--primary)",
            border: "1px solid var(--border)",
            borderLeftWidth: "4px"
          }}>
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default GuidancePanel;
