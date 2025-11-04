# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 23:31:14 2025

@author: MIND-HACKER
"""

import streamlit as st
import pandas as pd
import pickle

# --- Load trained model ---
model = pickle.load(open('25RP18835.sav', 'rb'))

# --- App Header ---
st.title("🌾 Crop Yield Prediction App")
st.write("Developed by *IMANISHIMWE Nadine*")
st.write("Fill in your crop and environmental details below to estimate yield:")

# --- User Inputs ---
Region = st.selectbox("Select Region", ["North", "South", "East", "West"])
Soil_Type = st.selectbox("Select Soil Type", ["Sandy", "Clay", "Loam", "Silt", "Peaty", "Chalky"])
Crop = st.selectbox("Select Crop", ["Cotton", "Rice", "Barley", "Soybean", "Wheat", "Maize"])
Rainfall_mm = st.number_input("🌧️ Rainfall (mm)", min_value=0.0, step=0.1)
Temperature_Celsius = st.number_input("🌡️ Temperature (°C)", min_value=-10.0, step=0.1)
Fertilizer_Used = st.selectbox("Fertilizer Used", ["TRUE", "FALSE"])
Irrigation_Used = st.selectbox("Irrigation Used", ["TRUE", "FALSE"])
Weather_Condition = st.selectbox("Weather Condition", ["Sunny", "Rainy", "Cloudy"])
Days_to_Harvest = st.number_input("Days to Harvest", min_value=0, step=1)

# --- Encoding for categorical variables ---
region_map = {"North": 0, "South": 1, "East": 2, "West": 3}
soil_map = {"Sandy": 0, "Clay": 1, "Loam": 2, "Silt": 3, "Peaty": 4, "Chalky": 5}
crop_map = {"Cotton": 0, "Rice": 1, "Barley": 2, "Soybean": 3, "Wheat": 4, "Maize": 5}
weather_map = {"Sunny": 0, "Rainy": 1, "Cloudy": 2}

# --- Prepare input data ---
encoded_data = {
    'Region': region_map[Region],
    'Soil_Type': soil_map[Soil_Type],
    'Crop': crop_map[Crop],
    'Rainfall_mm': Rainfall_mm,
    'Temperature_Celsius': Temperature_Celsius,
    'Fertilizer_Used': 1 if Fertilizer_Used == "TRUE" else 0,
    'Irrigation_Used': 1 if Irrigation_Used == "TRUE" else 0,
    'Weather_Condition': weather_map[Weather_Condition],
    'Days_to_Harvest': Days_to_Harvest
}

input_data = pd.DataFrame([encoded_data])

# --- Prediction ---
if st.button("🔍 Predict Crop Yield"):
    prediction = model.predict(input_data)
    st.success(f"🌾 predicted Yield in tons per hectare is: {prediction[0]:.2f}")

