import streamlit as st
import pickle
import pandas as pd
import numpy as np

# --- Load model ---
with open('25RP18835.sav', 'rb') as file:
    model = pickle.load(file)

st.title("🌾 Crop Yield Prediction App")
st.write("Predict crop yield based on regional and environmental conditions.")

st.sidebar.header("Enter Input Features")

# --- Input options ---
regions = ['North', 'South', 'East', 'West']
soil_types = ['Sandy', 'Clay', 'Loam', 'Silt', 'Peaty']
crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Barley', 'Soybean']
weather_conditions = ['Sunny', 'Rainy', 'Cloudy']

# --- Sidebar Inputs ---
region = st.sidebar.selectbox("Region", regions)
soil_type = st.sidebar.selectbox("Soil Type", soil_types)
crop = st.sidebar.selectbox("Crop", crops)
rainfall = st.sidebar.number_input("Rainfall (mm)", min_value=0.0, step=0.1)
temperature = st.sidebar.number_input("Temperature (°C)", min_value=-10.0, step=0.1)
days_to_harvest = st.sidebar.number_input("Days to Harvest", min_value=1, step=1)
fertilizer_used = st.sidebar.selectbox("Fertilizer Used", ['Yes', 'No'])
irrigation_used = st.sidebar.selectbox("Irrigation Used", ['Yes', 'No'])
weather_condition = st.sidebar.selectbox("Weather Condition", weather_conditions)

# --- Encoding mappings (must match your training preprocessing) ---
region_map = {'North': 0, 'South': 1, 'East': 2, 'West': 3}
soil_map = {'Sandy': 0, 'Clay': 1, 'Loam': 2, 'Silt': 3, 'Peaty': 4}
crop_map = {'Rice': 0, 'Wheat': 1, 'Maize': 2, 'Cotton': 3, 'Barley': 4, 'Soybean': 5}
weather_map = {'Sunny': 0, 'Rainy': 1, 'Cloudy': 2}

# --- Prepare input ---
input_data = pd.DataFrame({
    'Region': [region_map[region]],
    'Soil_Type': [soil_map[soil_type]],
    'Crop': [crop_map[crop]],
    'Rainfall_mm': [rainfall],
    'Temperature_Celsius': [temperature],
    'Fertilizer_Used': [1 if fertilizer_used == 'Yes' else 0],
    'Irrigation_Used': [1 if irrigation_used == 'Yes' else 0],
    'Weather_Condition': [weather_map[weather_condition]],
    'Days_to_Harvest': [days_to_harvest]
})

# --- Predict ---
if st.button("Predict Yield"):
    try:
        prediction = model.predict(input_data)

        # Ensure scalar output for formatting
        if isinstance(prediction, (np.ndarray, list)):
            prediction_value = float(np.squeeze(prediction))
        else:
            prediction_value = float(prediction)

        st.success(f"🌾 Estimated Crop Yield: **{prediction_value:.2f} tons per hectare**")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.info("💡 Make sure your model expects numeric encoded features or uses a preprocessing pipeline.")