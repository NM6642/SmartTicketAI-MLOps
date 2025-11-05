from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from pydantic import BaseModel
from pathlib import Path
import joblib

# Model paths
MODEL_PATH = "artifacts/ticket_classifier_pipeline.joblib"
LABELS_PATH = "artifacts/label_encoder.joblib"

# Load model artifacts
clf = joblib.load(MODEL_PATH)
le = joblib.load(LABELS_PATH)

AUTO_RESPONSES = {
    "Billing": "Please provide invoice number or billing details.",
    "Technical Issue": "Please share error message and device details.",
    "Feature Request": "Thanks! We will share this with the product team."
}

DEFAULT_RESPONSE = "Thanks, we will review your request."

app = FastAPI(title="SmartTicketAI", version="1.0.0")

# Mount static folder if present
static_dir = Path("src/static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Serve homepage or fallback to docs
@app.get("/", response_class=HTMLResponse)
def home():
    index_path = static_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return RedirectResponse(url="/docs")


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}


# Input model
class Ticket(BaseModel):
    text: str


# Prediction endpoint
@app.post("/predict")
def predict(ticket: Ticket):
    if not ticket.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    pred = clf.predict([ticket.text])[0]
    label = le.inverse_transform([pred])[0]
    confidence = float(clf.predict_proba([ticket.text])[0].max())

    suggested = AUTO_RESPONSES.get(label, DEFAULT_RESPONSE)

    return {
        "label": label,
        "confidence": confidence,
        "suggested_response": suggested
    }
