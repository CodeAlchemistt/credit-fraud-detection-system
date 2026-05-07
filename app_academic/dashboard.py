import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os
import sys

# 1. Page Configuration
st.set_page_config(page_title="Fraud Detection System", page_icon="🛡️", layout="wide")

# Point Python to our backend files so we can reuse our engineering scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend_pipeline.db_setup import create_db_connection
from backend_pipeline.etl_pipeline import extract_data, clean_and_normalize
from backend_pipeline.eda_visuals import generate_eda_plots

st.title("🛡️ Credit Card Fraud Detection System")
st.markdown("*Academic Presentation Dashboard - Vizztal Academy*")
st.markdown("---")

# 2. Cached Resource Loading (Prevents crashing and speeds up the app)
@st.cache_resource
def load_model():
    model_path = os.path.join("models", "fraud_model.pkl")
    return joblib.load(model_path)

@st.cache_data
def load_database_data():
    # Connect to your local database using the credentials we established
    conn = create_db_connection("localhost", "root", "passion", "fraud_detection_db")
    if conn:
        raw_df = extract_data(conn)
        cleaned_df = clean_and_normalize(raw_df)
        conn.close()
        return cleaned_df
    return None

# Load the AI and Data safely
try:
    model = load_model()
    st.sidebar.success("✅ Dashboard")
except FileNotFoundError:
    st.error("Model file not found. Please ensure 'fraud_model.pkl' is inside the 'models' folder.")
    st.stop()

df = load_database_data()
if df is not None:
    st.sidebar.success(f"✅ Database Connected ({len(df):,} rows)")
else:
    st.sidebar.error("❌ Failed to connect to MySQL database.")

# 3. Create Clean Navigation Tabs
tab1, tab2 = st.tabs(["📊 Academic Data Visualizations", "🛡️ Live AI Tester"])

# --- TAB 1: Visualizations ---
with tab1:
    st.header("Exploratory Data Analysis")
    st.write("These charts are generated live from the MySQL transaction database.")
    
    if df is not None:
        # Generate the figure but DO NOT pop it open; pass it to Streamlit instead
        fig = generate_eda_plots(df, return_fig=True)
        st.pyplot(fig)
    else:
        st.warning("Cannot generate charts without a database connection.")

# --- TAB 2: AI Tester ---
with tab2:
    st.header("Live Transaction Tester")
    st.write("Select a transaction scenario to test the AI, or manually override the PCA features.")
    
    # Dropdown for user-friendly scenarios
    scenario = st.selectbox(
        "Select Transaction Scenario",
        (
            "Normal: Small Local Coffee Shop Purchase", 
            "Normal: Regular Monthly Rent Payment",
            "Suspicious: High-Value Overseas Electronics Purchase",
            "Suspicious: Rapid Succession Micro-Transactions"
        )
    )
    
    st.markdown("### Transaction Details")
    col1, col2 = st.columns(2)
    
    # Set the hidden variables based on the user's scenario choice
    if scenario == "Normal: Small Local Coffee Shop Purchase":
        default_amount = 4.50
        default_time = 0.5
        default_v14 = 0.1  
        default_v4 = -0.5  
    elif scenario == "Normal: Regular Monthly Rent Payment":
        default_amount = 1200.00
        default_time = 0.1
        default_v14 = 0.5
        default_v4 = -0.2
    elif scenario == "Suspicious: High-Value Overseas Electronics Purchase":
        default_amount = 3500.00
        default_time = -1.5
        default_v14 = -6.5 
        default_v4 = 5.0   
    else:
        default_amount = 1.50
        default_time = -2.0
        default_v14 = -8.0 
        default_v4 = 6.0   
    
    with col1:
        amount = st.number_input("Transaction Amount ($)", value=default_amount, step=10.0)
        time = st.number_input("Time Factor (Scaled)", value=default_time, step=0.1)
    
    with col2:
        st.info("The original dataset uses anonymized PCA features to protect privacy. These represent hidden metadata like location and merchant.")
        v14 = st.number_input("PCA Feature V14", value=default_v14, step=0.5)
        v4 = st.number_input("PCA Feature V4", value=default_v4, step=0.5)
    
    # Prediction Logic
    if st.button("Run AI Analysis", type="primary"):
        features = np.zeros(30)
        features[0] = time      
        features[4] = v4         
        features[14] = v14       
        features[29] = amount    
        
        prediction = model.predict([features])
        
        st.markdown("### Analysis Result:")
        if prediction[0] == 1:
            st.error("🚨 **FRAUD DETECTED** - This transaction matches anomalous patterns.")
        else:
            st.success("✅ **TRANSACTION APPROVED** - No fraudulent patterns detected.")