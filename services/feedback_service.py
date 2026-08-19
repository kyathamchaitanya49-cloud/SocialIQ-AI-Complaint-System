import os
import joblib

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MODELS_FOLDER = os.path.join(PROJECT_ROOT, "models")

vectorizer = joblib.load(
    os.path.join(MODELS_FOLDER, "feedback_tfidf_vectorizer.pkl")
)

model = joblib.load(
    os.path.join(MODELS_FOLDER, "feedback_category_prediction_model.pkl")
)

encoder = joblib.load(
    os.path.join(MODELS_FOLDER, "feedback_label_encoder.pkl")
)


def predict_feedback(text):
    text_lower = text.lower()

    complaint_words = [
        "complaint",
        "problem",
        "issue",
        "not happened",
        "not working",
        "delay",
        "delayed",
        "shortage",
        "please take action",
        "immediate action",
        "waste",
        "garbage"
    ]

    appreciation_words = [
        "thank you",
        "thanks",
        "appreciate",
        "excellent",
        "great service",
        "well done"
    ]

    if any(word in text_lower for word in appreciation_words):
        return "Appreciation"

    if any(word in text_lower for word in complaint_words):
        return "Complaint"

    X = vectorizer.transform([text])
    prediction = model.predict(X)

    return str(encoder.inverse_transform(prediction)[0])