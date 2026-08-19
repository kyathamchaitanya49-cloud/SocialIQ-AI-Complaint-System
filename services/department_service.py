import os
import joblib

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MODELS_FOLDER = os.path.join(PROJECT_ROOT, "models")

model = joblib.load(
    os.path.join(
        MODELS_FOLDER,
        "government_department_prediction_model.pkl"
    )
)


def predict_department(text):

    text = text.lower().strip()

    # ==============================
    # WATER
    # ==============================
    water_keywords = [
        "water supply",
        "drinking water",
        "no water",
        "water shortage",
        "water leakage",
        "water leak",
        "water pipeline",
        "water pipe",
        "water tank",
        "water problem"
    ]

    if any(word in text for word in water_keywords):
        return "Water Supply Department"


    # ==============================
    # ELECTRICITY
    # ==============================
    electricity_keywords = [
        "electricity",
        "power outage",
        "power cut",
        "no power",
        "electric pole",
        "electric wire",
        "electrical wire",
        "transformer",
        "current",
        "voltage",
        "electric shock"
    ]

    if any(word in text for word in electricity_keywords):
        return "Electricity Department - Electrical Services"


    # ==============================
    # ROADS
    # ==============================
    road_keywords = [
        "road",
        "pothole",
        "potholes",
        "footpath",
        "pavement",
        "highway",
        "road damage",
        "road repair"
    ]

    if any(word in text for word in road_keywords):
        return "Municipal Roads Department"


    # ==============================
    # DRAINAGE
    # ==============================
    drainage_keywords = [
        "drainage",
        "drain",
        "sewer",
        "sewage",
        "blocked drain",
        "drain blockage",
        "sewer blockage"
    ]

    if any(word in text for word in drainage_keywords):
        return "Drainage Department"


    # ==============================
    # SANITATION
    # ==============================
    sanitation_keywords = [
        "garbage",
        "waste",
        "trash",
        "rubbish",
        "garbage collection",
        "waste collection",
        "sanitation",
        "dirty street",
        "dirty roads"
    ]

    if any(word in text for word in sanitation_keywords):
        return "Sanitation Department - Waste Management"


    # ==============================
    # HEALTH
    # ==============================
    health_keywords = [
        "hospital",
        "doctor",
        "medical",
        "health",
        "medicine",
        "clinic",
        "patient",
        "ambulance",
        "treatment"
    ]

    if any(word in text for word in health_keywords):
        return "Health Department - Healthcare Services"


    # ==============================
    # TRAFFIC
    # ==============================
    traffic_keywords = [
        "traffic",
        "traffic signal",
        "traffic light",
        "signal",
        "vehicle",
        "road congestion"
    ]

    if any(word in text for word in traffic_keywords):
        return "Traffic Police"


    # ==============================
    # PARKS
    # ==============================
    parks_keywords = [
        "park",
        "parks",
        "playground",
        "garden"
    ]

    if any(word in text for word in parks_keywords):
        return "Parks Department"


    # ==============================
    # ML FALLBACK
    # ==============================
    try:
        prediction = model.predict([text])[0]
        return str(prediction)

    except Exception as e:
        print("Department prediction error:", e)
        return "Citizen Services"