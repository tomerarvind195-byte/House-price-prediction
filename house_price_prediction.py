"""
IBM Project: California House Price Prediction (GUI Edition)
-----------------------------------------------------------
Features: Background Training -> Interactive UI -> Real-time Prediction
"""

import os
# Memory allocation fix
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox, ttk

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# ---------------------------------------------------------
# 1. DATA PIPELINE & MODEL TRAINING
# ---------------------------------------------------------
print("Step 1: Loading dataset & training the best model (Random Forest)...")

if not os.path.exists("california_housing.csv"):
    raise FileNotFoundError("Error: 'california_housing.csv' aapke folder mein nahi mili!")

df = pd.read_csv("california_housing.csv")

# Missing values handle karna
df["total_bedrooms"] = df["total_bedrooms"].fillna(df["total_bedrooms"].median())

# Categorical mapping for GUI simulation to match model expectations
df = pd.get_dummies(df, columns=["ocean_proximity"], drop_first=True, dtype=int)

TARGET = "median_house_value"
X = df.drop(TARGET, axis=1)
y = df[TARGET]

# Features ki list save kar rahe hain taaki predictable order bana rahe
feature_columns = list(X.columns)

# Split and train (Random forest handles unscaled data natively)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

best_model = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)
best_model.fit(X_train, y_train)

print("Model training complete! Opening GUI Window...")

# ---------------------------------------------------------
# 2. GUI APPLICATION (Tkinter Engine)
# ---------------------------------------------------------
def predict_price():
    try:
        # GUI fields se values read karna
        input_data = {
            "longitude": float(entry_long.get()),
            "latitude": float(entry_lat.get()),
            "housing_median_age": float(entry_age.get()),
            "total_rooms": float(entry_rooms.get()),
            "total_bedrooms": float(entry_bedrooms.get()),
            "population": float(entry_pop.get()),
            "households": float(entry_house.get()),
            "median_income": float(entry_income.get()),
        }
        
        # OOPS standard: Categorical binary columns ko pehle 0 initialize karein
        for col in feature_columns:
            if col not in input_data:
                input_data[col] = 0
                
        # Dropdown selection ke basis par correct dummy column ko 1 karna
        selected_ocean = combo_ocean.get()
        dummy_col = f"ocean_proximity_{selected_ocean}"
        if dummy_col in input_data:
            input_data[dummy_col] = 1
            
        # Dataframe build karna identical alignment ke sath
        input_df = pd.DataFrame([input_data])[feature_columns]
        
        # Real-time prediction call
        prediction = best_model.predict(input_df)[0]
        
        # Format and display output
        label_result.config(text=f"Predicted Price: ${prediction:,.2f}", foreground="#2e7d32")
        
    except ValueError:
        messagebox.showerror("Input Error", "Kripya saare input fields mein valid numeric numbers fill karein!")

# Root window configuration
root = tk.Tk()
root.title("IBM Project: California House Price Predictor")
root.geometry("480x580")
root.configure(bg="#f5f5f5")

# Custom Styling
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10), background="#f5f5f5")
style.configure("TButton", font=("Segoe UI", 11, "bold"))

# Header Section
header_frame = tk.Frame(root, bg="#1a237e", height=60)
header_frame.pack(fill="x")
title_label = tk.Label(header_frame, text="House Price Predictor Dashboard", font=("Segoe UI", 14, "bold"), fg="white", bg="#1a237e")
title_label.pack(pady=15)

# Input Layout Frame
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill="both", expand=True)

# Grid rows helper function
def add_row(text, default_val, row):
    ttk.Label(main_frame, text=text).grid(row=row, column=0, sticky="w", pady=6, padx=5)
    entry = ttk.Entry(main_frame, width=25, font=("Segoe UI", 10))
    entry.insert(0, str(default_val))
    entry.grid(row=row, column=1, pady=6, padx=5)
    return entry

# Generating fields with reference regional averages
entry_long = add_row("Longitude (e.g. -122.23):", -122.23, 0)
entry_lat = add_row("Latitude (e.g. 37.88):", 37.88, 1)
entry_age = add_row("Housing Median Age (Years):", 41, 2)
entry_rooms = add_row("Total Rooms in Block:", 880, 3)
entry_bedrooms = add_row("Total Bedrooms in Block:", 129, 4)
entry_pop = add_row("Block Population:", 322, 5)
entry_house = add_row("Total Households:", 126, 6)
entry_income = add_row("Median Income (in $10k, e.g. 8.3):", 8.32, 7)

# Categorical Dropdown setup
ttk.Label(main_frame, text="Ocean Proximity:").grid(row=8, column=0, sticky="w", pady=6, padx=5)
combo_ocean = ttk.Combobox(main_frame, values=["INLAND", "NEAR BAY", "NEAR OCEAN", "<1H OCEAN"], width=23, font=("Segoe UI", 10), state="readonly")
combo_ocean.set("NEAR BAY")
combo_ocean.grid(row=8, column=1, pady=6, padx=5)

# Separator line
ttk.Separator(root, orient="horizontal").pack(fill="x", padx=20, pady=5)

# Execution Button
btn_predict = tk.Button(root, text="Predict Price 🚀", command=predict_price, font=("Segoe UI", 12, "bold"), bg="#1a237e", fg="white", bd=0, cursor="hand2", activebackground="#283593", activeforeground="white")
btn_predict.pack(pady=12, ipady=5, ipadx=15)

# Final Output Banner
label_result = ttk.Label(root, text="Predicted Price: $0.00", font=("Segoe UI", 15, "bold"), foreground="#1a237e")
label_result.pack(pady=10)

root.mainloop()