"""
seed.py - Populates the database with 50 realistic records for dev/testing.

Run locally : uv run python seed.py
Docker      : controlled by SEED_ENABLED env var in entrypoint.sh
"""
import sys
from app.core.database import engine, SessionLocal
from app.core.config import settings
from app.models.models import AuthKey, Meal, Complaint, Hospital

from app.core.database import Base
from app.models import models as _m  # noqa – register all models
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # ── API Keys ────────────────────────────────────────────────────────────────
    api_keys = [
        {"api_key": "default-key-aCW5eV_VAL20k9MToEUOoFHQ2_DIXu80GxJYIkPSAIc", "client_name": "Default Client"},
        {"api_key": "dev-key-iMq39muMWJ2AHRoDNncztH4BhIGhyPwUn0JZZZCLbgc",     "client_name": "Dev Client"},
        {"api_key": "prod-key-32ZQf_8o0kh1D5xnflhCZjz5vTxp6XZTmUfnS0nWM1A",    "client_name": "Prod Client"},
    ]
    for entry in api_keys:
        if not db.query(AuthKey).filter(AuthKey.api_key == entry["api_key"]).first():
            db.add(AuthKey(**entry))
            print(f"  [AuthKey] Added   : {entry['client_name']}")
        else:
            print(f"  [AuthKey] Exists  : {entry['client_name']}")

    # ── Hospitals (10 world-renowned) ────────────────────────────────────────────
    hospitals = [
        {"name": "Mayo Clinic",                     "specialty": "General & Cardiology",      "rating": 4.9, "contact": "+1-507-284-2511", "address": "200 First St SW, Rochester, MN"},
        {"name": "Cleveland Clinic",                "specialty": "Cardiology & Surgery",      "rating": 4.8, "contact": "+1-800-223-2273", "address": "9500 Euclid Ave, Cleveland, OH"},
        {"name": "Johns Hopkins Hospital",          "specialty": "Oncology & Neurology",      "rating": 4.8, "contact": "+1-410-955-5000", "address": "1800 Orleans St, Baltimore, MD"},
        {"name": "Massachusetts General Hospital",  "specialty": "General & Research",        "rating": 4.7, "contact": "+1-617-726-2000", "address": "55 Fruit St, Boston, MA"},
        {"name": "Stanford Health Care",            "specialty": "Nutrition & Endocrine",     "rating": 4.7, "contact": "+1-650-723-4000", "address": "300 Pasteur Dr, Stanford, CA"},
        {"name": "UCSF Medical Center",             "specialty": "Gastroenterology",          "rating": 4.6, "contact": "+1-415-476-1000", "address": "505 Parnassus Ave, San Francisco, CA"},
        {"name": "Mount Sinai Hospital",            "specialty": "Internal Medicine",         "rating": 4.6, "contact": "+1-212-241-6500", "address": "1 Gustave L. Levy Pl, New York, NY"},
        {"name": "UCLA Medical Center",             "specialty": "Sports & Metabolic Health", "rating": 4.5, "contact": "+1-310-825-9111", "address": "757 Westwood Plaza, Los Angeles, CA"},
        {"name": "Toronto General Hospital",        "specialty": "Bariatric & Nutrition",     "rating": 4.5, "contact": "+1-416-340-4800", "address": "200 Elizabeth St, Toronto, ON"},
        {"name": "King's College Hospital",         "specialty": "Dietetics & GI",            "rating": 4.4, "contact": "+44-20-3299-9000", "address": "Denmark Hill, London, UK"},
    ]
    for h in hospitals:
        if not db.query(Hospital).filter(Hospital.name == h["name"]).first():
            db.add(Hospital(**h))
            print(f"  [Hospital] Added  : {h['name']} (⭐ {h['rating']})")
        else:
            print(f"  [Hospital] Exists : {h['name']}")

    # ── 30 Diverse Meals ─────────────────────────────────────────────────────────
    meals = [
        # Proteins
        {"name": "Grilled Chicken Breast (200g)",   "protein": 46.0, "carbs":  0.0, "fat":  5.0},
        {"name": "Salmon Fillet (180g)",             "protein": 40.0, "carbs":  0.0, "fat": 14.0},
        {"name": "Beef Steak (200g)",                "protein": 50.0, "carbs":  0.0, "fat": 18.0},
        {"name": "Tuna Can (140g)",                  "protein": 33.0, "carbs":  0.0, "fat":  1.5},
        {"name": "Turkey Breast (150g)",             "protein": 35.0, "carbs":  0.0, "fat":  3.0},
        {"name": "Egg Omelette (3 eggs)",            "protein": 18.0, "carbs":  1.0, "fat": 14.0},
        {"name": "Cottage Cheese (200g)",            "protein": 24.0, "carbs":  6.0, "fat":  4.0},
        {"name": "Whey Protein Shake",               "protein": 28.0, "carbs":  5.0, "fat":  2.0},
        # Carbs
        {"name": "Brown Rice (1 cup cooked)",        "protein":  5.0, "carbs": 45.0, "fat":  2.0},
        {"name": "Quinoa Bowl (200g)",               "protein":  8.0, "carbs": 39.0, "fat":  4.0},
        {"name": "Oatmeal with Honey (1 cup)",       "protein":  6.0, "carbs": 54.0, "fat":  3.5},
        {"name": "Whole Wheat Pasta (200g)",         "protein":  8.0, "carbs": 43.0, "fat":  1.5},
        {"name": "Sweet Potato (200g)",              "protein":  4.0, "carbs": 41.0, "fat":  0.1},
        {"name": "Multigrain Bread (2 slices)",      "protein":  6.0, "carbs": 26.0, "fat":  2.0},
        {"name": "Banana (1 medium)",                "protein":  1.3, "carbs": 27.0, "fat":  0.4},
        # Fats & Mixed
        {"name": "Avocado Toast (1 slice + half)",   "protein":  8.0, "carbs": 30.0, "fat": 14.0},
        {"name": "Mixed Nuts (30g)",                 "protein":  5.0, "carbs":  6.0, "fat": 16.0},
        {"name": "Peanut Butter (2 tbsp)",           "protein":  8.0, "carbs":  6.0, "fat": 16.0},
        {"name": "Full-Fat Greek Yogurt (200g)",     "protein": 18.0, "carbs": 10.0, "fat":  8.0},
        {"name": "Cheese Omelette + Veggies",        "protein": 22.0, "carbs":  5.0, "fat": 17.0},
        # Salads & Vegetables
        {"name": "Caesar Salad (300g)",              "protein": 10.0, "carbs": 12.0, "fat": 18.0},
        {"name": "Mixed Vegetable Stir-fry",         "protein":  6.0, "carbs": 20.0, "fat":  8.0},
        {"name": "Lentil Soup (400ml)",              "protein": 18.0, "carbs": 40.0, "fat":  3.0},
        {"name": "Chickpea Salad (300g)",            "protein": 15.0, "carbs": 45.0, "fat":  7.0},
        {"name": "Spinach & Feta Wrap",              "protein": 14.0, "carbs": 38.0, "fat": 12.0},
        # Snacks & Smoothies
        {"name": "Protein Bar (60g)",                "protein": 20.0, "carbs": 25.0, "fat":  7.0},
        {"name": "Berry Protein Smoothie",           "protein": 22.0, "carbs": 30.0, "fat":  3.0},
        {"name": "Apple + Almond Butter",            "protein":  5.0, "carbs": 28.0, "fat":  9.0},
        {"name": "Rice Cakes with Hummus (3 pcs)",   "protein":  6.0, "carbs": 24.0, "fat":  5.0},
        {"name": "Dark Chocolate (40g, 85%)",        "protein":  4.0, "carbs": 12.0, "fat": 14.0},
    ]
    for m in meals:
        calories = round((m["protein"] * 4) + (m["carbs"] * 4) + (m["fat"] * 9), 2)
        db.add(Meal(calories=calories, **m))
        print(f"  [Meal]     Added  : {m['name'][:42]:<42} ({calories:.0f} kcal)")

    # ── 10 Health Complaints ──────────────────────────────────────────────────────
    complaints = [
        {"description": "Mild headache after lunch",                                "severity": 3},
        {"description": "Feeling bloated after high-carb meal",                     "severity": 4},
        {"description": "Low energy in the afternoon, possible blood sugar drop",   "severity": 5},
        {"description": "Minor muscle soreness after leg day",                      "severity": 2},
        {"description": "Good energy levels throughout the day",                    "severity": 1},
        {"description": "Persistent nausea after dinner for 2 days",               "severity": 6},
        {"description": "Severe chest tightness and shortness of breath",           "severity": 9},
        {"description": "Persistent high fever (39.5°C) lasting 3 days",           "severity": 8},
        {"description": "Sudden sharp abdominal pain, cannot stand straight",       "severity": 10},
        {"description": "Mild dizziness when standing up quickly",                  "severity": 3},
    ]
    for c in complaints:
        flag = " ⚠️  → will auto-book appointment" if c["severity"] >= settings.severity_alert_threshold else ""
        db.add(Complaint(**c))
        print(f"  [Complaint] Added  : severity={c['severity']}{flag} | {c['description'][:45]}")

    db.commit()
    print(f"\n✅ Seed complete — {len(api_keys)} keys, {len(hospitals)} hospitals, {len(meals)} meals, {len(complaints)} complaints.")
    print(f"   Total records : {len(api_keys) + len(hospitals) + len(meals) + len(complaints)}")
    print(f"   Severity threshold : {settings.severity_alert_threshold}")

except Exception as e:
    db.rollback()
    print(f"\n❌ Seed failed: {e}", file=sys.stderr)
    sys.exit(1)

finally:
    db.close()
