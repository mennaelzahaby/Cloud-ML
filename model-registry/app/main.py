from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app.models import Base, ModelRegistry


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Model Registry API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register_model(
    name: str,
    version: str,
    accuracy: float,
    path: str,
    db: Session = Depends(get_db)
):
    db.query(ModelRegistry).update({ModelRegistry.active: False})

    model = ModelRegistry(
        name=name,
        version=version,
        accuracy=accuracy,
        path=path,
        active=True
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return {"message": "Model registered", "id": model.id}

@app.get("/models")
def list_models(db: Session = Depends(get_db)):
    return db.query(ModelRegistry).all()

@app.get("/active")
def get_active_model(db: Session = Depends(get_db)):
    return db.query(ModelRegistry).filter(ModelRegistry.active == True).first()

from fastapi.responses import HTMLResponse
import requests

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    models = requests.get("http://localhost:8000/models").json()
    active = requests.get("http://localhost:8000/active").json()

    html = """
    <html>
    <head>
        <title>ML Model Dashboard</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
            th { background-color: #f2f2f2; }
            .active { background-color: #d4edda; }
        </style>
    </head>
    <body>
        <h1>📊 ML Model Dashboard</h1>
        <h2>⭐ Active Model</h2>
        <p><b>Name:</b> {active_name}</p>
        <p><b>Version:</b> {active_version}</p>
        <p><b>Accuracy:</b> {active_acc}</p>

        <h2>📋 All Models</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Version</th>
                <th>Accuracy</th>
                <th>Active</th>
            </tr>
    """

    for m in models:
        row_class = "active" if m["active"] else ""
        html += f"""
        <tr class="{row_class}">
            <td>{m["id"]}</td>
            <td>{m["name"]}</td>
            <td>{m["version"]}</td>
            <td>{round(m["accuracy"], 4)}</td>
            <td>{m["active"]}</td>
        </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html.format(
        active_name=active["name"],
        active_version=active["version"],
        active_acc=round(active["accuracy"], 4)
    )
