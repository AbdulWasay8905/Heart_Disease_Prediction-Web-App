# heart_app.py
import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("heart_model.pkl")

st.set_page_config(page_title="Heart Disease Predictor", layout="centered")
st.title("❤️ Heart Disease Prediction App")

st.write("""
This app predicts the **likelihood of heart disease** based on medical details.  
Please enter the following values carefully.  
""")

# ------------------------------
# Input Form
# ------------------------------
with st.form("patient_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 20, 100, 50, help="Age of the patient in years")
        sex = st.selectbox("Sex", [0,1], help="0 = Female, 1 = Male")
        cp = st.selectbox("Chest Pain Type", [0,1,2,3], 
                          help="0: Typical Angina, 1: Atypical Angina, 2: Non-anginal, 3: Asymptomatic")
        trestbps = st.number_input("Resting Blood Pressure", 80, 200, 120, help="Measured in mm Hg")
        chol = st.number_input("Cholesterol", 100, 600, 200, help="Serum cholesterol in mg/dl")
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0,1], help="1 = True, 0 = False")

    with col2:
        restecg = st.selectbox("Resting ECG", [0,1,2], help="Electrocardiographic results (0-2)")
        thalach = st.number_input("Max Heart Rate Achieved", 70, 250, 150)
        exang = st.selectbox("Exercise Induced Angina", [0,1], help="1 = Yes, 0 = No")
        oldpeak = st.number_input("ST Depression", 0.0, 10.0, 1.0, step=0.1, 
                                  help="ST depression induced by exercise relative to rest")
        slope = st.selectbox("Slope of Peak Exercise ST Segment", [0,1,2])
        ca = st.selectbox("Number of Major Vessels", [0,1,2,3,4], help="Colored by fluoroscopy")
        thal = st.selectbox("Thal", [1,2,3], help="1 = Normal, 2 = Fixed Defect, 3 = Reversible Defect")

    submitted = st.form_submit_button("Predict")

# ------------------------------
# Prediction
# ------------------------------
if submitted:
    patient_data = pd.DataFrame({
        "age": [age],
        "sex": [sex],
        "cp": [cp],
        "trestbps": [trestbps],
        "chol": [chol],
        "fbs": [fbs],
        "restecg": [restecg],
        "thalach": [thalach],
        "exang": [exang],
        "oldpeak": [oldpeak],
        "slope": [slope],
        "ca": [ca],
        "thal": [thal]
    })

    prediction = model.predict(patient_data)[0]
    probability = model.predict_proba(patient_data)[0][1] * 100

    st.subheader("📋 Patient Details")
    st.table(patient_data)

    if prediction == 1:
        st.error(f"⚠️ High Risk: The patient is likely to have heart disease.")
        st.write(f"**Probability:** {probability:.2f}%")
        st.info("This means the entered values show patterns commonly linked with heart disease.")
    else:
        st.success(f"✅ Low Risk: The patient is unlikely to have heart disease.")
        st.write(f"**Probability:** {100 - probability:.2f}%")
        st.info("The values entered suggest a lower chance of heart disease.")

st.markdown("---")
st.caption("🔍 This tool is for **learning and demonstration only**. Please consult a doctor for medical decisions.")
