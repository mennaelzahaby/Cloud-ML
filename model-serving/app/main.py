from fastapi import FastAPI, Request
import joblib
import os

app = FastAPI()

MODEL_PATH = "/app/models/model.pkl"
model = None

@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully")
    else:
        print("⚠️ No model found")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(request: Request):
    body = await request.json()

    if model is None:
        return {"error": "Model not loaded"}

    # يقبل:
    # [ [...features...] ]
    # أو
    # {"data": [...features...]}

    if isinstance(body, dict):
        data = body.get("data")
    else:
        data = body

    return {"prediction": model.predict(data).tolist()}
