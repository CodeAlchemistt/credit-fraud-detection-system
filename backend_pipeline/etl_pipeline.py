import pandas as pd
import numpy as np

def extract_data(connection):
    """
    Queries the database and loads transaction data into a Pandas DataFrame.
    
    Inputs: MySQL connection object
    Outputs: Pandas DataFrame containing the extracted data
    """
    query = "SELECT * FROM transactions;"
    # Using Pandas to read SQL directly into a DataFrame
    df = pd.read_sql(query, connection)
    # Drop the auto-generated MySQL id column as we don't need it for analysis
    df = df.drop('id', axis=1) 
    return df

def clean_and_normalize(df):
    """
    Handles missing values, drops duplicates, and scales specific columns manually.
    
    Inputs: Raw Pandas DataFrame
    Outputs: Cleaned and normalized Pandas DataFrame
    """
    # 1. Handle Missing Values
    df = df.dropna()
    
    # 2. Remove Duplicates
    df = df.drop_duplicates()
    
    # 3. Manual Normalization (Standard Scaling: (X - mean) / std)
    # We do this using pure NumPy to avoid relying on scikit-learn
    time_mean = np.mean(df['Time'])
    time_std = np.std(df['Time'])
    df['Time'] = (df['Time'] - time_mean) / time_std
    
    amount_mean = np.mean(df['Amount'])
    amount_std = np.std(df['Amount'])
    df['Amount'] = (df['Amount'] - amount_mean) / amount_std
    
    print("Data cleaned and normalized successfully.")
    return df