import { Link } from "react-router-dom";
import { ArrowLeft, RefreshCw, Heart } from "lucide-react";
import logo from "../assets/logo.jpg";
import RiskGauge from "../components/RiskGauge";
import OrganGauge from "../components/OrganGauge";
import IssueCard from "../components/IssueCard";
import GuidancePanel from "../components/GuidancePanel";
import AIExplanation from "../components/AIExplanation";
import TimelineChart from "../components/TimelineChart";

function Dashboard({ result }) {
  if (!result) return (
    <div className="container" style={{ textAlign: "center", paddingTop: "100px" }}>
      <h2 style={{ marginBottom: "20px" }}>No analysis result found.</h2>
      <Link to="/" style={{ color: "var(--primary)", textDecoration: "none", fontWeight: 600 }}>
        Go back to Input Page
      </Link>
    </div>
  );

  return (
    <div className="container">
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <Link to="/" style={{ display: "flex", alignItems: "center", gap: "8px", textDecoration: "none", color: "var(--text-muted)", fontWeight: 500 }}>
            <ArrowLeft size={18} /> New Case
          </Link>
          <div style={{ height: "24px", width: "1px", background: "var(--border)" }}></div>
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <img src={logo} alt="Logo" style={{ width: "24px", height: "24px", borderRadius: "50%" }} />
            <span style={{ fontWeight: 700, fontSize: "16px", color: "var(--primary)" }}>Take It Right</span>
          </div>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: "12px", color: "var(--text-muted)", fontWeight: 600, textTransform: "uppercase" }}>Analysis Report</div>
          <div style={{ fontSize: "14px", fontWeight: 700 }}>#{Math.random().toString(36).substr(2, 9).toUpperCase()}</div>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "32px", marginBottom: "32px" }}>
        {/* HERO: Risk Gauge */}
        <RiskGauge
          score={result.score}
          riskLevel={result.risk_level}
        />


        {/* SECTION: Organ Load */}
        <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          <h3 style={{ fontSize: "16px", color: "var(--text-muted)", display: "flex", alignItems: "center", gap: "8px" }}>
            <RefreshCw size={18} /> Physiological Metrics
          </h3>
          <div style={{ display: "flex", gap: "16px" }}>
            <OrganGauge title="Liver Load" value={result.liver_load} />
            <OrganGauge title="Kidney Load" value={result.kidney_load} />
          </div>
          <OrganGauge title="Stomach Risk" value={result.stomach_risk} max={10} />
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "32px" }}>
        <div>
          {/* SECTION: Issue Cards */}
          <h3 style={{ marginBottom: "16px", fontSize: "16px", color: "var(--text-muted)" }}>Safety Observations</h3>
          {result.conflicts && result.conflicts.length > 0 ? (
            result.conflicts.map((issue, i) => (
              <IssueCard key={i} issue={issue} />
            ))
          ) : (
            <div className="card" style={{ textAlign: "center", padding: "40px", color: "var(--safe)" }}>
              <div style={{ fontSize: "14px", fontWeight: 600 }}>No safety conflicts detected.</div>
            </div>
          )}

          {/* SECTION: Guidance */}
          <div style={{ marginTop: "24px" }}>
            <GuidancePanel guidance={result.guidance} />
          </div>
        </div>

        <div>
          {/* SECTION: AI Explanation */}
          <AIExplanation text={result.ai_explanation} />

          {/* SECTION: Timeline Chart (Optional but Strong) */}
          <TimelineChart
            previousTime={result.previous_time}
            currentTime={result.time}
            minSpacing={result.min_spacing || 4}
          />
        </div>
      </div>

      {/* Footer CTA */}
      <div style={{ marginTop: "60px", textAlign: "center", borderTop: "1px solid var(--border)", paddingTop: "40px" }}>
        <Link to="/" style={{
          background: "var(--bg-card)",
          border: "1px solid var(--border)",
          padding: "16px 40px",
          borderRadius: "var(--radius-md)",
          textDecoration: "none",
          color: "var(--text-main)",
          fontWeight: 700,
          boxShadow: "var(--shadow-md)"
        }}>
          Start New Check
        </Link>
      </div>
    </div>
  );
}

export default Dashboard;
