import numpy as np

def detect_outliers_iqr(df, feature):
    """
    Flags potential outliers (frauds) using the Interquartile Range (IQR) on a given feature.
    
    Inputs: DataFrame, string of the feature name to analyze (e.g., 'V14')
    Outputs: DataFrame containing only the flagged outliers
    """
    # Calculate the 25th and 75th percentiles
    q1 = np.percentile(df[feature], 25)
    q3 = np.percentile(df[feature], 75)
    
    # Calculate the IQR
    iqr = q3 - q1
    
    # Determine the lower and upper bounds for outlier detection
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    
    # Filter the DataFrame to find outliers
    outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)]
    print(f"IQR Anomaly Detection on {feature}: Flagged {len(outliers)} potential outliers.")
    return outliers

def prepare_ml_data(df):
    """
    Splits the data into Feature matrix (X) and Target vector (y).
    
    Inputs: Cleaned Pandas DataFrame
    Outputs: X (DataFrame of features), y (Series of targets)
    """
    # Target is our 'Class' column (0 for normal, 1 for fraud)
    y = df['Class']
    
    # Features are everything EXCEPT the 'Class' column
    X = df.drop('Class', axis=1)
    
    print(f"Data split into X (Features: {X.shape}) and y (Target: {y.shape}) sets.")
    return X, y