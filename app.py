from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import joblib

MODEL_PATH = "artifacts/ticket_classifier_pipeline.joblib"
LABELS_PATH = "artifacts/label_encoder.joblib"

clf = joblib.load(MODEL_PATH)
le = joblib.load(LABELS_PATH)

AUTO_RESPONSES = {
    "Billing": "Please provide invoice number or billing details.",
    "Technical Issue": "Please share error message and device details.",
    "Feature Request": "Thanks! We will share this with product team.",
}
DEFAULT_RESPONSE = "Thanks, we will review your request."

app = FastAPI(title="SmartTicketAI")

# ✅ Serve static UI files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# ✅ Homepage route
@app.get("/")
def home():
    return FileResponse(Path("src/static/index.html"))

class Ticket(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(ticket: Ticket):
    if not ticket.text.strip():
        raise HTTPException(status_code=400, detail="Empty text.")
    pred = clf.predict([ticket.text])[0]
    label = le.inverse_transform([pred])[0]
    conf = float(clf.predict_proba([ticket.text])[0].max())
    resp = AUTO_RESPONSES.get(label, DEFAULT_RESPONSE)
    return {"label": label, "confidence": conf, "suggested_response": resp}
