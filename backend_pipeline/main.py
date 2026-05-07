from db_setup import create_db_connection, setup_schema, insert_data_in_batches
from etl_pipeline import extract_data, clean_and_normalize
from eda_visuals import generate_eda_plots
from analytics import detect_outliers_iqr, prepare_ml_data
from model_training import train_and_evaluate_models
import os

def main():
    # --- PHASE 1: Setup ---
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = "passion"
    DB_NAME = "fraud_detection_db" 
    
    print("Connecting to MySQL...")
    conn = create_db_connection(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) 
    
    if conn:
        # --- PHASE 2: ETL ---
        print("Extracting data from database...")
        raw_df = extract_data(conn)
        cleaned_df = clean_and_normalize(raw_df)
        
        # --- PHASE 3: Visualization ---
        print("Generating EDA Visualizations...")
        generate_eda_plots(cleaned_df)
        
        # --- PHASE 4: Baseline & Prep ---
        print("Running Anomaly Detection...")
        outliers = detect_outliers_iqr(cleaned_df, feature='V14') 
        
        X, y = prepare_ml_data(cleaned_df)
        
        # --- PHASE 5: Machine Learning ---
        print("Initiating Machine Learning Models...")
        # Automatically create the models/ folder one level up if it doesn't exist
        os.makedirs(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')), exist_ok=True)
        train_and_evaluate_models(X, y)
        
        conn.close()
        print("Pipeline execution finished successfully.")

if __name__ == "__main__":
    main()