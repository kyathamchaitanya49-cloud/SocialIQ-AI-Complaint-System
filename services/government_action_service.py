import joblib
import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MODELS = os.path.join(PROJECT_ROOT, "models")

model = joblib.load(
    os.path.join(
        MODELS,
        "government_department_prediction_model.pkl"
    )
)


def predict_government_action(text):
    text_lower = text.lower()

    # Garbage / waste / sanitation
    if any(word in text_lower for word in [
        "garbage",
        "waste",
        "trash",
        "rubbish",
        "sanitation",
        "dustbin",
        "garbage collection",
        "waste collection"
    ]):
        return "Sanitation Department - Waste Management"

    # Electricity
    if any(word in text_lower for word in [
        "electricity",
        "power cut",
        "power outage",
        "transformer",
        "electric pole"
    ]):
        return "Electricity Department - Electrical Services"

    # Water
    if any(word in text_lower for word in [
        "water supply",
        "water leakage",
        "water shortage",
        "pipeline"
    ]):
        return "Water Supply Department"

    # Roads
    if any(word in text_lower for word in [
        "road",
        "pothole",
        "street",
        "footpath"
    ]):
        return "Municipal Roads Department"

    # Drainage
    if any(word in text_lower for word in [
        "drainage",
        "sewer",
        "sewage",
        "drain"
    ]):
        return "Drainage Department - Drainage and Sewerage Services"

    # ML fallback
    prediction = model.predict([text])[0]

    return str(prediction)