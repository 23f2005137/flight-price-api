from fastapi import FastAPI
import joblib 
import pandas as pd

app = FastAPI()

model = joblib.load("model.pkl")


@app.get("/")
def home():
    return {"message": "Flight Price Prediction API is running"}


@app.post("/predict")
def predict(data: dict):

    df = pd.DataFrame([data])

    prediction = model.predict(df)

    return {
        "predicted_price": float(prediction[0])
    }