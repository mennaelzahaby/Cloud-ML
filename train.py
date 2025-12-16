import joblib
import requests
import os
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def main():
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print("Training completed. Accuracy:", acc)

    # ✅ أهم سطر
    os.makedirs("/app/models", exist_ok=True)

    model_path = "/app/models/model.pkl"
    joblib.dump(model, model_path)
    print("Model saved to", model_path)

    registry_url = "http://model-registry:8000/register"
    params = {
        "name": "breast_cancer_model",
        "version": "v1",
        "accuracy": acc,
        "path": model_path
    }

    response = requests.post(registry_url, json=params)
    print("Registry response:", response.status_code, response.text)


if __name__ == "__main__":
    main()
