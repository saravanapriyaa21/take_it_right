import { Sparkles } from "lucide-react";

const AIExplanation = ({ text }) => {
    if (!text) return null;

    return (
        <div style={{
            marginTop: "24px",
            padding: "24px",
            borderRadius: "var(--radius-lg)",
            background: "#fff9f9",
            border: "1px solid #fee2e2",
            boxShadow: "0 4px 12px rgba(0, 0, 0, 0.03)"
        }}>
            <h3 style={{
                marginBottom: "16px",
                fontSize: "18px",
                display: "flex",
                alignItems: "center",
                gap: "8px",
                color: "var(--primary)"
            }}>
                <Sparkles size={20} color="var(--primary)" /> Why This Is Risky
            </h3>
            <div style={{
                color: "#4a4a4a",
                lineHeight: "1.7",
                fontSize: "15px",
                whiteSpace: "pre-wrap"
            }}>
                {text}
            </div>
        </div>
    );
};

export default AIExplanation;
