def check_interactions(medicine, other_meds, interactions_data):
    conflicts = []

    for entry in interactions_data:
        if (
            (entry["drugA"] == medicine and entry["drugB"] in other_meds)
            or
            (entry["drugB"] == medicine and entry["drugA"] in other_meds)
        ):
            conflicts.append(entry)

    return conflicts
