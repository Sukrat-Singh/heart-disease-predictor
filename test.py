import requests
import json

# URL of your Flask API endpoint
url = "http://127.0.0.1:5000/predict_api"

# Sample input data — make sure these fields match what your model expects
data = {
    "data": {
        "Age": 70,
        "Sex": "M",
        "ChestPainType": "ATA",
        "RestingBP": 130,
        "Cholesterol": 483,
        "FastingBS": 0,
        "RestingECG": "ST",
        "MaxHR": 2000,
        "ExerciseAngina": "N",
        "Oldpeak": 0.0,
        "ST_Slope": "Up"
    }
}

# Send POST request to the Flask API
response = requests.post(url, json=data)

# Check response status and print neatly
print(f"Status Code: {response.status_code}")

try:
    pred = response.json()["prediction"]
    prob = response.json()["probability"]
    print(f"Prediction: {pred} | Probability: {prob:.4f}")
except Exception:
    print("Response Text:")
    print(response.text)
