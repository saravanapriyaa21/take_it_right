def compute_score(
    overdose=False,
    spacing_violation=False,
    conflicts=None,
    alcohol=False,
    liver_load=0,
    kidney_load=0
):
    score = 0
    issues = []

    if overdose:
        score += 50
        issues.append("Overdose risk detected")

    if spacing_violation:
        score += 30
        issues.append("Dose taken too soon")

    if conflicts:
        for conflict in conflicts:
            severity = conflict.get("severity", 1)
            score += severity * 10
            issues.append(f"Interaction risk: {conflict['risk']}")


    if alcohol:
        score += 25
        issues.append("Alcohol interaction risk")

    if liver_load > 0:
        organ_penalty = liver_load * 5
        score += organ_penalty
        if liver_load >= 3:
            issues.append(f"Liver load score is {liver_load}")

    if kidney_load >= 4:
        score += 20
        issues.append("High kidney stress detected")



    if score <= 25:
        level = "SAFE"
    elif score <= 60:
        level = "CAUTION"
    else:
        level = "HIGH RISK"

    return {
        "score": score,
        "risk_level": level,
        "issues": issues
    }
