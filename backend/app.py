from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .schemas import ComplaintRequest
from .crud import create_complaint, save_prediction
from .predict import predict_all


app = FastAPI(
    title="SocialIQ AI Complaint System",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "SocialIQ Backend Running Successfully"
    }


@app.post("/predict")
def predict(request: ComplaintRequest, db: Session = Depends(get_db)):

    print("===== REQUEST RECEIVED =====")
    print(request)

    complaint = create_complaint(
        db,
        request.citizen_name,
        request.complaint
    )

    print("Complaint saved:", complaint.id)

    results = predict_all(request.complaint)

    print("Prediction Results:")
    print(results)

    # Save prediction to database temporarily disabled
# save_prediction(
#     db,
#     complaint.id,
#     results
# )

    print("Prediction saved successfully.")

    return {
        "complaint_id": complaint.id,
        "prediction": results
    }