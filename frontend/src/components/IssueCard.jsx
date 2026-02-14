import { AlertCircle, AlertTriangle, Info } from "lucide-react";

const IssueCard = ({ issue }) => {
    const { risk, severity } = issue;

    const getConfig = (sev) => {
        if (sev >= 5) return { icon: <AlertCircle size={20} />, bg: "#fee2e2", border: "#f87171", color: "#991b1b" };
        if (sev >= 4) return { icon: <AlertTriangle size={20} />, bg: "#ffedd5", border: "#fb923c", color: "#9a3412" };
        return { icon: <Info size={20} />, bg: "#f1f5f9", border: "#cbd5e1", color: "#334155" };
    };

    const config = getConfig(severity);

    return (
        <div style={{
            display: "flex",
            alignItems: "center",
            gap: "16px",
            padding: "16px",
            borderRadius: "var(--radius-md)",
            background: config.bg,
            border: `1px solid ${config.border}`,
            color: config.color,
            marginBottom: "12px"
        }}>
            <div style={{ flexShrink: 0 }}>
                {config.icon}
            </div>
            <div style={{ fontWeight: 600, fontSize: "15px" }}>
                {risk}
            </div>
        </div>
    );
};

export default IssueCard;
