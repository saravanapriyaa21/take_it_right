import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { analyzeMedicine } from "../api/api";
import { AlertCircle, Pill, ShieldCheck, Clock, Activity, Heart, Wine } from "lucide-react";
import logo from "../assets/logo.jpg";

const PRESETS = [
  {
    name: "Standard Adult Dose",
    data: { medicine: "paracetamol", dose: "500", time: "14:00", previous_time: "08:00", other_meds: "", alcohol: false, age: "30", pregnant: false, weight: "70" }
  },
  {
    name: "Child Overdose Risk",
    data: { medicine: "paracetamol", dose: "500", time: "14:00", previous_time: "", other_meds: "", alcohol: false, age: "6", pregnant: false, weight: "20" }
  },
  {
    name: "Paracetamol + Alcohol",
    data: { medicine: "paracetamol", dose: "1000", time: "22:00", previous_time: "16:00", other_meds: "", alcohol: true, age: "40", pregnant: false, weight: "80" }
  },
  {
    name: "Multiple Painkillers Together",
    data: { medicine: "ibuprofen", dose: "400", time: "14:00", previous_time: "08:00", other_meds: "aspirin", alcohol: false, age: "25", pregnant: false, weight: "65" }
  },
  {
    name: "Hidden Paracetamol",
    data: { medicine: "crocin", dose: "500", time: "14:00", previous_time: "10:00", other_meds: "dolo_650", alcohol: false, age: "30", pregnant: false, weight: "70" }
  }
];

function InputPage({ setResult }) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    medicine: "",
    dose: "",
    time: "",
    previous_time: "",
    other_meds: "",
    alcohol: false,
    age: "",
    pregnant: false,
    weight: ""
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value
    });
  };

  const handlePreset = (preset) => {
    setFormData(preset.data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const formatted = {
        ...formData,
        dose: Number(formData.dose),
        age: formData.age ? Number(formData.age) : null,
        weight: formData.weight ? Number(formData.weight) : null,
        pregnant: formData.pregnant,
        other_meds: formData.other_meds
          ? formData.other_meds.split(",").map(m => m.trim()).filter(m => m)
          : []
      };

      const result = await analyzeMedicine(formatted);
      setResult(result);
      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      alert(`Analysis failed: ${err.message || "Unknown error"}. Check if the medicine name is recognized.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ paddingTop: "60px" }}>
      <div style={{ textAlign: "center", marginBottom: "40px" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "8px", marginBottom: "16px" }}>
          <img src={logo} alt="Take It Right Logo" style={{ width: "40px", height: "40px", borderRadius: "50%" }} />
          <h1 style={{ fontSize: "32px", letterSpacing: "-0.5px" }}>Take It Right</h1>
        </div>
        <p style={{ color: "var(--text-muted)", fontSize: "18px", fontWeight: 500 }}>
          Not sure about your medicine? Check here.
        </p>
      </div>

      <div style={{ maxWidth: "600px", margin: "0 auto" }}>
        <div className="card" style={{ padding: "30px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "20px", color: "black" }}>
            <Activity size={24} />
            <h2 style={{ fontSize: "20px", fontWeight: 700 }}>See If It’s Safe</h2>
          </div>

          <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
              <div>
                <label style={labelStyle}><Pill size={14} /> Medicine</label>
                <input name="medicine" value={formData.medicine} placeholder="e.g. Paracetamol" onChange={handleChange} required />
              </div>
              <div>
                <label style={labelStyle}>Dose (mg)</label>
                <input name="dose" type="number" value={formData.dose} placeholder="e.g. 500" onChange={handleChange} required />
              </div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
              <div>
                <label style={labelStyle}><Clock size={14} /> Current Time</label>
                <input name="time" type="time" value={formData.time} onChange={handleChange} required />
              </div>
              <div>
                <label style={labelStyle}>Previous Dose Time</label>
                <input name="previous_time" type="time" value={formData.previous_time} onChange={handleChange} />
              </div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
              <div>
                <label style={labelStyle}><AlertCircle size={14} /> Other Medications</label>
                <input name="other_meds" value={formData.other_meds} placeholder="e.g. Ibuprofen" onChange={handleChange} />
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
                <div>
                  <label style={labelStyle}>User Age</label>
                  <input name="age" type="number" min="0" value={formData.age} placeholder="Years" onChange={handleChange} />
                </div>
                <div>
                  <label style={labelStyle}>Weight (kg)</label>
                  <input name="weight" type="number" value={formData.weight} placeholder="kg" onChange={handleChange} />
                </div>
              </div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px", background: "#f8fafc", padding: "12px", borderRadius: "10px", border: "1px solid #e2e8f0" }}>
                <input
                  type="checkbox"
                  name="alcohol"
                  id="alcohol-toggle"
                  checked={formData.alcohol}
                  onChange={handleChange}
                  style={{ width: "20px", height: "20px" }}
                />
                <label htmlFor="alcohol-toggle" style={{ fontWeight: 600, display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "13px" }}>
                  <Wine size={16} /> Alcohol?
                </label>
              </div>

              <div style={{ display: "flex", alignItems: "center", gap: "10px", background: "#f8fafc", padding: "12px", borderRadius: "10px", border: "1px solid #e2e8f0" }}>
                <input
                  type="checkbox"
                  name="pregnant"
                  id="pregnant-toggle"
                  checked={formData.pregnant}
                  onChange={handleChange}
                  style={{ width: "20px", height: "20px" }}
                />
                <label htmlFor="pregnant-toggle" style={{ fontWeight: 600, display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", fontSize: "13px" }}>
                  Pregnant?
                </label>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              style={{
                width: "100%",
                padding: "16px",
                background: "var(--primary)",
                color: "white",
                border: "none",
                borderRadius: "12px",
                fontSize: "18px",
                fontWeight: 700,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: "10px",
                boxShadow: "0 4px 12px rgba(239, 106, 103, 0.2)",
                textTransform: "uppercase",
                letterSpacing: "1px"
              }}
            >
              {loading ? "Checking..." : "Check My Dose"}
            </button>
          </form>
        </div>

        <div style={{ marginTop: "40px" }}>
          <h3 style={{ marginBottom: "16px", color: "#64748b", fontSize: "14px", fontWeight: 700, textTransform: "uppercase" }}>Common Risk Situations</h3>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
            {PRESETS.map((preset) => (
              <button
                key={preset.name}
                onClick={() => handlePreset(preset)}
                style={{
                  background: "white",
                  border: "1px solid #e2e8f0",
                  padding: "14px",
                  borderRadius: "10px",
                  textAlign: "center",
                  fontSize: "14px",
                  fontWeight: 600,
                  boxShadow: "0 1px 2px rgba(0,0,0,0.05)"
                }}
              >
                {preset.name}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

const labelStyle = {
  display: "flex",
  alignItems: "center",
  gap: "6px",
  fontSize: "14px",
  fontWeight: 500,
  marginBottom: "6px",
  color: "#475569"
};

export default InputPage;
