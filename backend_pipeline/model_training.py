import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

def train_and_evaluate_models(X, y):
    """
    Trains and compares a Logistic Regression baseline against a Random Forest model.
    
    Inputs: X (Features DataFrame), y (Target Series)
    Outputs: None (Prints performance metrics to the terminal)
    """
    # 1. Data Split: 80% of data for training the AI, 20% for testing it
    # 'stratify=y' ensures our rare frauds are divided evenly between train and test sets
    print("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 2. Baseline Model: Logistic Regression
    print("\n--- Training Logistic Regression (Baseline) ---")
    lr_model = LogisticRegression(max_iter=1000)
    lr_model.fit(X_train, y_train)
    lr_predictions = lr_model.predict(X_test)
    
    print("Logistic Regression Confusion Matrix:")
    print(confusion_matrix(y_test, lr_predictions))
    print("\nLogistic Regression Classification Report:")
    print(classification_report(y_test, lr_predictions))
    
    # 3. Advanced Model: Random Forest
    # n_estimators=50 means we are building 50 decision trees to vote on the outcome
    # class_weight='balanced' forces the model to pay extra attention to the rare frauds
    print("\n--- Training Random Forest (Advanced) ---")
    rf_model = RandomForestClassifier(n_estimators=50, random_state=42, class_weight='balanced', n_jobs=-1)
    rf_model.fit(X_train, y_train)
    rf_predictions = rf_model.predict(X_test)
    
    print("Random Forest Confusion Matrix:")
    print(confusion_matrix(y_test, rf_predictions))
    print("\nRandom Forest Classification Report:")
    print(classification_report(y_test, rf_predictions))
        
    # NEW: Save the trained model to a file
    print("Saving Random Forest model to disk...")
    joblib.dump(rf_model, 'fraud_model.pkl')
    print("Model saved successfully as 'fraud_model.pkl'")