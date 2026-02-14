import { Clock } from "lucide-react";

const TimelineChart = ({ previousTime, currentTime, minSpacing }) => {
    if (!previousTime) return null;

    // Simple visual logic: if current - previous < minSpacing, it's red
    const getDiff = (t1, t2) => {
        const [h1, m1] = t1.split(':').map(Number);
        const [h2, m2] = t2.split(':').map(Number);
        let diff = (h2 * 60 + m2) - (h1 * 60 + m1);
        if (diff < 0) diff += 24 * 60;
        return diff / 60;
    };

    const actualSpacing = getDiff(previousTime, currentTime);
    const isViolation = actualSpacing < minSpacing;

    return (
        <div className="card" style={{ marginTop: "24px" }}>
            <h3 style={{ marginBottom: "20px", fontSize: "16px", color: "var(--text-muted)", display: "flex", alignItems: "center", gap: "8px" }}>
                <Clock size={18} /> Visual Reasoning: Dose Spacing
            </h3>

            <div style={{ position: "relative", height: "60px", padding: "0 20px" }}>
                {/* Timeline Line */}
                <div style={{ position: "absolute", top: "30px", left: "20px", right: "20px", height: "4px", background: "#e2e8f0", borderRadius: "2px" }} />

                {/* Previous Dose */}
                <div style={{ position: "absolute", left: "20px", top: "15px", textAlign: "center" }}>
                    <div style={{ width: "12px", height: "12px", background: "var(--primary)", borderRadius: "50%", margin: "0 auto 8px" }} />
                    <div style={{ fontSize: "12px", fontWeight: 700 }}>{previousTime}</div>
                    <div style={{ fontSize: "10px", color: "var(--text-muted)" }}>Last Dose</div>
                </div>

                {/* Connector Line (Red if violation) */}
                <div style={{
                    position: "absolute",
                    left: "26px",
                    top: "30px",
                    width: "calc(100% - 52px)",
                    height: "4px",
                    background: isViolation ? "var(--danger)" : "var(--safe)",
                    borderRadius: "2px"
                }} />

                {/* Current Dose */}
                <div style={{ position: "absolute", right: "20px", top: "15px", textAlign: "center" }}>
                    <div style={{ width: "12px", height: "12px", background: isViolation ? "var(--danger)" : "var(--primary)", borderRadius: "50%", margin: "0 auto 8px" }} />
                    <div style={{ fontSize: "12px", fontWeight: 700 }}>{currentTime}</div>
                    <div style={{ fontSize: "10px", color: "var(--text-muted)" }}>Current</div>
                </div>
            </div>

            <div style={{ display: "flex", justifyContent: "center", gap: "40px", marginTop: "30px", fontSize: "13px" }}>
                <div style={{ textAlign: "center" }}>
                    <div style={{ color: "var(--text-muted)" }}>Required Spacing</div>
                    <div style={{ fontWeight: 700 }}>{minSpacing}h</div>
                </div>
                <div style={{ textAlign: "center" }}>
                    <div style={{ color: "var(--text-muted)" }}>Actual Gap</div>
                    <div style={{ fontWeight: 700, color: isViolation ? "var(--danger)" : "var(--safe)" }}>{actualSpacing.toFixed(1)}h</div>
                </div>
            </div>
        </div>
    );
};

export default TimelineChart;
