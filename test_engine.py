from engine.analyzer import analyze
import itertools

tests = []

# --------------------------------------------------
# 1️⃣ Basic Valid Cases
# --------------------------------------------------

base_valid = [
    {"medicine": "paracetamol", "dose": 500, "time": "14:00"},
    {"medicine": "ibuprofen", "dose": 400, "time": "14:00"},
    {"medicine": "aspirin", "dose": 500, "time": "14:00"},
]

tests.extend(base_valid)


# --------------------------------------------------
# 2️⃣ Spacing Boundaries
# --------------------------------------------------

spacing_cases = [
    {"previous_time": "10:00", "time": "14:00"},  # exact boundary
    {"previous_time": "10:30", "time": "14:00"},  # violation
    {"previous_time": "23:00", "time": "01:00"},  # midnight
]

for case in spacing_cases:
    tests.append({
        "medicine": "paracetamol",
        "dose": 500,
        **case
    })


# --------------------------------------------------
# 3️⃣ Single Dose Extremes
# --------------------------------------------------

dose_values = [0, -100, 500, 1000, 1500, 4000]

for d in dose_values:
    tests.append({
        "medicine": "paracetamol",
        "dose": d,
        "time": "14:00"
    })


# --------------------------------------------------
# 4️⃣ Weight-Based mg/kg Boundaries
# --------------------------------------------------

weights = [10, 20, 25, 30, 50]
doses = [150, 300, 500, 650, 1000]

for w, d in itertools.product(weights, doses):
    tests.append({
        "medicine": "paracetamol",
        "dose": d,
        "weight": w,
        "age": 10,
        "time": "14:00"
    })


# --------------------------------------------------
# 5️⃣ Daily Accumulation
# --------------------------------------------------

dose_histories = [
    [500, 500],
    [1000, 1000],
    [1000, 1000, 1000],
    [1000, 1000, 1000, 500]
]

for history in dose_histories:
    tests.append({
        "medicine": "paracetamol",
        "dose": 500,
        "dose_history": history,
        "time": "14:00"
    })


# --------------------------------------------------
# 6️⃣ Alcohol Combinations
# --------------------------------------------------

for med in ["paracetamol", "ibuprofen", "diclofenac"]:
    tests.append({
        "medicine": med,
        "dose": 500,
        "alcohol": True,
        "time": "22:00"
    })


# --------------------------------------------------
# 7️⃣ Duplicate Ingredient / Brand Expansion
# --------------------------------------------------

brand_tests = [
    {"medicine": "crocin", "dose": 500, "other_meds": ["paracetamol"]},
    {"medicine": "crocin", "dose": 500, "other_meds": ["dolo_650"]},
    {"medicine": "paracetamol", "dose": 500, "other_meds": ["paracetamol"]}
]

for bt in brand_tests:
    bt["time"] = "14:00"
    tests.append(bt)


# --------------------------------------------------
# 8️⃣ NSAID Stacking
# --------------------------------------------------

nsaid_pairs = [
    ("ibuprofen", "aspirin"),
    ("aspirin", "naproxen"),
    ("naproxen", "diclofenac"),
]

for m1, m2 in nsaid_pairs:
    tests.append({
        "medicine": m1,
        "dose": 400,
        "other_meds": [m2],
        "time": "14:00"
    })


# --------------------------------------------------
# 9️⃣ Pregnancy & Age
# --------------------------------------------------

pregnancy_cases = [
    {"medicine": "aspirin", "dose": 500, "pregnant": True},
    {"medicine": "ibuprofen", "dose": 400, "pregnant": True},
]

age_cases = [
    {"medicine": "aspirin", "dose": 500, "age": 5},
    {"medicine": "ibuprofen", "dose": 400, "age": 4},
]

for case in pregnancy_cases + age_cases:
    case["time"] = "10:00"
    tests.append(case)


# --------------------------------------------------
# 🔟 Invalid Inputs
# --------------------------------------------------

invalid_inputs = [
    {"medicine": "paracetamol", "dose": 500, "time": "25:00"},
    {"medicine": "randompill", "dose": 100, "time": "10:00"},
    {"medicine": "paracetamol", "dose": 500, "weight": 0, "time": "14:00"},
]

tests.extend(invalid_inputs)


# --------------------------------------------------
# 11️⃣ Organ Load Stress Tests
# --------------------------------------------------

organ_cases = [
    {"medicine": "diclofenac", "dose": 75, "other_meds": ["ibuprofen"], "alcohol": True},
    {"medicine": "paracetamol", "dose": 1000, "alcohol": True},
]

for case in organ_cases:
    case["time"] = "18:00"
    tests.append(case)


# --------------------------------------------------
# 🔟 Pediatric & Infant Safety (New Rules)
# --------------------------------------------------

pediatric_tests = [
    # 1. Infant Hard Stop (< 5kg)
    {"medicine": "paracetamol", "dose": 60, "weight": 4.5, "time": "14:00"},
    
    # 2. Child < 12 without weight (Caution)
    {"medicine": "paracetamol", "dose": 250, "age": 8, "time": "14:00"},
    
    # 3. Paracetamol mg/kg Single Dose (20mg/kg -> High Risk)
    {"medicine": "paracetamol", "dose": 500, "weight": 20, "time": "14:00"}, # 25mg/kg
    
    # 4. Paracetamol mg/kg Single Dose (15-20mg/kg -> Caution)
    {"medicine": "paracetamol", "dose": 350, "weight": 20, "time": "14:00"}, # 17.5mg/kg
    
    # 5. Paracetamol daily accumulation (>75mg/kg -> High Risk)
    {"medicine": "paracetamol", "dose": 500, "dose_history": [1000, 1000, 500], "weight": 30, "time": "20:00"}, # ~83mg/kg
    
    # 6. Paracetamol daily accumulation (60-75mg/kg -> Caution)
    {"medicine": "paracetamol", "dose": 500, "dose_history": [500, 500, 500, 500], "weight": 30, "time": "20:00"}, # ~66mg/kg
]

for case in pediatric_tests:
    tests.append(case)

print(f"\nTOTAL TESTS: {len(tests)}")

# 21 Invalid age (Negative)
tests.append({
    "medicine": "paracetamol",
    "dose": 500,
    "age": -1,
    "time": "14:00"
})

for i, test in enumerate(tests, 1):
    print(f"\n--- TEST {i} ---")
    try:
        result = analyze(test)
        print(result)
    except Exception as e:
        print("CRASHED:", e)
