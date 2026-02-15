import json
from datetime import datetime
from collections import Counter

from engine.spacing import check_spacing
from engine.overdose import check_overdose
from engine.interactions import check_interactions
from engine.scoring import compute_score


# ----------------------------
# Load configuration files
# ----------------------------

def load_rules():
    with open("engine/rules.json") as f:
        return json.load(f)


def load_interactions():
    with open("engine/interactions.json") as f:
        return json.load(f)


def load_brand_map():
    with open("engine/brand_map.json") as f:
        return json.load(f)


# ----------------------------
# Utility
# ----------------------------

def calculate_remaining_time(previous_time, current_time, min_spacing):
    fmt = "%H:%M"
    prev = datetime.strptime(previous_time, fmt)
    curr = datetime.strptime(current_time, fmt)

    if curr < prev:
        curr = curr.replace(day=prev.day + 1)

    hours_passed = (curr - prev).total_seconds() / 3600
    remaining = min_spacing - hours_passed

    return round(remaining, 1) if remaining > 0 else 0


# ----------------------------
# Guidance Generator
# ----------------------------
def generate_guidance(
    spacing_violation,
    overdose,
    near_limit,
    liver_load,
    kidney_load,
    stomach_risk,
    nsaid_stacking,
    min_spacing_hours,
    previous_time,
    time,
    risk_level,
    absolute_block,
    medicine="general",
    conflicts=None,
    age=None,
    weight=None
):

    # Hard stop for contraindications
    if absolute_block:
        # Check for specific infant block
        if conflicts:
            infant_risk = next((c for c in conflicts if "infants" in c["risk"].lower()), None)
            if infant_risk:
                return [infant_risk["risk"]]
                
        return [
            "Avoid taking this medication until you speak to a healthcare professional."
        ]

    guidance = []

    if spacing_violation and previous_time:
        remaining = calculate_remaining_time(
            previous_time,
            time,
            min_spacing_hours
        )
        if remaining >= 1:
            guidance.append(
                f"Wait about {remaining} hour(s) before the next dose."
            )
        elif remaining > 0:
            guidance.append(
                f"Wait about {int(remaining * 60)} minutes before the next dose."
            )

    if overdose:
        guidance.append(
            "You have reached the daily safety limit. Do not take another dose today."
        )

    elif near_limit:
        guidance.append(
            "You are close to the maximum daily dose. Avoid further dosing."
        )

    if liver_load >= 4:
        guidance.append(
            "Avoid alcohol or other liver-impacting substances."
        )

    if kidney_load >= 4:
        guidance.append(
            "High kidney stress detected. Avoid additional strain."
        )

    if stomach_risk >= 5:
        guidance.append(
            "Taking medication with food may reduce stomach irritation."
        )

    if nsaid_stacking:
        guidance.append(
            "Avoid combining multiple NSAID medications."
        )

    # Only reassure if SAFE
    if not guidance and risk_level == "SAFE":
        # Pediatric Reassurance
        if age and age < 18 and weight:
            guidance.append("The entered dose is within safe weight-based limits for this age.")

        if medicine == "paracetamol":
            guidance.append("Current usage is within safety limits. Do not exceed 4000mg total in 24 hours.")
        elif not (age and age < 18 and weight):
            guidance.append("Current usage appears within safety limits.")

    if not guidance and risk_level == "HIGH RISK":
        guidance.append(
            "This situation carries a significant safety risk. Please do not take this dose and consult a healthcare professional."
        )

    return guidance



# ----------------------------
# Main Analyzer
# ----------------------------

def analyze(input_data):

    rules = load_rules()
    interactions_data = load_interactions()
    brand_map = load_brand_map()

    medicine = input_data["medicine"].lower()
    dose = input_data["dose"]
    dose_history = input_data.get("dose_history", [dose])
    time = input_data["time"]
    previous_time = input_data.get("previous_time")
    other_meds = [m.lower() for m in input_data.get("other_meds", [])]
    alcohol = input_data.get("alcohol", False)
    age = input_data.get("age")
    weight = input_data.get("weight")
    pregnant = input_data.get("pregnant", False)

    conflicts = []
    absolute_block = False

    # ---------------- Validation ----------------

    if weight is not None:
        try:
            weight = float(weight)
            if weight <= 0:
                return {"error": "Invalid weight value: must be positive"}
            
            # infant hard stop
            if weight < 5:
                absolute_block = True
                conflicts.append({
                    "risk": "Infants require pediatric supervision for medication dosing.",
                    "severity": 10
                })
        except (ValueError, TypeError):
            return {"error": "Invalid weight format: must be a number"}

    if age is not None:
        try:
            age = float(age)
            if age < 0:
                return {"error": "Invalid age value: must be zero or positive"}
            
            # pediatric caution without weight
            if age < 12 and weight is None:
                conflicts.append({
                    "risk": "Weight-based dosing is required for children.",
                    "severity": 5
                })
        except (ValueError, TypeError):
            return {"error": "Invalid age format: must be a number"}

    if not isinstance(dose, (int, float)) or dose <= 0:
        return {"error": "Invalid dose value"}

    if not isinstance(dose_history, list) or not all(
        isinstance(d, (int, float)) and d > 0 for d in dose_history
    ):
        return {"error": "Invalid dose_history format"}

    try:
        datetime.strptime(time, "%H:%M")
    except:
        return {"error": "Invalid time format. Use HH:MM"}

    if previous_time:
        try:
            datetime.strptime(previous_time, "%H:%M")
        except:
            return {"error": "Invalid previous_time format. Use HH:MM"}

    # ---------------- Brand Expansion ----------------

    def expand(med):
        return brand_map.get(med, [med])

    expanded_primary = expand(medicine)
    expanded_others = []

    for m in other_meds:
        expanded_others.extend(expand(m))

    expanded_all = expanded_primary + expanded_others

    if alcohol:
        expanded_all.append("alcohol")

    primary = expanded_primary[0]

    if primary not in rules:
        return {"error": "Medicine not found in rules"}

    # ---------------- Spacing ----------------

    spacing_violation = False
    if previous_time:
        spacing_violation = check_spacing(
            previous_time,
            time,
            rules[primary]["min_spacing_hours"]
        )

    # ---------------- Overdose & Near Limit ----------------

    overdose, total_dose = check_overdose(
        dose_history,
        rules[primary]["max_daily_dose"],
        rules[primary]["single_dose_limit"]
    )

    max_daily = rules[primary]["max_daily_dose"]
    
    # Stricter paracetamol accumulation
    if primary == "paracetamol":
        near_limit = (total_dose >= 0.75 * max_daily) and not overdose
    else:
        near_limit = (total_dose >= 0.85 * max_daily) and not overdose

    # ---------------- Interactions ----------------

    for i in range(len(expanded_all)):
        for j in range(i + 1, len(expanded_all)):
            conflicts.extend(
                check_interactions(
                    expanded_all[i],
                    [expanded_all[j]],
                    interactions_data
                )
            )

    # ---------------- Weight-Based Dosing (Paracetamol) ----------------
    
    dose_per_kg = 0
    if primary == "paracetamol" and weight:
        dose_per_kg = dose / weight
        if dose_per_kg > 20:
            absolute_block = True
            conflicts.append({
                "risk": f"Paracetamol dose too high for weight ({round(dose_per_kg, 1)}mg/kg > 20mg/kg)",
                "severity": 10
            })
        elif dose_per_kg > 15:
            conflicts.append({
                "risk": f"Paracetamol dose requires caution for weight ({round(dose_per_kg, 1)}mg/kg > 15mg/kg)",
                "severity": 4
            })

    # ---------------- Daily mg/kg Accumulation (Paracetamol) ----------------

    if primary == "paracetamol" and weight:
        total_dose_per_kg = total_dose / weight
        
        if total_dose_per_kg > 75:
            absolute_block = True
            conflicts.append({
                "risk": f"Critical daily paracetamol accumulation ({round(total_dose_per_kg, 1)}mg/kg > 75mg/kg)",
                "severity": 10
            })
        elif total_dose_per_kg > 60:
            conflicts.append({
                "risk": f"High daily paracetamol accumulation ({round(total_dose_per_kg, 1)}mg/kg > 60mg/kg)",
                "severity": 4
            })

    # ---------------- Contraindications ----------------

   

    for med in expanded_primary:
        contra = rules[med].get("contraindications", {})

        if pregnant and contra.get("pregnancy"):
            absolute_block = True
            conflicts.append({
                "risk": f"{med} contraindicated in pregnancy",
                "severity": 7
            })

        if age and age < contra.get("min_age", 0):
            absolute_block = True
            conflicts.append({
                "risk": f"{med} contraindicated for this age",
                "severity": 5
            })

    # ---------------- Duplicate Ingredient ----------------

    # Collect both name and ingredients to detect "hidden" ones
    all_pairs = []
    for med in [medicine] + other_meds:
        ingredients = expand(med)
        for ing in ingredients:
            all_pairs.append({"name": med, "ingredient": ing})

    if alcohol:
        all_pairs.append({"name": "alcohol", "ingredient": "alcohol"})

    # Count ingredient occurrences
    ing_counts = Counter(p["ingredient"] for p in all_pairs)

    duplicate_ingredients = [ing for ing, count in ing_counts.items() if count > 1 and ing in rules]

    for ing in duplicate_ingredients:
        # Check if the names used are different
        names_for_this_ing = set(p["name"] for p in all_pairs if p["ingredient"] == ing)
        
        if len(names_for_this_ing) > 1:
            # Different names = Hidden Duplicate
            if ing == "paracetamol":
                absolute_block = True
                conflicts.append({
                    "risk": "Critical: Hidden duplicate paracetamol detected across brands",
                    "severity": 10
                })
            else:
                conflicts.append({
                    "risk": f"Hidden duplicate {ing} detected across different brands",
                    "severity": 7
                })
        else:
            # Same name used multiple times
            if ing == "paracetamol":
                # For same-name paracetamol, we don't absolute block (overdose handles it)
                # but we still warn.
                conflicts.append({
                    "risk": "Multiple doses of paracetamol detected",
                    "severity": 2
                })
            else:
                conflicts.append({
                    "risk": f"Multiple doses of {ing} detected",
                    "severity": 2
                })

    duplicate_stacking = len(duplicate_ingredients) > 0

    # ---------------- Organ Load ----------------

    liver_load = 0
    stomach_risk = 0
    kidney_load = 0

    for med in expanded_all:
        if med in rules:
            liver_load += rules[med]["liver_load"]
            stomach_risk += rules[med]["stomach_risk"]
            kidney_load += rules[med].get("kidney_load", 0)

    # Severe organ escalation
    if liver_load >= 6:
        absolute_block = True
        conflicts.append({
            "risk": "Severe liver stress detected",
            "severity": 5
        })

    if kidney_load >= 4:
        absolute_block = True
        conflicts.append({
            "risk": "High kidney stress detected",
            "severity": 5
        })

    # ---------------- NSAID Stacking ----------------

    nsaid_list = ["ibuprofen", "aspirin", "naproxen", "diclofenac"]
    nsaid_count = sum(1 for med in expanded_all if med in nsaid_list)
    nsaid_stacking = nsaid_count > 1

    if nsaid_stacking:
        conflicts.append({
            "risk": "NSAID stacking",
            "severity": 4
        })

    # ---------------- Alcohol Synergy Escalation ----------------
    
    if alcohol and primary == "paracetamol":
        absolute_block = True
        conflicts.append({
            "risk": "Alcohol significantly increases paracetamol liver toxicity",
            "severity": 10
        })

    # ---------------- Conflict Deduplication ----------------
    unique_conflicts = {}
    for conflict in conflicts:
        key = conflict["risk"].lower()

        # Group similar liver-related risks
        if "liver" in key:
            key = "liver_issue"
        elif "kidney" in key:
            key = "kidney_issue"
        elif "duplicate" in key:
            key = "duplicate_issue"
        elif "nsaid" in key:
            key = "nsaid_issue"

        # Keep highest severity version
        if key not in unique_conflicts or conflict["severity"] > unique_conflicts[key]["severity"]:
            unique_conflicts[key] = conflict

    conflicts = list(unique_conflicts.values())

    # ---------------- Scoring ----------------

    result = compute_score(
        overdose=overdose,
        spacing_violation=spacing_violation,
        conflicts=conflicts,
        alcohol=alcohol,
        liver_load=liver_load,
        kidney_load=kidney_load
    )

    result["score"] = min(result["score"], 100)

    # ---------------- Deterministic Risk Logic ----------------

    if absolute_block:
        risk_level = "HIGH RISK"

    elif overdose:
        risk_level = "HIGH RISK"

    elif near_limit:
        risk_level = "CAUTION"

    elif result["score"] <= 25:
        risk_level = "SAFE"

    elif result["score"] <= 60:
        risk_level = "CAUTION"

    else:
        risk_level = "HIGH RISK"

    result["risk_level"] = risk_level

    # ---------------- Guidance ----------------

    result["guidance"] = generate_guidance(
        spacing_violation,
        overdose,
        near_limit,
        liver_load,
        kidney_load,
        stomach_risk,
        nsaid_stacking,
        rules[primary]["min_spacing_hours"],
        previous_time,
        time,
        risk_level,
        absolute_block,
        primary,
        conflicts,
        age,
        weight
    )


    
    result["conflicts"] = conflicts
    result["liver_load"] = liver_load
    result["stomach_risk"] = stomach_risk
    result["kidney_load"] = kidney_load
    result["nsaid_stacking"] = nsaid_stacking
    result["duplicate_stacking"] = duplicate_stacking
    result["total_dose"] = total_dose
    result["min_spacing"] = rules[primary]["min_spacing_hours"]

    print("FINAL RESULT:", result)

    return result
