from flask import Flask, request
from flask_restful import Api, Resource, abort
import joblib
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s : %(levelname)s : %(message)s]")

app = Flask(__name__)
api = Api(app)

# Load the full pipeline (preprocessing + model)
try:
    model = joblib.load(r"models/heart_disease_model.pkl")
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")

def abort_if_missing_fields(data):
    required_fields = [
        "Age", "Sex", "ChestPainType", "RestingBP", "Cholesterol",
        "FastingBS", "RestingECG", "MaxHR", "ExerciseAngina", "Oldpeak", "ST_Slope"
    ]
    missing = [field for field in required_fields if field not in data]
    if missing:
        abort(400, message=f"Missing required fields: {', '.join(missing)}")

class HeartDiseasePredict(Resource):
    def post(self):
        logging.info("POST request received for heart disease prediction.")
        data = request.get_json()

        if "data" not in data:
            abort(400, message="JSON payload must contain 'data' key.")
        
        input_data = data["data"]
        abort_if_missing_fields(input_data)

        input_df = pd.DataFrame([input_data])

        # Pipeline handles preprocessing
        prediction = model.predict(input_df)[0]
        logging.info(f"Prediction result: {prediction}")
        proba = model.predict_proba(input_df)[0][1]
        return {"prediction": int(prediction), "probability": float(proba)}, 200


api.add_resource(HeartDiseasePredict, "/predict_api")

if __name__ == "__main__":
    app.run(debug=True)
