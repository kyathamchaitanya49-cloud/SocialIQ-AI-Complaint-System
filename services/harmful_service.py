import os
import joblib

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MODELS_FOLDER = os.path.join(PROJECT_ROOT, "models")

harmful_model = joblib.load(
    os.path.join(
        MODELS_FOLDER,
        "harmful_content_prediction_model.pkl"
    )
)


def predict_harmful(text):
    text_lower = text.lower()

    # Normal civic complaints are not harmful
    civic_keywords = [
        "garbage",
        "waste",
        "sanitation",
        "road",
        "water",
        "electricity",
        "street",
        "drainage",
        "government",
        "municipal",
        "complaint",
        "please take action"
    ]

    if any(word in text_lower for word in civic_keywords):
        return "Safe"

    prediction = harmful_model.predict([text])[0]

    labels = {
        0: "Safe",
        1: "Harmful"
    }

    try:
        return labels[int(prediction)]
    except:
        return str(prediction)