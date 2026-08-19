import os
import joblib

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MODELS_FOLDER = os.path.join(PROJECT_ROOT, "models")

sentiment_model = joblib.load(
    os.path.join(
        MODELS_FOLDER,
        "government_sentiment_prediction_model.pkl"
    )
)


def predict_sentiment(text):
    text_lower = text.lower()

    negative_words = [
        "not happened",
        "problem",
        "issue",
        "bad",
        "worst",
        "dirty",
        "piling",
        "delay",
        "delayed",
        "failed",
        "complaint",
        "shortage",
        "no service",
        "not working"
    ]

    positive_words = [
        "thank",
        "thanks",
        "excellent",
        "good service",
        "appreciate",
        "well done"
    ]

    if any(word in text_lower for word in negative_words):
        return "Negative"

    if any(word in text_lower for word in positive_words):
        return "Positive"

    prediction = sentiment_model.predict([text])[0]

    return str(prediction)