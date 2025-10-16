# streamlit_app.py
import streamlit as st
import joblib
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s : %(levelname)s : %(message)s]")

# Load the model
try:
    model = joblib.load("models/heart_disease_model.pkl")
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    st.error("Failed to load the model. Check server logs.")

# ------------------------
# Streamlit App
# ------------------------
st.set_page_config(page_title="Heart Disease Predictor", layout="centered")
st.title("❤️ Heart Disease Predictor")

st.write("Enter your details below to predict the risk of heart disease:")

# Input form
with st.form("prediction_form"):
    Age = st.number_input("Age", min_value=1, max_value=120, value=50)
    Sex = st.selectbox("Sex", ["M", "F"])
    ChestPainType = st.selectbox("Chest Pain Type", ["TA", "ATA", "NAP", "ASY"])
    RestingBP = st.number_input("Resting Blood Pressure", min_value=50, max_value=250, value=120)
    Cholesterol = st.number_input("Cholesterol", min_value=100, max_value=600, value=200)
    FastingBS = st.selectbox("Fasting Blood Sugar (>120 mg/dl)", [0, 1])
    RestingECG = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
    MaxHR = st.number_input("Maximum Heart Rate", min_value=60, max_value=220, value=150)
    ExerciseAngina = st.selectbox("Exercise Induced Angina", ["Y", "N"])
    Oldpeak = st.number_input("Oldpeak", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
    ST_Slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])
    
    submitted = st.form_submit_button("Predict")

if submitted:
    input_data = {
        "Age": Age,
        "Sex": Sex,
        "ChestPainType": ChestPainType,
        "RestingBP": RestingBP,
        "Cholesterol": Cholesterol,
        "FastingBS": FastingBS,
        "RestingECG": RestingECG,
        "MaxHR": MaxHR,
        "ExerciseAngina": ExerciseAngina,
        "Oldpeak": Oldpeak,
        "ST_Slope": ST_Slope
    }

    input_df = pd.DataFrame([input_data])
    
    try:
        prediction = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0][1]

        st.subheader("Prediction Result")
        st.write(
            "❤️ Heart Disease Detected" if prediction == 1 else "✅ No Heart Disease"
        )
        st.write(f"Probability: {proba:.2f}")
    except Exception as e:
        st.error(f"Error making prediction: {e}")

# Optional: show raw input
with st.expander("Show input data"):
    st.json(input_data)
