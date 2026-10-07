from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("model.pkl")


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flight Price Prediction</title>
    </head>
    <body>

        <h1>Welcome to Flight Price Prediction</h1>

        <form id="form">

            <label>Airline:</label>
            <input id="airline" required><br><br>

            <label>Flight:</label>
            <input id="flight" required><br><br>

            <label>Source:</label>
            <input id="source" required><br><br>

            <label>Departure:</label>
            <input id="departure" required><br><br>

            <label>Stops:</label>
            <input id="stops" required><br><br>

            <label>Arrival:</label>
            <input id="arrival" required><br><br>

            <label>Destination:</label>
            <input id="destination" required><br><br>

            <label>Class:</label>
            <input id="class" required><br><br>

            <label>Duration:</label>
            <input id="duration" type="number" step="0.1" required><br><br>

            <label>Days Left:</label>
            <input id="days_left" type="number" required><br><br>

            <button type="submit">Predict Flight Price</button>

        </form>

        <h2 id="result"></h2>

        <script>
            document.getElementById("form").addEventListener("submit", async function(e) {
                e.preventDefault();

                const data = {
                    airline: document.getElementById("airline").value,
                    flight: document.getElementById("flight").value,
                    source: document.getElementById("source").value,
                    departure: document.getElementById("departure").value,
                    stops: document.getElementById("stops").value,
                    arrival: document.getElementById("arrival").value,
                    destination: document.getElementById("destination").value,
                    class: document.getElementById("class").value,
                    duration: parseFloat(document.getElementById("duration").value),
                    days_left: parseInt(document.getElementById("days_left").value)
                };

                const response = await fetch("/predict", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                document.getElementById("result").innerText =
                    "Your flight price might be ₹" +
                    result.predicted_price.toFixed(2);
            });
        </script>

    </body>
    </html>
    """


@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    prediction = model.predict(df)

    return {
        "predicted_price": float(prediction[0])
    }