import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None

def generate_explanation(risk_data):

    # ---- Core Inputs ----
    risk_level = risk_data.get("risk_level", "UNKNOWN")
    liver = risk_data.get("liver_load", 0)
    kidney = risk_data.get("kidney_load", 0)
    stomach = risk_data.get("stomach_risk", 0)
    issues = risk_data.get("conflicts", [])

    # ---- Customization Controls ----
    mode = risk_data.get("mode", "standard")
    detail = risk_data.get("detail", "medium")
    strength = risk_data.get("strength", "normal")
    audience = risk_data.get("audience", "general")

    explanation = []
    added_flags = set()

    # -------------------------
    # 1️⃣ Opening Tone Control
    # -------------------------
    opening_templates = {
        "reassuring": {
            "HIGH RISK": "There is a high level of risk right now, but it can be managed with the right steps.",
            "CAUTION": "There is some risk present, but it may be reduced with adjustments.",
            "SAFE": "Based on the current inputs, no major safety concerns were detected."
        },
        "standard": {
            "HIGH RISK": "This situation carries a high safety risk based on the current inputs.",
            "CAUTION": "There is a moderate safety concern with the current timing or combination.",
            "SAFE": "Based on the current inputs, no major safety concerns were detected."
        },
        "firm": {
            "HIGH RISK": "This situation presents a serious safety risk and requires caution.",
            "CAUTION": "There is a noticeable safety concern that should not be ignored.",
            "SAFE": "Risk appears minimal under current conditions."
        }
    }

    explanation.append(
        opening_templates.get(mode, opening_templates["standard"])
        .get(risk_level, "The current safety level could not be determined.")
    )

    # -------------------------
    # 2️⃣ Dominant Organ Logic
    # -------------------------
    organ_scores = {"liver": liver, "kidney": kidney, "stomach": stomach}
    main_organ = max(organ_scores, key=organ_scores.get)
    main_value = organ_scores[main_organ]

    if main_value >= 4:
        organ_phrases = {
            "general": {
                "liver": "There is stress on the liver.",
                "kidney": "There is strain on the kidneys.",
                "stomach": "There is irritation risk in the stomach."
            },
            "clinical": {
                "liver": "Liver strain is elevated.",
                "kidney": "Renal stress levels are increased.",
                "stomach": "Gastrointestinal irritation risk is elevated."
            }
        }

        explanation.append(organ_phrases[audience][main_organ])

        if detail in ["medium", "high"]:
            explanation.append(
                "This may reduce the body's ability to safely handle additional dosing."
            )

    # -------------------------
    # 3️⃣ Conflict Awareness
    # -------------------------
    for issue in issues:
        if not isinstance(issue, dict) or "risk" not in issue:
            continue

        text = issue["risk"].lower()

        if "pregnancy" in text and "pregnancy" not in added_flags:
            explanation.append(
                "This medication is generally not recommended during pregnancy."
            )
            added_flags.add("pregnancy")

        elif "age" in text and "age" not in added_flags:
            explanation.append(
                "This medication may not be appropriate for the given age."
            )
            added_flags.add("age")

        elif "duplicate" in text and "duplicate" not in added_flags:
            explanation.append(
                "The same active ingredient appears more than once, which increases risk."
            )
            added_flags.add("duplicate")

        elif "nsaid" in text and "nsaid" not in added_flags:
            explanation.append(
                "Combining multiple anti-inflammatory medicines increases safety risk."
            )
            added_flags.add("nsaid")

        elif "dose" in text and "dose" not in added_flags:
            explanation.append(
                "The total dose exceeds recommended limits."
            )
            added_flags.add("dose")

        elif "liver" in text and "liver" not in added_flags and main_value < 4:
            explanation.append(
                "There is significant stress on the liver."
            )
            added_flags.add("liver")

        elif "kidney" in text and "kidney" not in added_flags and main_value < 4:
            explanation.append(
                "Kidney strain is contributing to the overall risk."
            )
            added_flags.add("kidney")

    # -------------------------
    # 4️⃣ Strength-Based Closing
    # -------------------------
    closing_templates = {
        "soft": "Consider waiting before the next dose to lower potential risk.",
        "normal": "Waiting before the next dose may help reduce potential harm.",
        "strict": "It is strongly recommended to wait before taking another dose and avoid additional risk factors."
    }

    if risk_level == "SAFE":
        if risk_data.get("medicine") == "paracetamol":
            explanation.append(
                "The current paracetamol dose is well within recommended pediatric or adult safety limits for the given weight and timing."
            )
        else:
            explanation.append(
                "Following the recommended schedule should remain appropriate."
            )
    else:
        explanation.append(
            closing_templates.get(strength, closing_templates["normal"])
        )

    # -------------------------
    # 5️⃣ Professional Boundary
    # -------------------------
    severe_case = (
        risk_level == "HIGH RISK" or
        liver >= 6 or
        kidney >= 5
    )

    if severe_case:
        explanation.append(
            "This assessment provides general medication safety guidance and does not replace professional medical evaluation."
        )

    return " ".join(explanation)
